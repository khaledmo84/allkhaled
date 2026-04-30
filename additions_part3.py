#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ÅÖÇÝÇÊ - ÇáÌÒÁ ÇáËÇáË (ÇáäÙÇã ÇáãæÒÚ ÇáãÊÞÏã + ÇáäÙÇã ÇáãæÍÏ)
================================================================================
ÇáãíÒÇÊ ÇáÌÏíÏÉ Ýí åÐÇ ÇáÌÒÁ (ÛíÑ ÇáãæÌæÏÉ Ýí core/agents/unified/thinking_core/tests):
--------------------------------------------------------------------------------
1. DigitalIdentity (ECDSA): åæíÉ ÑÞãíÉ ÞæíÉ ãÚ ÊæÞíÚ æÊÍÞÞ.
2. KnowledgeRepository: ãÓÊæÏÚ ãÚÑÝÉ ÈÊÖãíäÇÊ TfidfVectorizer ááÈÍË ÇáÏáÇáí.
3. TrustNetwork: ÔÈßÉ ËÞÉ ãæÒÚÉ ãÚ ÓÌá ÚÞÏ (NodeRegistry) ÚÈÑ Redis.
4. MarketRegimeDetector: ßÇÔÝ äãØ ÇáÓæÞ (high_volatility, bull, bear, sideways).
5. MarketAdapter: ÊßíÝ ÇÓÊÑÇÊíÌíÇÊ ãÚ ÙÑæÝ ÇáÓæÞ.
6. StoryManager: ÅÏÇÑÉ ÞÕÕ ÝÔá æÊÍáíáåÇ.
7. IntelligentTradingAgent: æßíá ÊÏÇæá Ðßí íÊÚáã ãä ÇáÞÕÕ æíÊßíÝ ãÚ ÇáÓæÞ.
8. DistributedTradingSystem: äÙÇã ãæÒÚ íÏíÑ ÚÏÏÇð ÏíäÇãíßíÇð ãä ÇáæßáÇÁ.
9. AlKhaledUltimateOrchestrator: ÇáäÙÇã ÇáãæÍÏ ÇáÐí íÏãÌ ßá ÇáãßæäÇÊ ãä ÇáÃÌÒÇÁ ÇáËáÇËÉ.
10. ÏÇáÉ inject_all: ÍÞä ÌãíÚ ÇáÅÖÇÝÇÊ Ýí AlKhaledUltimateAgent.
11. æËÇÆÞ áßá ßáÇÓ æÏÇáÉ ãÚ ÃãËáÉ ÇÓÊÎÏÇã.
================================================================================
"""

import asyncio
import aiohttp
import aiosqlite
import json
import os
import sys
import time
import hashlib
import hmac
import secrets
import random
import pickle
import sqlite3
import signal
import inspect
from typing import Dict, List, Optional, Any, Tuple, Callable, Union, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque
import logging
import uuid
import numpy as np
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import redis.asyncio as redis

# ÇÓÊíÑÇÏ ÇáãßæäÇÊ ãä core (Åä æÌÏÊ)
try:
    from core import (
        Config, ExperienceDB, SmartCache, KeyManager, GodPulse,
        GasManager, CircuitBreaker, RiskManager, Opportunity as CoreOpportunity,
        StrategyCategory, BaseAgent as CoreBaseAgent, validate_ethereum_address,
        time_now_ns, gas_cost_usd, retry as core_retry, smart_retry,
        AESGCMEncryptor, SecureRedis, SUPPORTED_CHAINS,
        RPCManager, QuantumManager, MarketData, TradeRecord
    )
    from agents import AgentOrchestrator, PreflightSimulator, ContractDeployerAgent
    from unified import AlKhaledUltimateAgent, MempoolWatcher
    from thinking_core import ThinkingCore
    CORE_AVAILABLE = True
    logger = logging.getLogger('AdditionsPart3')
except ImportError as e:
    CORE_AVAILABLE = False
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('AdditionsPart3')
    logger.warning(f"?? ÇáãßæäÇÊ ÇáÃÓÇÓíÉ ÛíÑ ãÊæÝÑÉ: {e}")

# ÇÓÊíÑÇÏ ãä ÇáÃÌÒÇÁ ÇáÓÇÈÞÉ
try:
    from additions_part1 import (
        exponential_backoff, compress_zstd, decompress_zstd, with_retry,
        AutoStrategyAdvisor, NeuralEarlyWarningSystem, AdaptiveGasWall, SelfHealingContractGuardian,
        RPCManagerExtended, DeploymentPlatformManager,
        AdvancedBackupSystem, PreDeploymentTester, NodeDiscovery, PerformanceEvaluator,
        CloudCostMonitor, DefiLlamaClient, DuneClient, SelfUpdater, TerminationManager,
        PluginLoader, KeyRotationManager, MultiSigManager, TemporaryWalletManager
    )
    from additions_part2 import (
        CloudManager, DeploymentAgent, LiquidInfrastructureAgent, DecentralizedStorage,
        EdgeNetwork, StealthManager, SmartScheduler, TerraformIntegration,
        WalletGeneratorAgent, SignatureOpportunityAgent, ZeroWalletAgent,
        BlockchainConnector, BaseAgent as EthicalBaseAgent,
        DormantContractAgent, BridgeDustAgent, GovernanceRewardsAgent, LiquiditySweepAgent,
        BugBountyAgent, MEVProtectorAgent, ArbitrageAgent, TimeSeriesAgent,
        FlashblocksAgent, WhiteHatMediatorAgent, V2LiquiditySnipingAgent,
        BountyContractsAgent, SafeAirdropAgent, RelayContractsAgent,
        PancakeOldPoolsAgent, OldGovernanceAgent, UnclaimedBridgeAgent,
        V1LiquidityAgent, ExpiredGovernanceRewardsAgent, DustHuntingAgent,
        VulnerabilityReportingAgent, SmartContractWriterAgent, SecurityAuditorAgent,
        SolverAgent, FrontrunProtectorAgent, MempoolWatcherAgent,
        GasOptimizerAgent, ComplianceAgent, ReportingAgent
    )
    PART1_AVAILABLE = True
    PART2_AVAILABLE = True
except ImportError as e:
    PART1_AVAILABLE = False
    PART2_AVAILABLE = False
    logger.warning(f"?? ÇáÃÌÒÇÁ ÇáÓÇÈÞÉ ÛíÑ ãÊæÝÑÉ: {e}")

# =============================================================================
# ÅÚÏÇÏ ÇáÊÓÌíá (ãØÇÈÞ ááÃÌÒÇÁ ÇáÓÇÈÞÉ)
# =============================================================================
LOG_DIR = "logs"
BACKUP_DIR = "backups"
PLUGIN_DIR = "plugins"
for d in [LOG_DIR, BACKUP_DIR, PLUGIN_DIR]:
    os.makedirs(d, exist_ok=True)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        })

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'alkhaled.log')),
        logging.FileHandler(os.path.join(LOG_DIR, 'alkhaled.json'), mode='a'),
        logging.StreamHandler()
    ]
)
json_handler = logging.FileHandler(os.path.join(LOG_DIR, 'alkhaled.json'), mode='a')
json_handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(json_handler)
logger = logging.getLogger('AdditionsPart3')

# =============================================================================
# 1. ÇáäÙÇã ÇáãæÒÚ ÇáãÊÞÏã
# =============================================================================

class ConfigSettings:
    """ÅÚÏÇÏÇÊ ÇáäÙÇã ÇáãæÒÚ"""
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    DATABASE_DIR = os.getenv("DATABASE_DIR", "./data")
    API_PORT = int(os.getenv("API_PORT", 8080))
    NODE_REGISTRY_CHANNEL = "node_registry"
    OPPORTUNITY_CHANNEL = "opportunities"
    SECURITY_ALERTS_CHANNEL = "security_alerts"
    VOTING_CHANNEL = "voting"
    REPUTATION_DECAY = 0.99
    MIN_VOTES_FOR_BLACKLIST = 5
    VOTE_THRESHOLD = 0.6
    HEARTBEAT_INTERVAL = 30
    NODE_EXPIRY = 120

    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.DATABASE_DIR, exist_ok=True)

# 1.1 ÇáåæíÉ ÇáÑÞãíÉ (ECDSA)
class DigitalIdentity:
    """
    åæíÉ ÑÞãíÉ ÞæíÉ ÈÇÓÊÎÏÇã ECDSA (ãäÍäì secp256k1).
    ÊÊíÍ ÊæÞíÚ ÇáÑÓÇÆá æÇáÊÍÞÞ ãä ÇáÊæÞíÚÇÊ.
    """
    def __init__(self, node_id: str = None):
        self.node_id = node_id or str(uuid.uuid4())
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        self.created_at = datetime.utcnow()
        self.reputation = 1000.0
        self.trust_level = "NEW"
        self.successful_reports = 0
        self.failed_reports = 0

    def sign(self, message: str) -> str:
        """ÊæÞíÚ ÑÓÇáÉ"""
        signature = self.private_key.sign(
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    @staticmethod
    def verify(message: str, signature_hex: str, public_key_pem: str) -> bool:
        """ÇáÊÍÞÞ ãä ÇáÊæÞíÚ"""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode(),
                backend=default_backend()
            )
            signature = bytes.fromhex(signature_hex)
            public_key.verify(
                signature,
                message.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "public_key": self.public_key_pem,
            "created_at": self.created_at.isoformat(),
            "reputation": self.reputation,
            "trust_level": self.trust_level
        }

# 1.2 åíÇßá ÇáÈíÇäÇÊ ÇáÃÓÇÓíÉ
@dataclass
class Story:
    """ÞÕÉ ÊÚáíãíÉ ãÚ ÊÖãíä ááÈÍË ÇáÏáÇáí"""
    id: str
    timestamp: datetime
    agent_type: str
    title: str
    what_happened: str
    why_it_failed: str
    lesson_learned: str
    financial_impact: float
    market_regime: str
    tags: List[str]
    embedding: Optional[List[float]] = None  # ÓíÊã ÊæáíÏå áÇÍÞÇð

    def to_dict(self):
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        d["embedding"] = None
        return d

    def to_human_readable(self) -> str:
        return f"""
?? ÞÕÉ #{self.id}
?????????????????????????????????????
?? ÇáæÞÊ: {self.timestamp.strftime('%A, %d %B %Y ÇáÓÇÚÉ %I:%M %p')}
?? Çáæßíá: {self.agent_type}
?? ÇáÃËÑ ÇáãÇáí: ${self.financial_impact:,.2f}

?? {self.title}

?? ÇáÊÝÇÕíá:
{self.what_happened}

?? ÓÈÈ ÇáÝÔá:
{self.why_it_failed}

?? ÇáÏÑÓ ÇáãÓÊÝÇÏ:
{self.lesson_learned}

??? ÇáÊÕäíÝÇÊ: {', '.join(self.tags)}
?????????????????????????????????????
        """

@dataclass
class OpportunityMessage:
    """ÝÑÕÉ ÊÏÇæá ÊõäÔÑ ÚÈÑ ÇáÔÈßÉ"""
    id: str
    source_node: str
    signature: str
    protocol: str
    estimated_profit: float
    required_capital: float
    risk_score: float
    expiry: datetime
    details: Dict
    trust_votes: List[str] = field(default_factory=list)

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expiry

@dataclass
class SuspiciousContract:
    """ÚÞÏ ãÔÈæå ááÊÕæíÊ"""
    contract_address: str
    reported_by: str
    reason: str
    timestamp: datetime
    votes_yes: List[str] = field(default_factory=list)
    votes_no: List[str] = field(default_factory=list)
    is_blacklisted: bool = False

# 1.3 ãÓÊæÏÚ ÇáãÚÑÝÉ ÇáãÊÞÏã
class KnowledgeRepository:
    """
    ãÓÊæÏÚ ãÚÑÝÉ ÛíÑ ãÊÒÇãä ãÚ ÊÖãíä ÇáäÕæÕ (TfidfVectorizer).
    íÎÒä ÇáÞÕÕ æÇáÃäãÇØ Ýí SQLite.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.db_path = os.path.join(ConfigSettings.DATABASE_DIR, f"knowledge_{node_id}.db")
        self.vectorizer = TfidfVectorizer(max_features=128)
        self._embedding_cache = {}
        self._lock = asyncio.Lock()

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS stories (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    agent_type TEXT,
                    title TEXT,
                    what_happened TEXT,
                    why_it_failed TEXT,
                    lesson_learned TEXT,
                    financial_impact REAL,
                    market_regime TEXT,
                    tags TEXT,
                    embedding BLOB
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS patterns (
                    pattern_type TEXT PRIMARY KEY,
                    pattern_data TEXT,
                    confidence REAL,
                    occurrences INTEGER
                )
            ''')
            await db.commit()

    async def add_story(self, story: Story):
        """ÅÖÇÝÉ ÞÕÉ ÌÏíÏÉ ãÚ ÊæáíÏ ÇáÊÖãíä"""
        async with self._lock:
            text = f"{story.title} {story.what_happened} {story.why_it_failed} {story.lesson_learned}"
            if not self.vectorizer.vocabulary_:
                # ÊÏÑíÈ Ãæáí
                _ = self.vectorizer.fit_transform([text])
            embedding = self.vectorizer.transform([text]).toarray()[0].tolist()
            story.embedding = embedding

            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('''
                    INSERT OR REPLACE INTO stories
                    (id, timestamp, agent_type, title, what_happened, why_it_failed,
                     lesson_learned, financial_impact, market_regime, tags, embedding)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    story.id, story.timestamp.isoformat(), story.agent_type,
                    story.title, story.what_happened, story.why_it_failed,
                    story.lesson_learned, story.financial_impact,
                    story.market_regime, ','.join(story.tags),
                    pickle.dumps(embedding)
                ))
                await db.commit()

            # ÊÍÏíË ÇáÃäãÇØ
            await self._update_patterns(story)

    async def _update_patterns(self, story: Story):
        """ÊÍÏíË ÃäãÇØ ãÓÊÎáÕÉ ãä ÇáÞÕÉ"""
        # ÊÍáíá ÓÇÚÉ ÇáÝÔá
        hour = story.timestamp.hour
        if 2 <= hour <= 4:
            await self._increment_pattern("failure_hours", "02-04", story.financial_impact)

        # ÊÍáíá ÙÑæÝ ÇáÓæÞ
        if story.market_regime == "high_volatility":
            await self._increment_pattern("volatility_strategy", story.agent_type, story.financial_impact)

    async def _increment_pattern(self, pattern_type: str, value: str, impact: float):
        """ÒíÇÏÉ ÚÏÇÏ ÇáäãØ"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT pattern_data, confidence, occurrences FROM patterns WHERE pattern_type = ?",
                (pattern_type,)
            ) as cursor:
                row = await cursor.fetchone()

            if row:
                data = json.loads(row[0])
                data[value] = data.get(value, 0) + 1
                confidence = row[1] * 0.9 + (abs(impact) / 1000) * 0.1  # ÊÍÏíË ÇáËÞÉ
                occurrences = row[2] + 1
                await db.execute(
                    "UPDATE patterns SET pattern_data = ?, confidence = ?, occurrences = ? WHERE pattern_type = ?",
                    (json.dumps(data), confidence, occurrences, pattern_type)
                )
            else:
                data = {value: 1}
                await db.execute(
                    "INSERT INTO patterns (pattern_type, pattern_data, confidence, occurrences) VALUES (?, ?, ?, ?)",
                    (pattern_type, json.dumps(data), 0.5, 1)
                )
            await db.commit()

    async def get_similar_stories(self, query: Dict, limit: int = 5) -> List[Story]:
        """ÇáÈÍË Úä ÞÕÕ ãÔÇÈåÉ ÈÇÓÊÎÏÇã ÇáÊÖãíä æÇáäÕæÕ"""
        query_text = f"{query.get('agent_type', '')} {query.get('market_regime', '')}"
        if not self.vectorizer.vocabulary_:
            return []

        query_embedding = self.vectorizer.transform([query_text]).toarray()[0]

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT id, timestamp, agent_type, title, what_happened, why_it_failed, "
                "lesson_learned, financial_impact, market_regime, tags, embedding FROM stories"
            ) as cursor:
                rows = await cursor.fetchall()

            stories = []
            similarities = []
            for row in rows:
                embedding = pickle.loads(row[10])
                sim = cosine_similarity([query_embedding], [embedding])[0][0]
                similarities.append(sim)
                stories.append(Story(
                    id=row[0],
                    timestamp=datetime.fromisoformat(row[1]),
                    agent_type=row[2],
                    title=row[3],
                    what_happened=row[4],
                    why_it_failed=row[5],
                    lesson_learned=row[6],
                    financial_impact=row[7],
                    market_regime=row[8],
                    tags=row[9].split(',') if row[9] else [],
                    embedding=embedding
                ))

            # ÊÑÊíÈ ÍÓÈ ÇáÊÔÇÈå
            combined = list(zip(similarities, stories))
            combined.sort(key=lambda x: x[0], reverse=True)
            return [story for _, story in combined[:limit]]

# 1.4 ÓÌá ÇáÚÞÏ ÇáÏíäÇãíßí (NodeRegistry)
class NodeRegistry:
    """ÓÌá ÇáÚÞÏ ÇáÏíäÇãíßí ÈÇÓÊÎÏÇã Redis"""
    def __init__(self, redis_client: redis.Redis, identity: DigitalIdentity):
        self.redis = redis_client
        self.identity = identity
        self._heartbeat_task = None
        self._expiry_task = None

    async def register(self):
        """ÊÓÌíá ÇáÚÞÏÉ Ýí ÇáÔÈßÉ"""
        node_info = self.identity.to_dict()
        node_info["last_heartbeat"] = datetime.utcnow().isoformat()
        await self.redis.hset("nodes", self.identity.node_id, json.dumps(node_info))
        await self.redis.publish(ConfigSettings.NODE_REGISTRY_CHANNEL, json.dumps({
            "action": "register",
            "node": node_info
        }))

        # ÈÏÁ ÅÑÓÇá äÈÖÇÊ ÇáÞáÈ
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        self._expiry_task = asyncio.create_task(self._expiry_loop())

    async def unregister(self):
        """ÅáÛÇÁ ÊÓÌíá ÇáÚÞÏÉ"""
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self._expiry_task:
            self._expiry_task.cancel()

        await self.redis.hdel("nodes", self.identity.node_id)
        await self.redis.publish(ConfigSettings.NODE_REGISTRY_CHANNEL, json.dumps({
            "action": "unregister",
            "node_id": self.identity.node_id
        }))

    async def _heartbeat_loop(self):
        """ÅÑÓÇá äÈÖÇÊ ÇáÞáÈ ÈÔßá ÏæÑí"""
        while True:
            try:
                await asyncio.sleep(ConfigSettings.HEARTBEAT_INTERVAL)
                await self.redis.hset(
                    "nodes",
                    self.identity.node_id,
                    json.dumps({**self.identity.to_dict(), "last_heartbeat": datetime.utcnow().isoformat()})
                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

    async def _expiry_loop(self):
        """ÅÒÇáÉ ÇáÚÞÏ ÇáãäÊåíÉ"""
        while True:
            await asyncio.sleep(ConfigSettings.HEARTBEAT_INTERVAL)
            now = datetime.utcnow()
            nodes = await self.redis.hgetall("nodes")
            for node_id, data in nodes.items():
                node = json.loads(data)
                last = datetime.fromisoformat(node["last_heartbeat"])
                if (now - last).total_seconds() > ConfigSettings.NODE_EXPIRY:
                    await self.redis.hdel("nodes", node_id)
                    await self.redis.publish(ConfigSettings.NODE_REGISTRY_CHANNEL, json.dumps({
                        "action": "expire",
                        "node_id": node_id
                    }))

    async def get_active_nodes(self) -> List[Dict]:
        """ÇáÍÕæá Úáì ÞÇÆãÉ ÇáÚÞÏ ÇáäÔØÉ"""
        nodes = await self.redis.hgetall("nodes")
        active = []
        now = datetime.utcnow()
        for data in nodes.values():
            node = json.loads(data)
            last = datetime.fromisoformat(node["last_heartbeat"])
            if (now - last).total_seconds() <= ConfigSettings.NODE_EXPIRY:
                active.append(node)
        return active

# 1.5 ÔÈßÉ ÇáËÞÉ ÇáãæÒÚÉ (TrustNetwork)
class TrustNetwork:
    """ÔÈßÉ ÇáËÞÉ ÇáãæÒÚÉ"""
    def __init__(self, identity: DigitalIdentity, redis_client: redis.Redis):
        self.identity = identity
        self.redis = redis_client
        self.node_registry = NodeRegistry(redis_client, identity)
        self.blacklist: Dict[str, SuspiciousContract] = {}
        self.opportunities: Dict[str, OpportunityMessage] = {}
        self._listener_task = None

    async def start(self):
        """ÈÏÁ ÇáÇÓÊãÇÚ ááÃÍÏÇË"""
        await self.node_registry.register()
        self._listener_task = asyncio.create_task(self._listen())

    async def stop(self):
        """ÅíÞÇÝ ÇáÔÈßÉ"""
        if self._listener_task:
            self._listener_task.cancel()
        await self.node_registry.unregister()

    async def _listen(self):
        """ÇáÇÓÊãÇÚ ááÃÍÏÇË ãä ÇáÞäæÇÊ"""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(
            ConfigSettings.OPPORTUNITY_CHANNEL,
            ConfigSettings.SECURITY_ALERTS_CHANNEL,
            ConfigSettings.VOTING_CHANNEL,
            ConfigSettings.NODE_REGISTRY_CHANNEL
        )

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            try:
                data = json.loads(message["data"])
                channel = message["channel"]

                if channel == ConfigSettings.OPPORTUNITY_CHANNEL:
                    await self._handle_opportunity(data)
                elif channel == ConfigSettings.SECURITY_ALERTS_CHANNEL:
                    await self._handle_alert(data)
                elif channel == ConfigSettings.VOTING_CHANNEL:
                    await self._handle_vote(data)
                # Node registry updates are handled by NodeRegistry itself
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def publish_opportunity(self, opportunity: OpportunityMessage):
        """äÔÑ ÝÑÕÉ Úáì ÇáÔÈßÉ"""
        if self.identity.trust_level == "NEW":
            logger.warning("Node in test period, cannot publish opportunities")
            return

        msg = json.dumps(asdict(opportunity), default=str)
        opportunity.signature = self.identity.sign(msg)
        opportunity.source_node = self.identity.node_id

        await self.redis.publish(ConfigSettings.OPPORTUNITY_CHANNEL, json.dumps(asdict(opportunity), default=str))
        self.opportunities[opportunity.id] = opportunity

    async def _handle_opportunity(self, data: Dict):
        """ãÚÇáÌÉ ÝÑÕÉ æÇÑÏÉ"""
        try:
            opp = OpportunityMessage(**data)
            # ÇáÊÍÞÞ ãä ÇáÊæÞíÚ
            if not DigitalIdentity.verify(json.dumps(data, default=str), opp.signature, opp.source_node):
                logger.warning(f"Invalid signature for opportunity {opp.id}")
                return

            # ÇáÊÍÞÞ ãä Ãä ÇáÚÞÏÉ ãÕÏÑåÇ ãæËæÞÉ
            nodes = await self.node_registry.get_active_nodes()
            source_node = next((n for n in nodes if n["node_id"] == opp.source_node), None)
            if not source_node or source_node["trust_level"] == "NEW":
                logger.info(f"Ignoring opportunity from low-trust node {opp.source_node}")
                return

            self.opportunities[opp.id] = opp
            logger.info(f"New opportunity {opp.id} from {opp.source_node}: profit ${opp.estimated_profit}")
        except Exception as e:
            logger.error(f"Error handling opportunity: {e}")

    async def publish_alert(self, rpc_url: str, reason: str):
        """äÔÑ ÊäÈíå Ããäí"""
        alert = {
            "type": "bad_rpc",
            "rpc_url": rpc_url,
            "reason": reason,
            "node_id": self.identity.node_id,
            "timestamp": datetime.utcnow().isoformat(),
            "reputation": self.identity.reputation,
            "signature": self.identity.sign(json.dumps({"rpc_url": rpc_url, "reason": reason}))
        }
        await self.redis.publish(ConfigSettings.SECURITY_ALERTS_CHANNEL, json.dumps(alert, default=str))

    async def _handle_alert(self, data: Dict):
        """ãÚÇáÌÉ ÊäÈíå Ããäí"""
        msg = json.dumps({"rpc_url": data["rpc_url"], "reason": data["reason"]})
        if not DigitalIdentity.verify(msg, data["signature"], data.get("public_key", "")):
            logger.warning("Invalid alert signature")
            return
        logger.warning(f"Bad RPC reported: {data['rpc_url']} - {data['reason']}")

    async def propose_contract_vote(self, contract: SuspiciousContract):
        """ØÑÍ ÚÞÏ ááÊÕæíÊ"""
        vote_msg = {
            "contract_address": contract.contract_address,
            "reported_by": contract.reported_by,
            "reason": contract.reason,
            "timestamp": contract.timestamp.isoformat(),
            "signature": self.identity.sign(json.dumps(asdict(contract), default=str))
        }
        await self.redis.publish(ConfigSettings.VOTING_CHANNEL, json.dumps(vote_msg, default=str))

    async def _handle_vote(self, data: Dict):
        """ãÚÇáÌÉ ÇáÊÕæíÊ ÇáæÇÑÏ"""
        addr = data["contract_address"]
        if addr not in self.blacklist:
            self.blacklist[addr] = SuspiciousContract(
                contract_address=addr,
                reported_by=data["reported_by"],
                reason=data["reason"],
                timestamp=datetime.fromisoformat(data["timestamp"])
            )
        contract = self.blacklist[addr]
        await self.redis.sadd(f"votes:{addr}:yes", data.get("voter", ""))

    async def sync_blacklist(self):
        """ãÒÇãäÉ ÇáÞÇÆãÉ ÇáÓæÏÇÁ ÇáÚÇáãíÉ"""
        blacklist_keys = await self.redis.keys("blacklist:*")
        for key in blacklist_keys:
            addr = key.split(":")[1]
            if addr not in self.blacklist:
                details = await self.redis.hgetall(f"contract:{addr}")
                if details:
                    self.blacklist[addr] = SuspiciousContract(
                        contract_address=addr,
                        reported_by=details.get("reported_by", "unknown"),
                        reason=details.get("reason", ""),
                        timestamp=datetime.fromisoformat(details.get("timestamp", datetime.utcnow().isoformat()))
                    )

    async def is_contract_blacklisted(self, address: str) -> bool:
        return address in self.blacklist

# 1.6 ßÇÔÝ äãØ ÇáÓæÞ (MarketRegimeDetector)
class MarketRegimeDetector:
    """ßÇÔÝ äãØ ÇáÓæÞ ÈÇÓÊÎÏÇã ÈíÇäÇÊ ÍÞíÞíÉ"""
    def __init__(self):
        self.history = deque(maxlen=100)

    async def analyze(self, market_data: Dict) -> str:
        """ÊÍáíá ÙÑæÝ ÇáÓæÞ"""
        volatility = market_data.get("volatility_24h", 0)
        price_change = market_data.get("price_change_24h", 0)
        volume_ratio = market_data.get("volume_ratio", 1.0)

        if volatility > 0.1 and volume_ratio > 2.5:
            return "high_volatility"
        elif price_change > 0.15:
            return "bull_aggressive"
        elif price_change > 0.05:
            return "bull_gradual"
        elif price_change < -0.15:
            return "bear_panic"
        elif price_change < -0.05:
            return "bear_gradual"
        else:
            return "sideways"

# 1.7 äÙÇã ÇáÊßíÝ ãÚ ÇáÓæÞ (MarketAdapter)
class MarketAdapter:
    """äÙÇã ÇáÊßíÝ ãÚ ÇáÓæÞ"""
    def __init__(self, knowledge_repo: KnowledgeRepository):
        self.knowledge_repo = knowledge_repo
        self.detector = MarketRegimeDetector()
        self.current_regime = "sideways"
        self.agent_weights = {
            "arbitrage": 0.3,
            "sandwich": 0.2,
            "liquidation": 0.2,
            "mev_boost": 0.15,
            "flash_loan": 0.15
        }
        self.risk_params = {
            "min_profit_threshold": 10.0,
            "max_slippage": 0.01,
            "max_gas_price": 50,
            "position_size_factor": 1.0
        }

    async def update(self, market_data: Dict):
        """ÊÍÏíË äãØ ÇáÓæÞ æÊßííÝ ÇáãÚÇííÑ"""
        new_regime = await self.detector.analyze(market_data)
        if new_regime == self.current_regime:
            return

        logger.info(f"Market regime changed: {self.current_regime} -> {new_regime}")
        self.current_regime = new_regime

        # ÊÛííÑ ÇáÃæÒÇä ÍÓÈ ÇáäãØ
        if new_regime in ["high_volatility", "bear_panic"]:
            self.agent_weights = {
                "arbitrage": 0.1,
                "sandwich": 0.25,
                "liquidation": 0.35,
                "mev_boost": 0.2,
                "flash_loan": 0.1
            }
            self.risk_params["min_profit_threshold"] = 50.0
            self.risk_params["max_slippage"] = 0.02
            self.risk_params["position_size_factor"] = 0.5
        elif new_regime in ["bull_aggressive", "bull_gradual"]:
            self.agent_weights = {
                "arbitrage": 0.4,
                "sandwich": 0.15,
                "liquidation": 0.1,
                "mev_boost": 0.2,
                "flash_loan": 0.15
            }
            self.risk_params["min_profit_threshold"] = 20.0
            self.risk_params["max_slippage"] = 0.01
            self.risk_params["position_size_factor"] = 1.2
        else:  # sideways, bear_gradual
            self.agent_weights = {
                "arbitrage": 0.3,
                "sandwich": 0.2,
                "liquidation": 0.2,
                "mev_boost": 0.15,
                "flash_loan": 0.15
            }
            self.risk_params["min_profit_threshold"] = 10.0
            self.risk_params["max_slippage"] = 0.01
            self.risk_params["position_size_factor"] = 0.8

        # ÇÓÊÏÚÇÁ ÞÕÕ ãÔÇÈåÉ ááÊÚáã
        similar = await self.knowledge_repo.get_similar_stories({"market_regime": new_regime})
        if similar:
            logger.info(f"Learning from {len(similar)} similar stories for regime {new_regime}")

    def get_agent_weight(self, agent_type: str) -> float:
        return self.agent_weights.get(agent_type, 0.1)

# 1.8 ÅÏÇÑÉ ÇáÞÕÕ (StoryManager)
class StoryManager:
    """ÅÏÇÑÉ ÇáÞÕÕ ÇáÊÚáíãíÉ"""
    def __init__(self, knowledge_repo: KnowledgeRepository):
        self.knowledge_repo = knowledge_repo

    async def create_from_failure(self, failure_data: Dict) -> Story:
        """ÅäÔÇÁ ÞÕÉ ãä ÝÔá"""
        analysis = self._analyze_failure(failure_data)
        story = Story(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            agent_type=failure_data.get("agent_type", "arbitrage"),
            title=analysis["title"],
            what_happened=analysis["description"],
            why_it_failed=analysis["root_cause"],
            lesson_learned=analysis["lesson"],
            financial_impact=abs(failure_data.get("loss", 0)),
            market_regime=failure_data.get("market_regime", "sideways"),
            tags=analysis["tags"]
        )
        await self.knowledge_repo.add_story(story)
        logger.info(f"Story created: {story.title}")
        print(story.to_human_readable())
        return story

    def _analyze_failure(self, failure_data: Dict) -> Dict:
        """ÊÍáíá ÇáÝÔá æÇÓÊÎáÇÕ ÇáÏÑæÓ"""
        error_type = failure_data.get("error_type", "unknown")

        if "gas" in error_type:
            return {
                "title": "ÇÑÊÝÇÚ ÓÚÑ ÇáÛÇÒ íÍæá ÑÈÍÇð ãÄßÏÇð Åáì ÎÓÇÑÉ",
                "description": f"ãÍÇæáÉ ÊäÝíÐ ÕÝÞÉ {failure_data.get('strategy', '')} áßä ÓÚÑ ÇáÛÇÒ ÇÑÊÝÚ ÈÔßá ãÝÇÌÆ",
                "root_cause": "ÇÑÊÝÇÚ ãÝÇÌÆ Ýí ÓÚÑ ÇáÛÇÒ ÈÓÈÈ ÇÒÏÍÇã ÇáÔÈßÉ",
                "lesson": "íÌÈ ãÑÇÞÈÉ ÓÚÑ ÇáÛÇÒ ÞÈá ÇáÊäÝíÐ ÈÏÞíÞÉ Úáì ÇáÃÞá æÊÌäÈ ÃæÞÇÊ ÇáÐÑæÉ",
                "tags": ["gas_spike", "network_congestion"]
            }
        elif "slippage" in error_type:
            return {
                "title": "ÇäÒáÇÞ ÇáÓÚÑ: ÏÑÓ ÞÇÓò Ýí ÅÏÇÑÉ ÇáãÎÇØÑ",
                "description": f"ÇäÒáÇÞ ÓÚÑ ßÈíÑ ÃËäÇÁ ÊäÝíÐ ÇáÕÝÞÉ Úáì {failure_data.get('protocol', 'unknown')}",
                "root_cause": "ÇáÓíæáÉ ÇáãäÎÝÖÉ Ãæ ÍÑßÉ ÓÚÑíÉ ÓÑíÚÉ",
                "lesson": "ÇÓÊÎÏÇã ÍÏæÏ ÇäÒáÇÞ ÃÞá æÊäÝíÐ ÇáÕÝÞÇÊ Úáì ÏÝÚÇÊ ÕÛíÑÉ",
                "tags": ["slippage", "liquidity_issue"]
            }
        else:
            return {
                "title": "ÏÑÓ ÌÏíÏ ãä ÓÇÍÉ ÇáãÚÑßÉ",
                "description": f"ÝÔá Ýí ÊäÝíÐ ÇÓÊÑÇÊíÌíÉ {failure_data.get('strategy', '')} ÈÓÈÈ {error_type}",
                "root_cause": error_type,
                "lesson": "ÊÍáíá ÃÝÖá ááÙÑæÝ ÞÈá ÇáÊäÝíÐ",
                "tags": ["general_failure"]
            }

# 1.9 æßíá ÇáÊÏÇæá ÇáÐßí (IntelligentTradingAgent)
class IntelligentTradingAgent:
    """Çáæßíá ÇáÑÆíÓí ááÊÏÇæá ÇáÐßí"""
    def __init__(self, identity: DigitalIdentity):
        self.identity = identity
        self.knowledge = KnowledgeRepository(identity.node_id)
        self.trust_network = None
        self.market_adapter = MarketAdapter(self.knowledge)
        self.story_manager = StoryManager(self.knowledge)
        self.metrics = {
            "total_trades": 0,
            "successful_trades": 0,
            "total_profit": 0.0,
            "total_loss": 0.0
        }
        self.running = False
        self._task = None

    async def init(self, redis_client: redis.Redis):
        """ÊåíÆÉ Çáæßíá ãÚ redis"""
        self.trust_network = TrustNetwork(self.identity, redis_client)
        await self.knowledge.init()
        await self.trust_network.start()

    async def start(self):
        """ÈÏÁ ÊÔÛíá Çáæßíá"""
        self.running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        """ÅíÞÇÝ Çáæßíá"""
        self.running = False
        if self._task:
            self._task.cancel()
        await self.trust_network.stop()

    async def _run_loop(self):
        """ÇáÍáÞÉ ÇáÑÆíÓíÉ ááæßíá"""
        while self.running:
            try:
                # ÌáÈ ÈíÇäÇÊ ÇáÓæÞ (ãÍÇßÇÉ  Ýí ÇáÅäÊÇÌ ÊÓÊÎÏã ãÕÇÏÑ ÍÞíÞíÉ)
                market_data = await self._fetch_market_data()

                # ÊÍÏíË ÇáÊßíÝ ãÚ ÇáÓæÞ
                await self.market_adapter.update(market_data)

                # ÇÎÊíÇÑ ÇáÇÓÊÑÇÊíÌíÉ ÍÓÈ ÇáÃæÒÇä
                strategies = list(self.market_adapter.agent_weights.keys())
                weights = list(self.market_adapter.agent_weights.values())
                selected = random.choices(strategies, weights=weights)[0]

                # ÊäÝíÐ ÇáÇÓÊÑÇÊíÌíÉ
                await self._execute_strategy(selected, market_data)

                # ÊÍÏíË ÇáÅÍÕÇÆíÇÊ ßá ÓÇÚÉ
                if datetime.utcnow().minute == 0:
                    self._print_stats()

                await asyncio.sleep(10)  # ÇäÊÙÇÑ Èíä ÇáÕÝÞÇÊ
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Agent loop error: {e}")
                await asyncio.sleep(5)

    async def _fetch_market_data(self) -> Dict:
        """ÌáÈ ÈíÇäÇÊ ÇáÓæÞ (ãÍÇßÇÉ  íãßä ÇÓÊÈÏÇáåÇ ÈÜ DefiLlama Ãæ Dune)"""
        return {
            "volatility_24h": random.uniform(0.02, 0.15),
            "price_change_24h": random.uniform(-0.2, 0.2),
            "volume_ratio": random.uniform(0.5, 3.0),
            "protocol": random.choice(["uniswap", "sushiswap", "curve"]),
            "gas_price": random.uniform(20, 200)
        }

    async def _execute_strategy(self, strategy: str, market_data: Dict):
        """ÊäÝíÐ ÇÓÊÑÇÊíÌíÉ ãÍÏÏÉ"""
        # ÇáÈÍË Úä ÞÕÕ ãÔÇÈåÉ
        similar = await self.knowledge.get_similar_stories({
            "agent_type": strategy,
            "market_regime": self.market_adapter.current_regime
        })
        if similar:
            logger.info(f"Found {len(similar)} similar stories for {strategy}")

        # ãÍÇßÇÉ ÊäÝíÐ ÇáÕÝÞÉ
        success_rate = 0.7 if self.market_adapter.current_regime != "high_volatility" else 0.4
        if random.random() < success_rate:
            profit = random.uniform(10, 500) * self.market_adapter.risk_params["position_size_factor"]
            self.metrics["successful_trades"] += 1
            self.metrics["total_profit"] += profit
            logger.info(f"Successful trade: +${profit:.2f}")

            # ãÔÇÑßÉ ÇáÝÑÕ ÇáßÈíÑÉ
            if profit > 100:
                opp = OpportunityMessage(
                    id=str(uuid.uuid4()),
                    source_node=self.identity.node_id,
                    signature="",
                    protocol=market_data["protocol"],
                    estimated_profit=profit,
                    required_capital=profit * 5,
                    risk_score=random.uniform(0.1, 0.5),
                    expiry=datetime.utcnow() + timedelta(minutes=1),
                    details={}
                )
                await self.trust_network.publish_opportunity(opp)
        else:
            loss = random.uniform(20, 200) * self.market_adapter.risk_params["position_size_factor"]
            self.metrics["total_loss"] += loss
            error = random.choice(["gas_price_too_high", "slippage_exceeded", "sandwich_detected"])
            logger.warning(f"Failed trade: -${loss:.2f} ({error})")

            # ÅäÔÇÁ ÞÕÉ ÊÚáíãíÉ
            await self.story_manager.create_from_failure({
                "agent_type": strategy,
                "error_type": error,
                "loss": loss,
                "market_regime": self.market_adapter.current_regime,
                "strategy": strategy,
                "protocol": market_data["protocol"]
            })

        self.metrics["total_trades"] += 1

    def _print_stats(self):
        """ØÈÇÚÉ ÇáÅÍÕÇÆíÇÊ"""
        success_rate = (self.metrics["successful_trades"] / max(1, self.metrics["total_trades"])) * 100
        net = self.metrics["total_profit"] - self.metrics["total_loss"]
        logger.info(f"""
        ????????????????????????????????????????
        ?? Agent {self.identity.node_id}
        ????????????????????????????????????????
        ?? Trades: {self.metrics['total_trades']}
        ? Success: {success_rate:.1f}%
        ?? Profit: ${self.metrics['total_profit']:,.2f}
        ?? Loss: ${self.metrics['total_loss']:,.2f}
        ?? Net: ${net:,.2f}
        ?? Regime: {self.market_adapter.current_regime}
        ?? Stories: {len(self.knowledge._embedding_cache)} (approx)
        ?? Trust: {self.identity.reputation:.0f}
        ????????????????????????????????????????
        """)

# 1.10 ÇáäÙÇã ÇáãæÒÚ ÇáÏíäÇãíßí (DistributedTradingSystem)
class DistributedTradingSystem:
    """äÙÇã ãæÒÚ íÏíÑ ÚÏÏÇð ÏíäÇãíßíÇð ãä ÇáÚÞÏ"""
    def __init__(self):
        self.agents: Dict[str, IntelligentTradingAgent] = {}
        self.redis_client: Optional[redis.Redis] = None
        self._shutdown_event = asyncio.Event()

    async def start(self):
        """ÈÏÁ ÇáäÙÇã"""
        ConfigSettings.ensure_dirs()

        # ÅÚÏÇÏ Redis
        self.redis_client = await redis.from_url(ConfigSettings.REDIS_URL, decode_responses=True)

        # ÅÔÇÑÉ áÅíÞÇÝ ÇáÊÔÛíá
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))

        # ÅäÔÇÁ 30 æßíá ßãËÇá (íãßä ÊÚÏíá ÇáÚÏÏ)
        for i in range(30):
            identity = DigitalIdentity(node_id=f"agent_{i+1:03d}")
            agent = IntelligentTradingAgent(identity)
            await agent.init(self.redis_client)
            await agent.start()
            self.agents[identity.node_id] = agent
            logger.info(f"Agent {identity.node_id} started")
            await asyncio.sleep(0.1)

        logger.info(f"System started with {len(self.agents)} agents")
        await self._monitor_loop()

    async def _monitor_loop(self):
        """ãÑÇÞÈÉ ÕÍÉ ÇáäÙÇã"""
        while not self._shutdown_event.is_set():
            await asyncio.sleep(30)
            active_nodes = await self.redis_client.hlen("nodes")
            logger.info(f"Active nodes in registry: {active_nodes}")

    async def shutdown(self):
        """ÅíÞÇÝ ÇáäÙÇã ÈÔßá Âãä"""
        logger.info("Shutting down system...")
        self._shutdown_event.set()

        # ÅíÞÇÝ ÌãíÚ ÇáæßáÇÁ
        for agent in self.agents.values():
            await agent.stop()

        if self.redis_client:
            await self.redis_client.close()

        logger.info("System stopped")
        sys.exit(0)

    async def add_agent(self, node_id: str = None):
        """ÅÖÇÝÉ æßíá ÌÏíÏ ÏíäÇãíßíÇð"""
        identity = DigitalIdentity(node_id)
        agent = IntelligentTradingAgent(identity)
        await agent.init(self.redis_client)
        await agent.start()
        self.agents[identity.node_id] = agent
        logger.info(f"New agent {identity.node_id} added")
        return identity.node_id

    async def remove_agent(self, node_id: str):
        """ÅÒÇáÉ æßíá"""
        if node_id in self.agents:
            await self.agents[node_id].stop()
            del self.agents[node_id]
            logger.info(f"Agent {node_id} removed")

# =============================================================================
# 2. ÇáäÙÇã ÇáãæÍÏ (AlKhaledUltimateOrchestrator)
# =============================================================================

class AlKhaledUltimateOrchestrator:
    """
    ÇáãÏíÑ ÇáÑÆíÓí ÇáÐí íÏãÌ ÌãíÚ ãßæäÇÊ ÇáÃÌÒÇÁ ÇáËáÇËÉ ãÚ Çáæßíá ÇáÃÓÇÓí.
    íæÝÑ æÇÌåÉ ãæÍÏÉ ááæÕæá Åáì ÌãíÚ ÇáãíÒÇÊ æÅÏÇÑÉ ÏæÑÉ ÍíÇÊåÇ.
    """
    def __init__(self, config: Dict = None, agent: AlKhaledUltimateAgent = None):
        self.config = config or {}
        self.agent = agent
        self.logger = logging.getLogger('AlKhaledOrchestrator')

        # ãßæäÇÊ ãä ÇáÌÒÁ ÇáÃæá (Åä æÌÏÊ)
        self.rpc_ext = None
        self.advisor = None
        self.neural_warning = None
        self.gas_wall = None
        self.guardian = None
        self.backup = None
        self.tester = None
        self.node_discovery = None
        self.performance = None
        self.cost_monitor = None
        self.deploy_platforms = None
        self.defillama = None
        self.dune = None
        self.updater = None
        self.terminator = None
        self.plugin_loader = None
        self.key_rotator = None
        self.multi_sig = None
        self.temp_wallets = None

        # ãßæäÇÊ ãä ÇáÌÒÁ ÇáËÇäí (Åä æÌÏÊ)
        self.cloud = None
        self.deployment = None
        self.liquid = None
        self.storage = None
        self.edge = None
        self.stealth = None
        self.scheduler = None
        self.terraform = None
        self.wallet_gen = None
        self.signature = None
        self.zero_wallet = None
        self.ethical_agents = []

        # ãßæäÇÊ ãä ÇáÌÒÁ ÇáËÇáË (ÇáäÙÇã ÇáãæÒÚ)
        self.trust_network = None
        self.distributed_system = None

        self.running = False
        self._tasks = []

    async def initialize(self):
        """ÊåíÆÉ ÌãíÚ ÇáãßæäÇÊ ÍÓÈ ÇáÅÚÏÇÏÇÊ æÇáÊæÝÑ"""
        self.logger.info("Initializing AlKhaled Ultimate Orchestrator...")

        # --- ÇáÌÒÁ ÇáÃæá ---
        if PART1_AVAILABLE:
            self.rpc_ext = RPCManagerExtended()
            self.advisor = AutoStrategyAdvisor(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                orchestrator=self.agent.orchestrator if self.agent else None,
                simulator=getattr(self.agent, 'simulator', None),
                deployer=getattr(self.agent, 'deployer', None)
            )
            self.neural_warning = NeuralEarlyWarningSystem(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                mev_scanner=getattr(self.agent, 'mev_scanner', None),
                sandwich_agent=getattr(self.agent, 'sandwich_agent', None),
                stealth=self.stealth,
                private_mempool=getattr(self.agent, 'private_mempool', None)
            )
            self.gas_wall = AdaptiveGasWall(
                config=self.config,
                gas_manager=self.agent.gas_manager if self.agent else None,
                mev_scanner=getattr(self.agent, 'mev_scanner', None),
                private_mempool=getattr(self.agent, 'private_mempool', None),
                stealth=self.stealth,
                exp_db=self.agent.exp_db if self.agent else None,
                flashbots_executor=getattr(self.agent, 'flashbots_executor', None)
            )
            self.guardian = SelfHealingContractGuardian(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                p2p=getattr(self.agent, 'p2p', None),
                healer=getattr(self.agent, 'healer', None),
                security_updater=getattr(self.agent, 'security_updater', None),
                deployer=getattr(self.agent, 'deployer', None),
                signature_mgr=getattr(self.agent, 'signature_mgr', None)
            )
            self.backup = AdvancedBackupSystem()
            self.tester = PreDeploymentTester()
            self.node_discovery = NodeDiscovery(self.config.get('node_id', str(uuid.uuid4())))
            self.performance = PerformanceEvaluator()
            self.cost_monitor = CloudCostMonitor()
            self.deploy_platforms = DeploymentPlatformManager()
            self.defillama = DefiLlamaClient()
            self.dune = DuneClient()
            self.updater = SelfUpdater(self.config)
            self.terminator = TerminationManager()
            self.plugin_loader = PluginLoader()
            self.key_rotator = KeyRotationManager(
                self.agent.key_manager if self.agent else None,
                self.config.get('key_rotation_interval', 86400)
            )
            self.multi_sig = MultiSigManager()
            self.temp_wallets = TemporaryWalletManager()
        else:
            self.logger.warning("ÇáÌÒÁ ÇáÃæá ÛíÑ ãÊæÝÑ¡ ÈÚÖ ÇáãßæäÇÊ áä ÊÚãá")

        # --- ÇáÌÒÁ ÇáËÇäí ---
        if PART2_AVAILABLE:
            self.cloud = CloudManager(
                config=self.config,
                key_manager=self.agent.key_manager if self.agent else None,
                exp_db=self.agent.exp_db if self.agent else None,
                cache=self.agent.cache if self.agent else None
            )
            self.deployment = DeploymentAgent(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None
            )
            self.liquid = LiquidInfrastructureAgent(
                config=self.config,
                cache=self.agent.cache if self.agent else None,
                cloud_mgr=self.cloud,
                agent=self.agent
            )
            self.storage = DecentralizedStorage(
                config=self.config,
                cache=self.agent.cache if self.agent else None
            )
            self.edge = EdgeNetwork(
                config=self.config,
                cache=self.agent.cache if self.agent else None,
                key_manager=self.agent.key_manager if self.agent else None
            )
            self.stealth = StealthManager(
                config=self.config,
                key_manager=self.agent.key_manager if self.agent else None
            )
            self.scheduler = SmartScheduler(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                god_pulse=self.agent.god_pulse if self.agent else None
            )
            self.terraform = TerraformIntegration(
                config=self.config,
                cloud_mgr=self.cloud
            )
            self.wallet_gen = WalletGeneratorAgent(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                key_manager=self.agent.key_manager if self.agent else None
            )
            self.signature = SignatureOpportunityAgent(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                god_pulse=self.agent.god_pulse if self.agent else None,
                wallet_gen=self.wallet_gen
            )
            self.zero_wallet = ZeroWalletAgent(
                config=self.config,
                exp_db=self.agent.exp_db if self.agent else None,
                wallet_gen=self.wallet_gen
            )

            # ÇáæßáÇÁ ÇáÃÎáÇÞíæä (29 æßíá)  äÍÊÇÌ Åáì BlockchainConnector
            if self.agent and self.agent.signer:
                connector = BlockchainConnector('ethereum', self.agent.signer.key.hex())
                self.ethical_agents = [
                    DormantContractAgent(connector),
                    BridgeDustAgent(connector),
                    GovernanceRewardsAgent(connector),
                    LiquiditySweepAgent(connector),
                    BugBountyAgent(connector),
                    MEVProtectorAgent(connector),
                    ArbitrageAgent(connector),
                    TimeSeriesAgent(connector),
                    FlashblocksAgent(connector),
                    WhiteHatMediatorAgent(connector),
                    V2LiquiditySnipingAgent(connector),
                    BountyContractsAgent(connector),
                    SafeAirdropAgent(connector),
                    RelayContractsAgent(connector),
                    PancakeOldPoolsAgent(connector),
                    OldGovernanceAgent(connector),
                    UnclaimedBridgeAgent(connector),
                    V1LiquidityAgent(connector),
                    ExpiredGovernanceRewardsAgent(connector),
                    DustHuntingAgent(connector),
                    VulnerabilityReportingAgent(connector),
                    SmartContractWriterAgent(connector),
                    SecurityAuditorAgent(connector),
                    SolverAgent(connector),
                    FrontrunProtectorAgent(connector),
                    MempoolWatcherAgent(connector),
                    GasOptimizerAgent(connector),
                    ComplianceAgent(connector),
                    ReportingAgent(connector)
                ]
            else:
                self.logger.warning("áÇ íæÌÏ signer Ýí Çáæßíá ÇáÃÓÇÓí¡ áä íÊã ÊÔÛíá ÇáæßáÇÁ ÇáÃÎáÇÞííä")
        else:
            self.logger.warning("ÇáÌÒÁ ÇáËÇäí ÛíÑ ãÊæÝÑ¡ ÈÚÖ ÇáãßæäÇÊ áä ÊÚãá")

        # --- ÇáÌÒÁ ÇáËÇáË (ÇáäÙÇã ÇáãæÒÚ) ---
        # äÍÊÇÌ Åáì redis_client ãä Çáæßíá ÇáÃÓÇÓí Ãæ ääÔÆå
        if self.agent and hasattr(self.agent, 'redis') and self.agent.redis:
            redis_client = self.agent.redis
        else:
            # ÅäÔÇÁ Úãíá Redis ÌÏíÏ
            redis_client = await redis.from_url(ConfigSettings.REDIS_URL, decode_responses=True)

        identity = DigitalIdentity(self.config.get('node_id', str(uuid.uuid4())))
        self.trust_network = TrustNetwork(identity, redis_client)
        self.distributed_system = DistributedTradingSystem()  # åÐÇ ÇáäÙÇã íÏíÑ æßáÇÁå ÇáÎÇÕíä

        # ÅÖÇÝÉ ÇáæßáÇÁ ÇáÃÎáÇÞííä Åáì ÇáäÙÇã ÇáãæÍÏ (ÇÎÊíÇÑí)
        if hasattr(self.agent, 'orchestrator'):
            for agent in self.ethical_agents:
                self.agent.orchestrator.agents[agent.name] = agent

        self.logger.info("Orchestrator initialized")

    async def start(self):
        """ÊÔÛíá ÌãíÚ ÇáãßæäÇÊ Ýí ÇáÎáÝíÉ"""
        if self.running:
            return
        self.running = True

        await self.initialize()

        # ÊÔÛíá ÇáãåÇã ÇáÎáÝíÉ
        tasks = []

        if self.advisor:
            tasks.append(asyncio.create_task(self.advisor.start()))
        if self.neural_warning:
            tasks.append(asyncio.create_task(self.neural_warning.start()))
        if self.gas_wall:
            tasks.append(asyncio.create_task(self.gas_wall.start()))
        if self.guardian:
            tasks.append(asyncio.create_task(self.guardian.start()))
        if self.backup:
            # áÇ äÍÊÇÌ Åáì ÊÔÛíá backup Ýí ÇáÎáÝíÉ¡ íÓÊÎÏã ÚäÏ ÇáØáÈ
            pass
        if self.tester:
            pass  # íÓÊÎÏã ÚäÏ ÇáØáÈ
        if self.node_discovery:
            tasks.append(asyncio.create_task(self.node_discovery.start()))
        if self.performance:
            tasks.append(asyncio.create_task(self.performance.start()))
        if self.cost_monitor:
            tasks.append(asyncio.create_task(self.cost_monitor.start()))
        if self.deploy_platforms:
            pass
        if self.defillama:
            pass
        if self.dune:
            pass
        if self.updater:
            pass  # íÓÊÎÏã ÚäÏ ÇáØáÈ
        if self.terminator:
            pass
        if self.plugin_loader:
            tasks.append(asyncio.create_task(self.plugin_loader.load_plugins()))
        if self.key_rotator:
            tasks.append(asyncio.create_task(self.key_rotator.start()))
        if self.multi_sig:
            pass
        if self.temp_wallets:
            tasks.append(asyncio.create_task(self.temp_wallets.start_cleanup()))

        # ãßæäÇÊ ÇáÌÒÁ ÇáËÇäí
        if self.cloud:
            tasks.append(asyncio.create_task(self.cloud.initialize()))
        if self.deployment:
            tasks.append(asyncio.create_task(self.deployment.start_monitoring()))
        if self.liquid:
            tasks.append(asyncio.create_task(self.liquid.start_monitoring()))
        if self.scheduler:
            tasks.append(asyncio.create_task(self.scheduler.start()))
        if self.wallet_gen:
            tasks.append(asyncio.create_task(self.wallet_gen.setup()))
        if self.zero_wallet:
            tasks.append(asyncio.create_task(self.zero_wallet.setup()))
        for agent in self.ethical_agents:
            tasks.append(asyncio.create_task(agent.run()))

        # ÇáäÙÇã ÇáãæÒÚ
        if self.distributed_system:
            tasks.append(asyncio.create_task(self.distributed_system.start()))

        self._tasks = tasks
        self.logger.info(f"Orchestrator started with {len(tasks)} background tasks")

    async def stop(self):
        """ÅíÞÇÝ ÌãíÚ ÇáãßæäÇÊ"""
        self.running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)

        # ÅíÞÇÝ ãßæäÇÊ ãÍÏÏÉ
        if self.advisor:
            await self.advisor.stop()
        if self.neural_warning:
            await self.neural_warning.stop()
        if self.gas_wall:
            await self.gas_wall.stop()
        if self.guardian:
            await self.guardian.stop()
        if self.node_discovery:
            await self.node_discovery.stop()
        if self.performance:
            await self.performance.stop()
        if self.cost_monitor:
            await self.cost_monitor.stop()
        if self.key_rotator:
            await self.key_rotator.stop()
        if self.temp_wallets:
            await self.temp_wallets.stop()
        if self.deployment:
            await self.deployment.stop()
        if self.liquid:
            await self.liquid.stop()
        if self.scheduler:
            await self.scheduler.stop()
        if self.edge:
            await self.edge.close()
        if self.defillama:
            await self.defillama.close()
        if self.dune:
            await self.dune.close()
        if self.distributed_system:
            await self.distributed_system.shutdown()
        for agent in self.ethical_agents:
            agent.stop()

        self.logger.info("Orchestrator stopped")

    def get_status(self) -> Dict:
        """ÇáÍÕæá Úáì ÍÇáÉ ÇáäÙÇã"""
        status = {
            "running": self.running,
            "components": {
                "advisor": self.advisor is not None,
                "neural_warning": self.neural_warning is not None,
                "gas_wall": self.gas_wall is not None,
                "guardian": self.guardian is not None,
                "node_discovery": self.node_discovery is not None,
                "performance": self.performance is not None,
                "cost_monitor": self.cost_monitor is not None,
                "cloud": self.cloud is not None,
                "deployment": self.deployment is not None,
                "liquid": self.liquid is not None,
                "storage": self.storage is not None,
                "edge": self.edge is not None,
                "stealth": self.stealth is not None,
                "scheduler": self.scheduler is not None,
                "terraform": self.terraform is not None,
                "wallet_gen": self.wallet_gen is not None,
                "signature": self.signature is not None,
                "zero_wallet": self.zero_wallet is not None,
                "ethical_agents": len(self.ethical_agents),
                "distributed_system": self.distributed_system is not None
            }
        }
        if self.node_discovery:
            status["node_discovery_details"] = {
                "nodes": len(self.node_discovery.nodes),
                "active": len(self.node_discovery.active_nodes)
            }
        if self.scheduler:
            status["scheduler"] = {
                "tasks": len(self.scheduler.tasks),
                "task_names": list(self.scheduler.tasks.keys())
            }
        if self.wallet_gen:
            status["wallets"] = len(self.wallet_gen.wallets)
        if self.zero_wallet:
            status["testnet_wallets"] = len(self.zero_wallet.testnet_wallets)
        return status

    async def run_api(self, host: str = "0.0.0.0", port: int = 8000):
        """ÊÔÛíá ÎÇÏã FastAPI (ÅÐÇ ßÇä ãÊÇÍÇð)"""
        if not FASTAPI_AVAILABLE:
            self.logger.error("FastAPI not available")
            return

        # ÅäÔÇÁ ÇáÊØÈíÞ
        from additions_part2 import create_api_for_nexus
        app = create_api_for_nexus(
            cloud_manager=self.cloud,
            deployment=self.deployment,
            liquid=self.liquid,
            storage=self.storage,
            edge=self.edge,
            stealth=self.stealth,
            scheduler=self.scheduler,
            terraform=self.terraform,
            wallet_gen=self.wallet_gen,
            signature=self.signature,
            zero_wallet=self.zero_wallet
        )

        # ÅÖÇÝÉ äÞÇØ äåÇíÉ ÅÖÇÝíÉ ãä ÇáÌÒÁ ÇáËÇáË
        @app.get("/distributed/status")
        async def distributed_status():
            if self.distributed_system:
                return {"agents": len(self.distributed_system.agents)}
            return {"error": "Distributed system not available"}

        @app.post("/distributed/add_agent")
        async def add_agent(node_id: str = None):
            if self.distributed_system:
                new_id = await self.distributed_system.add_agent(node_id)
                return {"node_id": new_id}
            return {"error": "Distributed system not available"}

        @app.post("/distributed/remove_agent")
        async def remove_agent(node_id: str):
            if self.distributed_system:
                await self.distributed_system.remove_agent(node_id)
                return {"status": "removed"}
            return {"error": "Distributed system not available"}

        @app.get("/stories/similar")
        async def get_similar_stories(agent_type: str = None, market_regime: str = None):
            # äÍÊÇÌ Åáì ãÚÑÝÉ Ãí KnowledgeRepository äÓÊÎÏã
            # äÓÊÎÏã ãä Ãæá æßíá Ýí ÇáäÙÇã ÇáãæÒÚ
            if self.distributed_system and self.distributed_system.agents:
                first_agent = next(iter(self.distributed_system.agents.values()))
                stories = await first_agent.knowledge.get_similar_stories({
                    "agent_type": agent_type or "",
                    "market_regime": market_regime or ""
                })
                return [s.to_dict() for s in stories]
            return {"error": "No knowledge repository available"}

        @app.get("/orchestrator/status")
        async def orchestrator_status():
            return self.get_status()

        config = uvicorn.Config(app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

# =============================================================================
# 3. ÏÇáÉ ÇáÍÞä ÇáäåÇÆíÉ (inject_all)
# =============================================================================

def inject_all(agent: AlKhaledUltimateAgent) -> AlKhaledUltimateOrchestrator:
    """
    ÍÞä ÌãíÚ ÇáÅÖÇÝÇÊ ãä ÇáÃÌÒÇÁ ÇáËáÇËÉ Ýí Çáæßíá ÇáÃÓÇÓí.
    ÊÖíÝ ÎÇÕíÉ 'orchestrator' æÊÔÛá ÇáãßæäÇÊ.
    """
    if not hasattr(agent, 'orchestrator'):
        agent.orchestrator = AlKhaledUltimateOrchestrator({}, agent)
        asyncio.create_task(agent.orchestrator.start())
        logger.info("All additions injected into AlKhaledUltimateAgent")
    return agent.orchestrator

# =============================================================================
# äÞØÉ ÏÎæá ÇÎÊíÇÑíÉ ááÇÎÊÈÇÑ
# =============================================================================

async def test_part3():
    print("\n" + "="*60)
    print("?? ÇÎÊÈÇÑ ÇáÌÒÁ ÇáËÇáË - ÇáäÙÇã ÇáãæÒÚ + ÇáäÙÇã ÇáãæÍÏ")
    print("="*60)

    # ÇÎÊÈÇÑ DigitalIdentity
    try:
        identity = DigitalIdentity()
        message = "test message"
        sig = identity.sign(message)
        assert DigitalIdentity.verify(message, sig, identity.public_key_pem)
        print("? DigitalIdentity works")
    except Exception as e:
        print(f"? DigitalIdentity test failed: {e}")

    # ÇÎÊÈÇÑ KnowledgeRepository
    try:
        repo = KnowledgeRepository("test_node")
        await repo.init()
        story = Story(
            id="test1",
            timestamp=datetime.utcnow(),
            agent_type="arbitrage",
            title="Test story",
            what_happened="Something happened",
            why_it_failed="Gas spike",
            lesson_learned="Check gas",
            financial_impact=100,
            market_regime="high_volatility",
            tags=["gas"]
        )
        await repo.add_story(story)
        similar = await repo.get_similar_stories({"market_regime": "high_volatility"})
        print(f"? KnowledgeRepository stored story, found {len(similar)} similar")
    except Exception as e:
        print(f"? KnowledgeRepository test failed: {e}")

    # ÇÎÊÈÇÑ TrustNetwork (íÊØáÈ Redis)
    try:
        redis_client = await redis.from_url(ConfigSettings.REDIS_URL, decode_responses=True)
        identity = DigitalIdentity()
        trust = TrustNetwork(identity, redis_client)
        await trust.start()
        await asyncio.sleep(1)
        await trust.stop()
        await redis_client.close()
        print("? TrustNetwork started and stopped")
    except Exception as e:
        print(f"? TrustNetwork test failed: {e}")

    # ÇÎÊÈÇÑ MarketRegimeDetector
    try:
        detector = MarketRegimeDetector()
        regime = await detector.analyze({"volatility_24h": 0.12, "price_change_24h": 0.05, "volume_ratio": 3.0})
        assert regime == "high_volatility"
        print("? MarketRegimeDetector works")
    except Exception as e:
        print(f"? MarketRegimeDetector test failed: {e}")

    # ÇÎÊÈÇÑ IntelligentTradingAgent (ãÍÇßÇÉ)
    try:
        identity = DigitalIdentity()
        agent = IntelligentTradingAgent(identity)
        # áÇ äÈÏÃå ÝÚáíÇð¡ ÝÞØ äÊÍÞÞ ãä ÇáÊåíÆÉ
        await agent.knowledge.init()
        print("? IntelligentTradingAgent initialized")
    except Exception as e:
        print(f"? IntelligentTradingAgent test failed: {e}")

    print("\n" + "="*60)
    print("? ÇäÊåì ÇÎÊÈÇÑ ÇáÌÒÁ ÇáËÇáË")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_part3())
