#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
MANAGER – ÅÏÇÑÉ ÇáÃÏæÇÊ ÇáãÓÊÞáÉ (Standalone)
================================================================================
åÐÇ ÇáãáÝ íæÝÑ ÃÏæÇÊ ÌÇåÒÉ ááÇÓÊÎÏÇã:
1. BaseTool – ßáÇÓ ÃÓÇÓí
2. CloudflareWorkers – äÔÑ æÊÔÛíá
3. VercelFunctions – äÔÑ ÇáÏæÇá
4. SupabaseClient – ÇáÇÊÕÇá ÈÜ Supabase
5. AIHordeClient – ÊæáíÏ ÇáäÕæÕ æÇáÕæÑ
6. PlanetScaleClient – ÇáÇÊÕÇá ÈÜ PlanetScale
7. PluginManager – ÇßÊÔÇÝ ÊáÞÇÆí
8. ExtendedToolsManager – ãÏíÑ ãÑßÒí

áÇ íÞæã åÐÇ ÇáãáÝ ÈÃí ÍÞä (injection) Ýí ÇáßæÏ ÇáÃÕáí. íãßä ÇÓÊÎÏÇãå ÈãÝÑÏå.
================================================================================
"""

import asyncio
import json
import os
import logging
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from abc import ABC, abstractmethod

from foundation import SmartHTTPClient, check_command_exists, safe_run_command

logger = logging.getLogger("ManagerStandalone")

# =============================================================================
# 1. BaseTool
# =============================================================================
class BaseTool(ABC):
    def __init__(self, name: str):
        self.name = name
        self._available = None

    @abstractmethod
    async def is_available(self) -> bool:
        pass

    @abstractmethod
    async def test_connection(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    async def close(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# =============================================================================
# 2. CloudflareWorkers
# =============================================================================
class CloudflareWorkers(BaseTool, SmartHTTPClient):
    def __init__(self, account_id: str, api_token: str):
        BaseTool.__init__(self, "cloudflare_workers")
        SmartHTTPClient.__init__(self)
        self.account_id = account_id
        self.api_token = api_token
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}"

    async def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        self._available = bool(self.account_id and self.api_token)
        return self._available

    async def test_connection(self) -> Tuple[bool, str]:
        if not await self.is_available():
            return False, "Missing account_id or api_token"
        try:
            resp = await self.get(f"{self.base_url}/workers/scripts", headers={"Authorization": f"Bearer {self.api_token}"})
            return resp.status == 200, "OK" if resp.status == 200 else f"HTTP {resp.status}"
        except Exception as e:
            return False, str(e)

    async def deploy_worker(self, script_name: str, code: str) -> bool:
        if not await self.is_available():
            raise RuntimeError("CloudflareWorkers not available")
        url = f"{self.base_url}/workers/scripts/{script_name}"
        headers = {"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/javascript"}
        resp = await self.put(url, data=code, headers=headers)
        data = await resp.json()
        return data.get("success", False)

    async def close(self):
        await SmartHTTPClient.close(self)


# =============================================================================
# 3. VercelFunctions
# =============================================================================
class VercelFunctions(BaseTool):
    def __init__(self, api_token: str):
        BaseTool.__init__(self, "vercel")
        self.api_token = api_token
        self._client = SmartHTTPClient()

    async def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        self._available = bool(self.api_token) and check_command_exists("vercel")
        return self._available

    async def test_connection(self) -> Tuple[bool, str]:
        if not await self.is_available():
            if not check_command_exists("vercel"):
                return False, "Vercel CLI not found"
            return False, "Missing api_token"
        return True, "OK"

    async def deploy(self, project_path: str) -> Dict:
        if not await self.is_available():
            raise RuntimeError("VercelFunctions not available")
        cmd = ["vercel", "--token", self.api_token, "--prod", "--yes", project_path]
        code, out, err = await safe_run_command(cmd, timeout=120)
        url = None
        if code == 0:
            import re
            m = re.search(r'https://[^\s]+', out)
            if m:
                url = m.group(0)
        return {"success": code == 0, "url": url, "output": out, "error": err}

    async def close(self):
        await self._client.close()


# =============================================================================
# 4. SupabaseClient
# =============================================================================
class SupabaseClient(BaseTool, SmartHTTPClient):
    def __init__(self, url: str, anon_key: str):
        BaseTool.__init__(self, "supabase")
        SmartHTTPClient.__init__(self)
        self.url = url.rstrip('/')
        self.anon_key = anon_key
        self.rest_url = f"{self.url}/rest/v1"

    async def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        self._available = bool(self.url and self.anon_key)
        return self._available

    async def test_connection(self) -> Tuple[bool, str]:
        if not await self.is_available():
            return False, "Missing URL or anon_key"
        try:
            headers = {"apikey": self.anon_key, "Authorization": f"Bearer {self.anon_key}"}
            resp = await self.get(f"{self.rest_url}/pg_catalog.pg_tables?limit=1", headers=headers)
            return resp.status == 200, "OK" if resp.status == 200 else f"HTTP {resp.status}"
        except Exception as e:
            return False, str(e)

    async def insert(self, table: str, data: Dict) -> Dict:
        headers = {"apikey": self.anon_key, "Authorization": f"Bearer {self.anon_key}"}
        resp = await self.post(f"{self.rest_url}/{table}", json=data, headers=headers)
        return await resp.json()

    async def close(self):
        await SmartHTTPClient.close(self)


# =============================================================================
# 5. AIHordeClient
# =============================================================================
class AIHordeClient(BaseTool, SmartHTTPClient):
    def __init__(self, api_key: str = None):
        BaseTool.__init__(self, "ai_horde")
        SmartHTTPClient.__init__(self, max_retries=5, base_delay=2.0)
        self.api_key = api_key
        self.base_url = "https://stablehorde.net/api/v2"

    async def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            resp = await self.get(f"{self.base_url}/status")
            self._available = resp.status == 200
            return self._available
        except Exception:
            self._available = False
            return False

    async def test_connection(self) -> Tuple[bool, str]:
        try:
            resp = await self.get(f"{self.base_url}/status")
            if resp.status == 200:
                data = await resp.json()
                return True, f"Queued: {data.get('queued_requests', 0)}"
            return False, f"HTTP {resp.status}"
        except Exception as e:
            return False, str(e)

    async def generate_text(self, prompt: str, model: str = "LLaMA3", max_length: int = 100) -> str:
        headers = {"apikey": self.api_key} if self.api_key else {}
        payload = {"prompt": prompt, "max_length": max_length, "models": [model]}
        resp = await self.post(f"{self.base_url}/generate/text", json=payload, headers=headers)
        data = await resp.json()
        gens = data.get("generations", [])
        return gens[0].get("text", "") if gens else ""

    async def close(self):
        await SmartHTTPClient.close(self)


# =============================================================================
# 6. PlanetScaleClient
# =============================================================================
class PlanetScaleClient(BaseTool):
    def __init__(self, connection_string: str):
        BaseTool.__init__(self, "planetscale")
        self.conn_string = connection_string
        self._pool = None

    async def is_available(self) -> bool:
        try:
            import aiomysql
            return True
        except ImportError:
            return False

    async def test_connection(self) -> Tuple[bool, str]:
        if not await self.is_available():
            return False, "aiomysql not installed"
        try:
            import aiomysql
            pool = await aiomysql.create_pool(dsn=self.conn_string)
            pool.close()
            await pool.wait_closed()
            return True, "OK"
        except Exception as e:
            return False, str(e)

    async def execute(self, query: str, *args) -> List[Dict]:
        if self._pool is None:
            import aiomysql
            self._pool = await aiomysql.create_pool(dsn=self.conn_string)
        async with self._pool.acquire() as conn:
            from pymysql.cursors import DictCursor
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchall()

    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()


# =============================================================================
# 7. PluginManager
# =============================================================================
class PluginManager:
    def __init__(self, plugin_dir: str = None):
        self.plugin_dir = Path(plugin_dir) if plugin_dir else Path(__file__).parent / "tools"
        self.tools: Dict[str, BaseTool] = {}

    def discover(self) -> Dict[str, BaseTool]:
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            return {}
        for mod_info in pkgutil.iter_modules([str(self.plugin_dir)]):
            try:
                mod = importlib.import_module(f"tools.{mod_info.name}")
                for attr in dir(mod):
                    obj = getattr(mod, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseTool) and obj != BaseTool:
                        try:
                            self.tools[attr.lower()] = obj()
                            logger.info(f"Discovered tool: {attr}")
                        except Exception as e:
                            logger.debug(f"Could not instantiate {attr}: {e}")
            except ImportError as e:
                logger.debug(f"Cannot import {mod_info.name}: {e}")
            except Exception as e:
                logger.warning(f"Failed to load plugin {mod_info.name}: {e}")
        return self.tools

    def register(self, name: str, tool: BaseTool):
        self.tools[name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)


# =============================================================================
# 8. ExtendedToolsManager
# =============================================================================
class ExtendedToolsManager:
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.plugin_manager = PluginManager()

    def register(self, name: str, tool: BaseTool):
        self.tools[name] = tool

    def discover_plugins(self):
        self.tools.update(self.plugin_manager.discover())

    async def start(self) -> Dict[str, bool]:
        results = {}
        for name, tool in self.tools.items():
            try:
                if await tool.is_available():
                    ok, msg = await tool.test_connection()
                    results[name] = ok
                    logger.info(f"{name}: {msg}")
                else:
                    results[name] = False
            except Exception as e:
                results[name] = False
                logger.error(f"{name}: {e}")
        return results

    async def stop(self):
        for tool in self.tools.values():
            await tool.close()

    def get(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)


# =============================================================================
# ÇáÊÔÛíá ÇáãÓÊÞá (ááÇÎÊÈÇÑ)
# =============================================================================
async def main():
    print("\n" + "=" * 60)
    print("ÊÔÛíá MANAGER (ÇáäÓÎÉ ÇáãÓÊÞáÉ)")
    print("=" * 60)

    horde = AIHordeClient()
    if await horde.is_available():
        ok, msg = await horde.test_connection()
        print(f"AI Horde: {msg}")
    await horde.close()

    pm = PluginManager()
    tools = pm.discover()
    print(f"ÚÏÏ ÇáÅÖÇÝÇÊ ÇáãßÊÔÝÉ: {len(tools)}")

    print("\n? Manager (ÇáäÓÎÉ ÇáãÓÊÞáÉ) ÊÚãá ÈÔßá ÕÍíÍ")

if __name__ == "__main__":
    asyncio.run(main())
