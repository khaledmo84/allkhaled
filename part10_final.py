#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ÇáÌÒÁ ÇáÚÇÔÑ – ÇáÅÕÏÇÑ ÇáäåÇÆí 15.0.0 (53 ãíÒÉ)
ÌãíÚ ÇáãíÒÇÊ ÇáÃÓÇÓíÉ (1-42) æÇáÅÖÇÝÇÊ (43-53) Ýí ãáÝ æÇÍÏ.
Êã ÅÕáÇÍ ÌãíÚ äÞÇØ ÇáÖÚÝ æÇáÊßÇãá ãÚ ÇáßæÏ ÇáÖÎã.
-----------------------------------------------------------------------------
ÇáãÊÛíÑÇÊ ÇáÈíÆíÉ ÇáãØáæÈÉ:
- DEPLOYER_PRIVATE_KEY: ÇáãÝÊÇÍ ÇáÎÇÕ ááäÔÑ æÇáãÚÇãáÇÊ (hex)
- SECONDARY_WALLET: ÚäæÇä ÇáãÍÝÙÉ ÇáËÇäæíÉ áÊÍæíá ÇáÃãæÇá (ÇÎÊíÇÑí)
- ALKHALED_MASTER_KEY: ãÝÊÇÍ ÑÆíÓí áÊÔÝíÑ ÇáãÝÇÊíÍ (32 ÈÇíÊ hex)
- ETHERSCAN_API_KEY, ARBISCAN_API_KEY, ... : ãÝÇÊíÍ APIs ááÓáÇÓá
- ETHEREUM_RPC_URL, ARBITRUM_RPC_URL, ... : ÚäÇæíä RPC áßá ÔÈßÉ
- OPENSEA_API_KEY, BLUR_API_KEY: ãÝÇÊíÍ APIs áÃÓæÇÞ NFT (ÇÎÊíÇÑí)
- USE_REDIS: true/false áÇÓÊÎÏÇã Redis ááÊÎÒíä ÇáãÄÞÊ (ÇÎÊíÇÑí)
-----------------------------------------------------------------------------
"""

import asyncio
import aiohttp
import json
import hashlib
import secrets
import time
import base64
import logging
import os
import sys
import traceback
import subprocess
import random
import uuid
import re
import shlex
import hmac
import functools
import tempfile
from typing import Dict, List, Optional, Any, Tuple, Union, Callable, Awaitable, Set
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# ÇÓÊíÑÇÏÇÊ ÇáäÙÇã ÇáÃÓÇÓí (ãÑäÉ)
# =============================================================================
try:
    from core import GodPulse, ExperienceDB, ExecutionEngine, AtomicNonceManager
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False
    class GodPulse: pass
    class ExperienceDB: pass
    class ExecutionEngine: pass
    class AtomicNonceManager: pass

try:
    from agents import AgentOrchestrator, BaseAgent
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    class AgentOrchestrator: pass
    class BaseAgent: pass

try:
    from unified import Opportunity, TradeRecord, StrategyCategory
    UNIFIED_AVAILABLE = True
except ImportError:
    UNIFIED_AVAILABLE = False
    class Opportunity:
        def __init__(self, name, category, profit, params, chain):
            self.id = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:16]
            self.name = name
            self.category = category
            self.profit = profit
            self.params = params
            self.chain = chain
    class TradeRecord:
        def __init__(self, opportunity_id, profit_usd, gas_cost_usd, tx_hash, chain, executor, metadata=None):
            self.opportunity_id = opportunity_id
            self.profit_usd = profit_usd
            self.gas_cost_usd = gas_cost_usd
            self.tx_hash = tx_hash
            self.chain = chain
            self.executor = executor
            self.metadata = metadata or {}
    class StrategyCategory(Enum):
        ARBITRAGE = "arbitrage"
        LIQUIDITY = "liquidity"
        YIELD = "yield"
        CLOSE = "close"

try:
    from core import AddressManager
    ADDRESS_MANAGER_AVAILABLE = True
except ImportError:
    ADDRESS_MANAGER_AVAILABLE = False

# =============================================================================
# ãßÊÈÇÊ ÎÇÑÌíÉ (ãÚ fallback Âãä)
# =============================================================================
NUMPY_AVAILABLE = False
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    pass

TORCH_AVAILABLE = False
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    pass

TENSEAL_AVAILABLE = False
try:
    import tenseal as ts
    TENSEAL_AVAILABLE = True
except ImportError:
    pass

CRYPTO_AVAILABLE = False
try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    pass

CACHE_AVAILABLE = False
try:
    from aiocache import cached, Cache
    from aiocache.serializers import JsonSerializer
    CACHE_AVAILABLE = True
except ImportError:
    pass

WEB3_AVAILABLE = False
try:
    from web3 import Web3
    from eth_account import Account
    WEB3_AVAILABLE = True
except ImportError:
    pass

SOLCX_AVAILABLE = False
try:
    from solcx import compile_source, install_solc
    SOLCX_AVAILABLE = True
except ImportError:
    pass

REDIS_AVAILABLE = False
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    pass

SOLANA_AVAILABLE = False
try:
    from solders.pubkey import Pubkey
    from solana.rpc.async_api import AsyncClient
    from solana.rpc.commitment import Confirmed
    SOLANA_AVAILABLE = True
except ImportError:
    pass

# =============================================================================
# ÅÚÏÇÏ ÇáÊÓÌíá
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('alkhaled_part10.log')
    ]
)
logger = logging.getLogger('AlkhaledPart10')

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'msg'):
            record.msg = re.sub(r'private_key=[a-f0-9]{64}', 'private_key=***', str(record.msg))
            record.msg = re.sub(r'password=[^ ]+', 'password=***', str(record.msg))
        return True
logger.addFilter(SensitiveDataFilter())

# =============================================================================
# ÇÓÊËäÇÁÇÊ ãÎÕÕÉ
# =============================================================================
class DataUnavailableError(Exception): pass
class ExternalServiceError(Exception): pass
class SecurityError(Exception): pass
class ConfigurationError(Exception): pass
class MarketRiskError(Exception): pass

# =============================================================================
# ÃÏæÇÊ ãÓÇÚÏÉ ãÍÓäÉ
# =============================================================================
def retry_async(max_attempts=3, delay=1, backoff=2, retry_on=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except asyncio.CancelledError:
                    raise
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    if not isinstance(e, retry_on):
                        raise
                    last_exception = e
                    wait = delay * (backoff ** attempt)
                    logger.warning(f"Attempt {attempt+1} for {func.__name__} failed: {e}. Retry in {wait}s")
                    await asyncio.sleep(wait)
            raise ExternalServiceError(f"{func.__name__} failed after {max_attempts} attempts") from last_exception
        return wrapper
    return decorator

def stable_hash(value: Any) -> int:
    s = str(value).encode()
    return int(hashlib.sha256(s).hexdigest(), 16)

def safe_int(val: Any, default: int = 0) -> int:
    if isinstance(val, int): return val
    if isinstance(val, bytes): return int.from_bytes(val, byteorder='big')
    if isinstance(val, str):
        if val.startswith('0x'):
            try: return int(val, 16)
            except ValueError: pass
        try: return int(val)
        except ValueError: pass
    return default

def safe_float(val: Any, default: float = 0.0) -> float:
    if isinstance(val, float): return val
    if isinstance(val, int): return float(val)
    if isinstance(val, str):
        try: return float(val)
        except ValueError: pass
    return default

def encrypt_aes_gcm(key: bytes, plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
    if not CRYPTO_AVAILABLE: raise SecurityError("Cryptography library not available")
    iv = secrets.token_bytes(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, iv, encryptor.tag

def decrypt_aes_gcm(key: bytes, ciphertext: bytes, iv: bytes, tag: bytes) -> bytes:
    if not CRYPTO_AVAILABLE: raise SecurityError("Cryptography library not available")
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# =============================================================================
# SecureKeyManager
# =============================================================================
class SecureKeyManager:
    def __init__(self, key_name: str, rotation_seconds: int = 86400):
        self.key_name = key_name
        self.rotation_seconds = rotation_seconds
        self.master_key = self._get_master_key()
        self.key_file = os.path.expanduser(f"~/.alkhaled/keys/{key_name}.enc")
        self._ensure_dir()
        self._load_or_create_key()
        self.key_created_at = time.time()
        self._lock = asyncio.Lock()

    def _ensure_dir(self):
        os.makedirs(os.path.dirname(self.key_file), mode=0o700, exist_ok=True)

    def _get_master_key(self) -> bytes:
        master_key_hex = os.environ.get('ALKHALED_MASTER_KEY')
        if not master_key_hex: raise ConfigurationError("ALKHALED_MASTER_KEY environment variable not set.")
        try: return bytes.fromhex(master_key_hex)
        except ValueError: raise ConfigurationError("ALKHALED_MASTER_KEY must be a 32-byte hex string.")

    def _derive_key(self, salt: bytes) -> bytes:
        if CRYPTO_AVAILABLE:
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            return kdf.derive(self.master_key)
        else:
            return hashlib.pbkdf2_hmac('sha256', self.master_key, salt, 100000, dklen=32)

    def _encrypt(self, data: bytes) -> bytes:
        if not CRYPTO_AVAILABLE: raise SecurityError("Cannot encrypt without cryptography")
        salt = secrets.token_bytes(16)
        key = self._derive_key(salt)
        ciphertext, iv, tag = encrypt_aes_gcm(key, data)
        return salt + iv + tag + ciphertext

    def _decrypt(self, encrypted: bytes) -> bytes:
        if not CRYPTO_AVAILABLE: raise SecurityError("Cannot decrypt without cryptography")
        salt = encrypted[:16]; iv = encrypted[16:28]; tag = encrypted[28:44]; ciphertext = encrypted[44:]
        key = self._derive_key(salt)
        return decrypt_aes_gcm(key, ciphertext, iv, tag)

    def _load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                encrypted = f.read()
            self.current_key = self._decrypt(encrypted)
        else:
            self.current_key = secrets.token_bytes(32)
            self._save_key()

    def _save_key(self):
        encrypted = self._encrypt(self.current_key)
        with open(self.key_file, 'wb') as f:
            f.write(encrypted)
        os.chmod(self.key_file, 0o600)

    async def get_key(self) -> bytes:
        async with self._lock:
            if time.time() - self.key_created_at > self.rotation_seconds:
                self.current_key = secrets.token_bytes(32)
                self._save_key()
                self.key_created_at = time.time()
                logger.info(f"Rotated key {self.key_name}")
            return self.current_key

    async def encrypt(self, data: bytes) -> bytes:
        key = await self.get_key()
        salt = secrets.token_bytes(16)
        derived = self._derive_key(salt)
        ciphertext, iv, tag = encrypt_aes_gcm(derived, data)
        return salt + iv + tag + ciphertext

    async def decrypt(self, encrypted: bytes) -> bytes:
        key = await self.get_key()
        salt = encrypted[:16]; iv = encrypted[16:28]; tag = encrypted[28:44]; ciphertext = encrypted[44:]
        derived = self._derive_key(salt)
        return decrypt_aes_gcm(derived, ciphertext, iv, tag)

# =============================================================================
# CacheManager
# =============================================================================
class CacheManager:
    def __init__(self, use_redis=False, redis_url=None, max_size=10000):
        self.use_redis = use_redis and REDIS_AVAILABLE and CACHE_AVAILABLE
        self.max_size = max_size
        if self.use_redis:
            self.cache = Cache(Cache.REDIS, endpoint=redis_url or "redis://localhost", serializer=JsonSerializer())
        else:
            self.cache = {}
            self.ttl = {}
            self._access_order = deque()
        self._cleanup_task = None
        self._closed = False
        self._lock = asyncio.Lock()

    async def start_cleanup(self, interval: int = 300):
        if self.use_redis or self._closed: return
        self._cleanup_task = asyncio.create_task(self._cleanup_loop(interval))

    async def _cleanup_loop(self, interval: int):
        while not self._closed:
            await asyncio.sleep(interval)
            async with self._lock:
                now = time.time()
                expired = [k for k, t in self.ttl.items() if t <= now]
                for k in expired:
                    self.cache.pop(k, None); self.ttl.pop(k, None)
                if len(self.cache) > self.max_size:
                    to_remove = len(self.cache) - self.max_size
                    for _ in range(to_remove):
                        if self._access_order:
                            oldest = self._access_order.popleft()
                            self.cache.pop(oldest, None); self.ttl.pop(oldest, None)

    async def get(self, key: str) -> Optional[Any]:
        if self._closed: return None
        if self.use_redis: return await self.cache.get(key)
        async with self._lock:
            now = time.time()
            if key in self.cache: self._access_order.append(key)
            if len(self._access_order) > self.max_size * 2: self._access_order = deque(list(self._access_order)[-self.max_size:])
            if key in self.ttl and self.ttl[key] <= now:
                self.cache.pop(key, None); self.ttl.pop(key, None); return None
            return self.cache.get(key)

    async def set(self, key: str, value: Any, ttl: int = 60):
        if self._closed: return
        if self.use_redis: await self.cache.set(key, value, ttl=ttl)
        else:
            async with self._lock:
                self.cache[key] = value
                self.ttl[key] = time.time() + ttl
                self._access_order.append(key)
                if len(self.cache) > self.max_size:
                    oldest = self._access_order.popleft()
                    self.cache.pop(oldest, None); self.ttl.pop(oldest, None)

    async def delete(self, key: str):
        if self._closed: return
        if self.use_redis: await self.cache.delete(key)
        else:
            async with self._lock:
                self.cache.pop(key, None); self.ttl.pop(key, None)

    async def close(self):
        self._closed = True
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try: await self._cleanup_task
            except asyncio.CancelledError: pass
        if self.use_redis: await self.cache.close()

# =============================================================================
# SolanaConnector
# =============================================================================
class SolanaConnector:
    def __init__(self, rpc_url: str = None):
        if not SOLANA_AVAILABLE: raise RuntimeError("Solana libraries not installed.")
        self.rpc_url = rpc_url or os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        self.client = AsyncClient(self.rpc_url)

    async def get_price(self, token_mint: str) -> float:
        logger.warning("Solana price fetching requires external API integration. Returning 0.")
        return 0.0

    async def get_transactions(self, address: str, limit: int = 100) -> List[Dict]:
        try:
            pubkey = Pubkey.from_string(address)
            sigs = await self.client.get_signatures_for_address(pubkey, limit=limit)
            return [{'signature': sig['signature'], 'slot': sig['slot']} for sig in sigs.get('result', [])]
        except Exception as e:
            logger.error(f"Solana transaction fetch failed: {e}")
            return []

    async def close(self):
        await self.client.close()

# =============================================================================
# ExtendedGodPulse (ÇáãÍÑß ÇáÑÆíÓí)
# =============================================================================
class ExtendedGodPulse:
    def __init__(self, original_god: Optional[GodPulse] = None):
        # ÅÐÇ ãÑÑäÇ ßÇÆä GodPulse ÃÕáí¡ ääÓÎ ãäå ÇáÎÕÇÆÕ ÇáÖÑæÑíÉ áÊÌäÈ ÇÒÏæÇÌíÉ ÇáÇÊÕÇáÇÊ
        if original_god is not None:
            self._session = getattr(original_god, '_session', None)
            self._cache = getattr(original_god, '_cache', CacheManager())
            self._last_valid = getattr(original_god, '_last_valid', {})
            self._last_valid_timestamps = getattr(original_god, '_last_valid_timestamps', {})
            self._lock = getattr(original_god, '_lock', asyncio.Lock())
            self._solana = getattr(original_god, '_solana', None)
            self._last_cleanup = getattr(original_god, '_last_cleanup', time.time())
        else:
            self._session = None
            self._cache = CacheManager(use_redis=os.environ.get('USE_REDIS') == 'true')
            self._last_valid = {}
            self._last_valid_maxsize = 1000
            self._last_valid_timestamps = {}
            self._cleanup_interval = 3600
            self._last_cleanup = time.time()
            self._lock = asyncio.Lock()
            self._solana = None

        # ãÕÇÏÑ ÇáÈíÇäÇÊ (ËÇÈÊÉ)
        self._defillama_base = "https://api.llama.fi"
        self._coingecko_base = "https://api.coingecko.com/api/v3"
        self._opensea_base = "https://api.opensea.io/api/v2"
        self._blur_base = "https://api.blur.io/v1"
        self._etherscan_base = "https://api.etherscan.io/api"
        self._arbiscan_base = "https://api.arbiscan.io/api"
        self._optimismscan_base = "https://api-optimistic.etherscan.io/api"
        self._polygonscan_base = "https://api.polygonscan.com/api"
        self._bscscan_base = "https://api.bscscan.com/api"
        self._binance_base = "https://api.binance.com/api/v3"
        self._hop_api = "https://api.hop.exchange/v1"
        self._synapse_api = "https://api.synapseprotocol.com"
        self._blockscout_base = "https://base.blockscout.com/api/v2"

        self._subgraphs = {
            "uniswap": {
                "ethereum": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
                "arbitrum": "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-arbitrum-one",
                "optimism": "https://api.thegraph.com/subgraphs/name/ianlapham/optimism-post-regenesis",
                "polygon": "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-polygon",
                "base": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3-base",
                "zksync": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3-zksync"
            },
            "sushiswap": {
                "ethereum": "https://api.thegraph.com/subgraphs/name/sushiswap/exchange",
                "arbitrum": "https://api.thegraph.com/subgraphs/name/sushiswap/arbitrum-exchange",
                "optimism": "https://api.thegraph.com/subgraphs/name/sushiswap/optimism-exchange",
                "polygon": "https://api.thegraph.com/subgraphs/name/sushiswap/matic-exchange"
            },
            "curve": {
                "ethereum": "https://api.thegraph.com/subgraphs/name/curvefi/curve",
                "arbitrum": "https://api.thegraph.com/subgraphs/name/curvefi/curve-arbitrum",
                "polygon": "https://api.thegraph.com/subgraphs/name/curvefi/curve-polygon",
            },
            "pancakeswap": {
                "bsc": "https://api.thegraph.com/subgraphs/name/pancakeswap/exchange-v2",
            }
        }

        self._token_addresses = {
            "ethereum": {
                "ETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
                "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
                "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
                "STETH": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
                "RETH": "0xae78736cd615f374d3085123a210448e74fc6393",
                "CBETH": "0xbe9895146f7af43049ca1c1ae358b0541ea49704",
                "ANKRETH": "0xe95a203b1a91a908f9b9ce46459d101078c2c3cb",
                "MATIC": "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0"
            },
            "arbitrum": {
                "ETH": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
                "USDC": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                "STETH": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
                "RETH": "0xec70dcb4a1efa46b8f2d97c310c9c4790ba5ffa8",
                "CBETH": "0x1debd73e752beaf79865fd6446b0c970eae7732f",
                "ARB": "0x912ce59144191c1204e64559fe8253a0e49e6548"
            },
            "optimism": {
                "ETH": "0x4200000000000000000000000000000000000006",
                "USDC": "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
                "STETH": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
                "RETH": "0x9bcef72be871e61ed4fbbc7630889bee758eb81d",
                "CBETH": "0xad3eab4c5b1ad6c77bd78f4d36a1c1f2ed9bb30b",
                "OP": "0x4200000000000000000000000000000000000042"
            },
            "polygon": {
                "MATIC": "0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270",
                "USDC": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                "ETH": "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",
                "STETH": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
                "RETH": "0x9bcef72be871e61ed4fbbc7630889bee758eb81d",
                "CBETH": "0xad3eab4c5b1ad6c77bd78f4d36a1c1f2ed9bb30b"
            },
            "base": {
                "ETH": "0x4200000000000000000000000000000000000006",
                "USDC": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
            },
            "zksync": {
                "ETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
                "USDC": "0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4"
            },
            "bsc": {
                "BNB": "0xb8c77482e45f1f44de1745f52c74426c631bdd52",
                "USDC": "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d",
                "USDT": "0x55d398326f99059ff775485246999027b3197955",
                "CAKE": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
                "WBNB": "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
            }
        }

        self._native_tokens = {
            "ethereum": "ETH", "arbitrum": "ETH", "optimism": "ETH", "polygon": "MATIC",
            "base": "ETH", "zksync": "ETH", "bsc": "BNB", "solana": "SOL"
        }

        self._gas_token_addresses = {
            "ethereum": "0x0000000000004946c0e9f43f4dee607b0ef1fa1c",
            "bsc": "", "solana": ""
        }
        self._gas_token_symbols = {
            "0x0000000000004946c0e9f43f4dee607b0ef1fa1c": "CHI",
        }

    async def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _cleanup_last_valid(self):
        async with self._lock:
            now = time.time()
            if now - self._last_cleanup < self._cleanup_interval: return
            self._last_cleanup = now
            old_keys = [k for k, ts in self._last_valid_timestamps.items() if now - ts > 86400]
            for k in old_keys:
                self._last_valid.pop(k, None)
                self._last_valid_timestamps.pop(k, None)
            if len(self._last_valid) > self._last_valid_maxsize:
                sorted_keys = sorted(self._last_valid_timestamps.items(), key=lambda x: x[1])
                remove_count = len(self._last_valid) - self._last_valid_maxsize
                for k, _ in sorted_keys[:remove_count]:
                    self._last_valid.pop(k, None)
                    self._last_valid_timestamps.pop(k, None)

    def _token_to_coingecko_id(self, token: str) -> Optional[str]:
        mapping = {
            "ETH": "ethereum", "BTC": "bitcoin", "USDC": "usd-coin", "USDT": "tether",
            "DAI": "dai", "STETH": "staked-ether", "RETH": "rocket-pool-eth",
            "CBETH": "coinbase-wrapped-staked-eth", "UNI": "uniswap", "AAVE": "aave",
            "COMP": "compound-governance-token", "LINK": "chainlink", "MATIC": "matic-network",
            "ARB": "arbitrum", "OP": "optimism", "ANKRETH": "ankreth", "BNB": "binancecoin",
            "CHI": "chi-gastoken", "CAKE": "pancakeswap-token", "SOL": "solana"
        }
        return mapping.get(token.upper())

    async def _get_solana_connector(self) -> Optional[SolanaConnector]:
        if not SOLANA_AVAILABLE: return None
        if self._solana is None: self._solana = SolanaConnector()
        return self._solana

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_price(self, token: str, chain: str, max_age_seconds: int = 300) -> float:
        cache_key = f"price:{token}:{chain}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached

        if chain.lower() == "solana":
            sol = await self._get_solana_connector()
            if sol:
                try:
                    price = await sol.get_price(token)
                    if price > 0:
                        await self._cache.set(cache_key, price, ttl=30)
                        async with self._lock:
                            self._last_valid[cache_key] = price
                            self._last_valid_timestamps[cache_key] = time.time()
                            await self._cleanup_last_valid()
                        return price
                except NotImplementedError: pass
            cg_id = self._token_to_coingecko_id(token)
            if cg_id:
                async with await self._get_session() as session:
                    try:
                        url = f"{self._coingecko_base}/simple/price?ids={cg_id}&vs_currencies=usd"
                        async with session.get(url) as resp:
                            data = await resp.json()
                            price = float(data.get(cg_id, {}).get('usd', 0))
                            if price > 0:
                                await self._cache.set(cache_key, price, ttl=30)
                                async with self._lock:
                                    self._last_valid[cache_key] = price
                                    self._last_valid_timestamps[cache_key] = time.time()
                                    await self._cleanup_last_valid()
                                return price
                    except Exception as e: logger.warning(f"CoinGecko price failed for {token} on {chain}: {e}")

        prices = []
        weights = []
        cg_id = self._token_to_coingecko_id(token)

        async with await self._get_session() as session:
            if cg_id:
                try:
                    url = f"{self._defillama_base}/prices/current/{cg_id}"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            price = float(data.get('coins', {}).get(cg_id, {}).get('price', 0))
                            if price > 0:
                                prices.append(price); weights.append(0.6)
                except Exception as e: logger.warning(f"DefiLlama price failed for {token} on {chain}: {e}")

            if cg_id:
                try:
                    url = f"{self._coingecko_base}/simple/price?ids={cg_id}&vs_currencies=usd"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        price = float(data.get(cg_id, {}).get('usd', 0))
                        if price > 0:
                            prices.append(price); weights.append(0.3)
                except Exception as e: logger.warning(f"CoinGecko price failed for {token} on {chain}: {e}")

            for dex in ["uniswap", "sushiswap", "curve", "pancakeswap"]:
                if chain in self._subgraphs.get(dex, {}):
                    try:
                        token_addr = self._token_addresses.get(chain, {}).get(token.upper())
                        usdc_addr = self._token_addresses.get(chain, {}).get("USDC")
                        if token_addr and usdc_addr:
                            query = f"""
                            {{
                              pools(where: {{token0: "{token_addr}", token1: "{usdc_addr}"}}) {{
                                token0Price
                              }}
                            }}
                            """
                            async with session.post(self._subgraphs[dex][chain], json={'query': query}) as resp:
                                data = await resp.json()
                                pools = data.get('data', {}).get('pools', [])
                                if pools:
                                    price = float(pools[0]['token0Price'])
                                    if price > 0:
                                        prices.append(price); weights.append(0.5)
                                        break
                    except Exception as e: logger.warning(f"The Graph price failed for {dex} on {chain}: {e}")

        if prices:
            total_weight = sum(weights)
            weighted_price = sum(p * w for p, w in zip(prices, weights)) / total_weight if total_weight > 0 else sum(prices)/len(prices)
            weighted_price = round(weighted_price, 2)
            await self._cache.set(cache_key, weighted_price, ttl=30)
            async with self._lock:
                self._last_valid[cache_key] = weighted_price
                self._last_valid_timestamps[cache_key] = time.time()
                await self._cleanup_last_valid()
            return weighted_price

        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"Price for {token} on {chain} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid

        raise DataUnavailableError(f"Price for {token} on {chain} not available from any source.")

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_volume(self, token: str, chain: str, max_age_seconds: int = 600) -> float:
        cache_key = f"volume:{token}:{chain}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached

        volume = None
        async with await self._get_session() as session:
            if chain in self._subgraphs["uniswap"]:
                token_addr = self._token_addresses.get(chain, {}).get(token.upper())
                if token_addr:
                    query = f"""
                    {{
                      tokenDayDatas(first: 1, orderBy: date, orderDirection: desc, where: {{token: "{token_addr}"}}) {{
                        volumeUSD
                      }}
                    }}
                    """
                    try:
                        async with session.post(self._subgraphs["uniswap"][chain], json={'query': query}) as resp:
                            data = await resp.json()
                            vol_data = data.get('data', {}).get('tokenDayDatas', [])
                            if vol_data: volume = float(vol_data[0]['volumeUSD'])
                    except Exception as e: logger.warning(f"The Graph volume failed for {token} on {chain}: {e}")

            if not volume:
                try:
                    url = f"{self._defillama_base}/summary/dexes/{chain}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        for item in data.get('tokens', []):
                            if item.get('symbol') == token.upper():
                                volume = float(item.get('volume', 0))
                                break
                except Exception as e: logger.warning(f"DefiLlama volume failed: {e}")

            if not volume:
                cg_id = self._token_to_coingecko_id(token)
                if cg_id:
                    try:
                        url = f"{self._coingecko_base}/coins/{cg_id}"
                        async with session.get(url) as resp:
                            data = await resp.json()
                            volume = float(data.get('market_data', {}).get('total_volume', {}).get('usd', 0))
                    except Exception as e: logger.warning(f"CoinGecko volume failed: {e}")

        if volume is not None and volume > 0:
            await self._cache.set(cache_key, volume, ttl=300)
            async with self._lock:
                self._last_valid[cache_key] = volume
                self._last_valid_timestamps[cache_key] = time.time()
                await self._cleanup_last_valid()
            return volume

        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"Volume for {token} on {chain} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid

        raise DataUnavailableError(f"Volume for {token} on {chain} not available.")

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_gas_price(self, chain: str, max_age_seconds: int = 120) -> float:
        cache_key = f"gas:{chain}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached

        gas = None
        api_key = None
        base_url = None
        if chain == "ethereum":
            api_key = os.environ.get("ETHERSCAN_API_KEY"); base_url = self._etherscan_base
        elif chain == "arbitrum":
            api_key = os.environ.get("ARBISCAN_API_KEY"); base_url = self._arbiscan_base
        elif chain == "optimism":
            api_key = os.environ.get("OPTIMISMSCAN_API_KEY"); base_url = self._optimismscan_base
        elif chain == "polygon":
            api_key = os.environ.get("POLYGONSCAN_API_KEY"); base_url = self._polygonscan_base
        elif chain == "bsc":
            api_key = os.environ.get("BSCSCAN_API_KEY"); base_url = self._bscscan_base
        elif chain == "base":
            try:
                async with await self._get_session() as session:
                    url = f"{self._blockscout_base}/gas-price"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if 'result' in data:
                            gas = float(data['result']['fast']) / 1e9
                            gas = min(gas, 1000)
                            await self._cache.set(cache_key, gas, ttl=60)
                            async with self._lock:
                                self._last_valid[cache_key] = gas
                                self._last_valid_timestamps[cache_key] = time.time()
                                await self._cleanup_last_valid()
                            return gas
            except Exception as e: logger.warning(f"Base gas fetch failed: {e}")
            fallback = 0.05; logger.warning(f"Using fallback gas price for base: {fallback}"); return fallback
        elif chain == "zksync":
            fallback = 0.1; logger.warning(f"No gas oracle for zksync, using fallback {fallback}"); return fallback
        elif chain == "solana":
            return 0.0
        else:
            fallback = 30; logger.warning(f"No gas oracle for {chain}, using fallback {fallback}"); return fallback

        if api_key and base_url:
            async with await self._get_session() as session:
                try:
                    url = f"{base_url}?module=gastracker&action=gasoracle&apikey={api_key}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if data.get('status') == '1':
                            gas = float(data.get('result', {}).get('FastGasPrice', 0))
                except Exception as e: logger.warning(f"Gas oracle failed for {chain}: {e}")

        if gas is not None and gas > 0:
            gas = min(gas, 1000)
            await self._cache.set(cache_key, gas, ttl=60)
            async with self._lock:
                self._last_valid[cache_key] = gas
                self._last_valid_timestamps[cache_key] = time.time()
                await self._cleanup_last_valid()
            return gas

        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"Gas price for {chain} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid

        fallback = {"ethereum":30, "arbitrum":0.5, "optimism":0.5, "base":0.05, "polygon":30, "zksync":0.1, "bsc":5}.get(chain, 10)
        logger.warning(f"Gas price for {chain} not available, using fallback {fallback}")
        return fallback

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_apy(self, protocol: str, max_age_seconds: int = 3600) -> float:
        cache_key = f"apy:{protocol}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached

        apy = None
        async with await self._get_session() as session:
            if protocol == "aave":
                try:
                    url = "https://aave-api.vercel.app/api/reserve-data"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        for reserve in data.get('reserves', []):
                            if reserve.get('symbol') == 'ETH':
                                apy = float(reserve.get('liquidityRate', 0)) / 100
                                break
                except Exception as e: logger.warning(f"Aave APY failed: {e}")
            elif protocol == "compound":
                try:
                    url = "https://api.compound.finance/api/v2/ctoken"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        for ctoken in data.get('cToken', []):
                            if ctoken.get('symbol') == 'cETH':
                                apy = float(ctoken.get('supply_rate', 0)) * 100
                                break
                except Exception as e: logger.warning(f"Compound APY failed: {e}")
            elif protocol in ["uniswap", "curve"]:
                try:
                    url = f"{self._defillama_base}/yields?project={protocol}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        for pool in data:
                            symbol = pool.get('symbol', '')
                            if ('ETH' in symbol and 'USDC' in symbol) or (protocol == "uniswap" and 'ETH' in symbol):
                                if pool.get('chain') == 'Ethereum':
                                    apy = float(pool.get('apy', 0))
                                    break
                except Exception as e: logger.warning(f"{protocol} APY failed: {e}")

        if apy is not None and apy > 0:
            await self._cache.set(cache_key, apy, ttl=3600)
            async with self._lock:
                self._last_valid[cache_key] = apy
                self._last_valid_timestamps[cache_key] = time.time()
                await self._cleanup_last_valid()
            return apy

        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"APY for {protocol} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid

        raise DataUnavailableError(f"APY for {protocol} not available.")

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_nft_price(self, collection: str, marketplace: str, max_age_seconds: int = 300) -> float:
        cache_key = f"nft_price:{collection}:{marketplace}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached

        price = None
        api_key = os.environ.get("OPENSEA_API_KEY")
        if api_key:
            async with await self._get_session() as session:
                try:
                    url = f"{self._opensea_base}/collection/{collection}/stats"
                    headers = {"X-API-KEY": api_key}
                    async with session.get(url, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            price = float(data.get('stats', {}).get('floor_price', 0))
                except Exception as e: logger.warning(f"OpenSea price failed: {e}")

        if not price:
            blur_key = os.environ.get("BLUR_API_KEY")
            if blur_key:
                try:
                    async with await self._get_session() as session:
                        url = f"{self._blur_base}/collection/{collection}/floor"
                        headers = {"Authorization": f"Bearer {blur_key}"}
                        async with session.get(url, headers=headers) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                price = float(data.get('floor_price', 0))
                except Exception as e: logger.warning(f"Blur price failed: {e}")

        if price is not None and price > 0:
            await self._cache.set(cache_key, price, ttl=60)
            async with self._lock:
                self._last_valid[cache_key] = price
                self._last_valid_timestamps[cache_key] = time.time()
                await self._cleanup_last_valid()
            return price

        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"NFT price for {collection} on {marketplace} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid

        raise DataUnavailableError(f"NFT price for {collection} on {marketplace} not available.")

    async def get_nft_mint_time(self, collection: str, token_id: str) -> float:
        cache_key = f"nft_mint:{collection}:{token_id}"
        cached = await self._cache.get(cache_key)
        if cached: return cached
        api_key = os.environ.get("OPENSEA_API_KEY")
        if api_key:
            async with await self._get_session() as session:
                try:
                    url = f"{self._opensea_base}/asset/{collection}/{token_id}"
                    headers = {"X-API-KEY": api_key}
                    async with session.get(url, headers=headers) as resp:
                        data = await resp.json()
                        mint_time = data.get('asset_contract', {}).get('created_date')
                        if mint_time:
                            ts = time.mktime(time.strptime(mint_time, "%Y-%m-%dT%H:%M:%S.%fZ"))
                            await self._cache.set(cache_key, ts, ttl=86400)
                            async with self._lock:
                                self._last_valid[cache_key] = ts
                                self._last_valid_timestamps[cache_key] = time.time()
                                await self._cleanup_last_valid()
                            return ts
                except Exception as e: logger.warning(f"OpenSea mint time failed: {e}")
        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            if last_valid is not None: return last_valid
        return time.time()

    async def get_nft_transfers(self, collection: str, token_id: str) -> List[Dict]:
        cache_key = f"nft_transfers:{collection}:{token_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        api_key = os.environ.get("OPENSEA_API_KEY")
        if api_key:
            async with await self._get_session() as session:
                try:
                    url = f"{self._opensea_base}/events"
                    params = {"asset_contract_address": collection, "token_id": token_id, "event_type": "transfer"}
                    headers = {"X-API-KEY": api_key}
                    async with session.get(url, headers=headers, params=params) as resp:
                        data = await resp.json()
                        events = data.get('asset_events', [])
                        await self._cache.set(cache_key, events, ttl=3600)
                        async with self._lock:
                            self._last_valid[cache_key] = events
                            self._last_valid_timestamps[cache_key] = time.time()
                            await self._cleanup_last_valid()
                        return events
                except Exception as e: logger.warning(f"OpenSea transfers failed: {e}")
        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            if last_valid is not None: return last_valid
        return []

    async def get_nft_last_sale(self, collection: str, token_id: str) -> Dict:
        cache_key = f"nft_last_sale:{collection}:{token_id}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        api_key = os.environ.get("OPENSEA_API_KEY")
        if api_key:
            async with await self._get_session() as session:
                try:
                    url = f"{self._opensea_base}/events"
                    params = {"asset_contract_address": collection, "token_id": token_id, "event_type": "successful"}
                    headers = {"X-API-KEY": api_key}
                    async with session.get(url, headers=headers, params=params) as resp:
                        data = await resp.json()
                        events = data.get('asset_events', [])
                        if events:
                            result = {"price": float(events[0].get('total_price', 0)) / 1e18}
                        else:
                            result = {"price": 0.0}
                        await self._cache.set(cache_key, result, ttl=3600)
                        async with self._lock:
                            self._last_valid[cache_key] = result
                            self._last_valid_timestamps[cache_key] = time.time()
                            await self._cleanup_last_valid()
                        return result
                except Exception as e: logger.warning(f"OpenSea last sale failed: {e}")
        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            if last_valid is not None: return last_valid
        return {"price": 0.0}

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_transactions(self, address: str, limit: int = 5000, page: int = 1) -> List[Dict]:
        cache_key = f"tx:{address}:{limit}:{page}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        api_key = os.environ.get("ETHERSCAN_API_KEY")
        if not api_key: raise DataUnavailableError("ETHERSCAN_API_KEY not set")
        async with await self._get_session() as session:
            try:
                url = f"{self._etherscan_base}?module=account&action=txlist&address={address}&page={page}&offset={limit}&sort=desc&apikey={api_key}"
                async with session.get(url) as resp:
                    data = await resp.json()
                    if data.get('status') == '1':
                        txs = data.get('result', [])
                        await self._cache.set(cache_key, txs, ttl=300)
                        async with self._lock:
                            self._last_valid[cache_key] = txs
                            self._last_valid_timestamps[cache_key] = time.time()
                            await self._cleanup_last_valid()
                        return txs
                    else:
                        raise DataUnavailableError(f"Etherscan error: {data.get('message', 'Unknown')}")
            except Exception as e: logger.warning(f"Etherscan transactions failed: {e}"); raise

    async def get_all_transactions(self, address: str, days: int = 30, max_pages: int = 50) -> Tuple[List[Dict], float]:
        all_txs = []
        page = 1
        limit = 10000
        now = time.time()
        cutoff = now - (days * 86400)
        total_volume = 0.0
        pages_fetched = 0
        while pages_fetched < max_pages:
            txs = await self.get_transactions(address, limit, page)
            if not txs: break
            for tx in txs:
                if int(tx.get('timeStamp', 0)) >= cutoff:
                    all_txs.append(tx)
                    try:
                        val = safe_int(tx.get('value', 0)) / 1e18
                        total_volume += val
                    except: pass
            pages_fetched += 1
            if len(txs) < limit: break
            page += 1
        logger.info(f"Fetched {len(all_txs)} transactions for {address} across {pages_fetched} pages, total volume {total_volume:.2f} ETH")
        return all_txs, total_volume

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_new_contracts(self, since: Optional[int] = None, max_pages: int = 10) -> List[Dict]:
        cache_key = f"new_contracts:{since or 'latest'}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        api_key = os.environ.get("ETHERSCAN_API_KEY")
        if not api_key: raise DataUnavailableError("ETHERSCAN_API_KEY not set")
        if since is None: since = int(time.time()) - 600
        all_contracts = []
        page = 1
        offset = 1000
        pages_fetched = 0
        while pages_fetched < max_pages:
            async with await self._get_session() as session:
                try:
                    url = f"{self._etherscan_base}?module=contract&action=getcontractcreation&apikey={api_key}&page={page}&offset={offset}&sort=desc"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if data.get('status') != '1': break
                        contracts = data.get('result', [])
                        if not contracts: break
                        filtered = [c for c in contracts if int(c.get('timestamp', 0)) > since]
                        all_contracts.extend(filtered)
                        if len(contracts) < offset: break
                        page += 1; pages_fetched += 1
                except Exception as e: logger.warning(f"Etherscan new contracts fetch failed: {e}"); break
        await self._cache.set(cache_key, all_contracts, ttl=60)
        async with self._lock:
            self._last_valid[cache_key] = all_contracts
            self._last_valid_timestamps[cache_key] = time.time()
            await self._cleanup_last_valid()
        return all_contracts

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_cex_price(self, cex: str, token: str, max_age_seconds: int = 30) -> float:
        cache_key = f"cex:{cex}:{token}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        async with await self._get_session() as session:
            try:
                if cex == "binance":
                    symbol = f"{token.upper()}USDT"
                    url = f"{self._binance_base}/ticker/price?symbol={symbol}"
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            price = float(data.get('price', 0))
                            if price > 0:
                                await self._cache.set(cache_key, price, ttl=10)
                                async with self._lock:
                                    self._last_valid[cache_key] = price
                                    self._last_valid_timestamps[cache_key] = time.time()
                                    await self._cleanup_last_valid()
                                return price
                elif cex == "coinbase":
                    url = f"https://api.coinbase.com/v2/prices/{token.upper()}-USD/spot"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        price = float(data.get('data', {}).get('amount', 0))
                        if price > 0:
                            await self._cache.set(cache_key, price, ttl=10)
                            async with self._lock:
                                self._last_valid[cache_key] = price
                                self._last_valid_timestamps[cache_key] = time.time()
                                await self._cleanup_last_valid()
                            return price
                elif cex == "kraken":
                    kraken_pairs = {"ETH": "XETHZUSD","BTC": "XXBTZUSD","USDC": "USDCUSD","USDT": "USDTUSD","DAI": "DAIUSD"}
                    pair = kraken_pairs.get(token.upper(), f"{token.upper()}USD")
                    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if 'result' in data and pair in data['result']:
                            price = float(data['result'][pair].get('c', [0])[0])
                            if price > 0:
                                await self._cache.set(cache_key, price, ttl=10)
                                async with self._lock:
                                    self._last_valid[cache_key] = price
                                    self._last_valid_timestamps[cache_key] = time.time()
                                    await self._cleanup_last_valid()
                                return price
            except Exception as e: logger.warning(f"CEX price fetch for {cex} failed: {e}")
        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"CEX price for {cex} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid
        raise DataUnavailableError(f"CEX price for {cex} not available")

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_dex_price(self, dex: str, token: str, chain: str = "ethereum", quote_token: str = "USDC", tried: set = None, depth: int = 0) -> float:
        if depth > 5: raise DataUnavailableError(f"Max recursion depth exceeded for {dex}/{token} on {chain}")
        if tried is None: tried = set()
        tried.add(quote_token)
        cache_key = f"dex:{dex}:{token}:{chain}:{quote_token}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached

        if dex.lower() not in self._subgraphs or chain not in self._subgraphs[dex.lower()]:
            raise DataUnavailableError(f"DEX {dex} not supported for chain {chain}")

        token_addr = self._token_addresses.get(chain, {}).get(token.upper())
        quote_addr = self._token_addresses.get(chain, {}).get(quote_token.upper())
        if not token_addr or not quote_addr:
            possible_quotes = ["USDC", "ETH", "WETH", "DAI", "USDT"]
            for q in possible_quotes:
                if q not in tried:
                    return await self.get_dex_price(dex, token, chain, q, tried, depth + 1)
            raise DataUnavailableError(f"No token address for {token} or quote token on {chain}")

        query = f"""
        {{
          pools(where: {{token0: "{token_addr}", token1: "{quote_addr}"}}) {{
            token0Price
          }}
        }}
        """
        async with await self._get_session() as session:
            try:
                async with session.post(self._subgraphs[dex.lower()][chain], json={'query': query}) as resp:
                    data = await resp.json()
                    pools = data.get('data', {}).get('pools', [])
                    if pools:
                        price = float(pools[0]['token0Price'])
                        if price > 0:
                            await self._cache.set(cache_key, price, ttl=30)
                            async with self._lock:
                                self._last_valid[cache_key] = price
                                self._last_valid_timestamps[cache_key] = time.time()
                                await self._cleanup_last_valid()
                            return price
            except Exception as e: logger.warning(f"The Graph price for {dex} failed: {e}")

        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            if last_valid is not None:
                logger.warning(f"DEX price for {dex} not available. Using last valid")
                return last_valid

        raise DataUnavailableError(f"DEX price for {dex} not available")

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_bridge_fee(self, bridge: str, from_chain: str, to_chain: str, max_age_seconds: int = 600) -> float:
        cache_key = f"bridge_fee:{bridge}:{from_chain}:{to_chain}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        fee = None
        async with await self._get_session() as session:
            if bridge == "hop":
                try:
                    url = f"{self._hop_api}/fees?from={from_chain}&to={to_chain}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        fee = float(data.get('fee', 0))
                except Exception as e: logger.warning(f"Hop fee failed: {e}")
            elif bridge == "synapse":
                try:
                    url = f"{self._synapse_api}/fees?from={from_chain}&to={to_chain}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        fee = float(data.get('fee', 0))
                except Exception as e: logger.warning(f"Synapse fee failed: {e}")
        if fee is not None:
            await self._cache.set(cache_key, fee, ttl=60)
            async with self._lock:
                self._last_valid[cache_key] = fee
                self._last_valid_timestamps[cache_key] = time.time()
                await self._cleanup_last_valid()
            return fee
        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"Bridge fee for {bridge} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid
        default_fee = {"hop":2.5, "synapse":2.0}.get(bridge, 2.0)
        logger.warning(f"Bridge fee for {bridge} not available, using default {default_fee}")
        return default_fee

    @retry_async(max_attempts=3, retry_on=(aiohttp.ClientError, asyncio.TimeoutError))
    async def get_funding_rate(self, exchange: str, symbol: str = "ETHUSDT", max_age_seconds: int = 120) -> Optional[float]:
        cache_key = f"funding:{exchange}:{symbol}"
        cached = await self._cache.get(cache_key)
        if cached is not None: return cached
        async with await self._get_session() as session:
            try:
                if exchange == "binance":
                    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        for item in data:
                            if item.get('symbol') == symbol.upper():
                                rate = float(item.get('lastFundingRate', 0))
                                await self._cache.set(cache_key, rate, ttl=60)
                                async with self._lock:
                                    self._last_valid[cache_key] = rate
                                    self._last_valid_timestamps[cache_key] = time.time()
                                    await self._cleanup_last_valid()
                                return rate
                elif exchange == "bybit":
                    url = f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={symbol.upper()}"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        rate = float(data.get('result', {}).get('list', [{}])[0].get('fundingRate', 0))
                        await self._cache.set(cache_key, rate, ttl=60)
                        async with self._lock:
                            self._last_valid[cache_key] = rate
                            self._last_valid_timestamps[cache_key] = time.time()
                            await self._cleanup_last_valid()
                        return rate
            except Exception as e: logger.warning(f"Funding rate fetch for {exchange} failed: {e}")
        async with self._lock:
            last_valid = self._last_valid.get(cache_key)
            last_ts = self._last_valid_timestamps.get(cache_key, 0)
            if last_valid is not None and (time.time() - last_ts) <= max_age_seconds:
                logger.warning(f"Funding rate for {exchange} not available. Using last valid from {time.ctime(last_ts)}")
                return last_valid
        return None

    async def get_whale_volume(self, address: str, days: int = 30) -> float:
        _, volume = await self.get_all_transactions(address, days)
        return volume

    @retry_async(max_attempts=3, retry_on=(Exception,))
    async def deploy_contract(self, source: str, chain: str, pri
