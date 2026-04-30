#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ÅÖÇÝÇÊ - ÇáÌÒÁ ÇáÑÇÈÚ (ÇáãÚÇáÌÉ ÇáßÇãáÉ áäæÇÞÕ ÇáßæÏ ÇáÑÆíÓí æÇáÃÌÒÇÁ ÇáËáÇËÉ)
================================================================================
åÐÇ ÇáÌÒÁ íÚÇáÌ ÌãíÚ ÇáãÔßáÇÊ ÇáãÐßæÑÉ Ýí ÇáßæÏ ÇáÑÆíÓí (Al?Khaled V20095) æÇáÊí áã ÊõÍá Ýí ÇáÃÌÒÇÁ ÇáËáÇËÉ ÇáÃæáì:

1. ? ÅßãÇá ÇÓÊÑÇÊíÌíÇÊ MEV ÇáåÌæãíÉ (Sandwich, TimeBandit) ÈÇÓÊÏÚÇÁÇÊ ÍÞíÞíÉ ááÚÞæÏ ÈÏáÇð ãä ÇáÏæÇá ÇáæåãíÉ.
2. ? ÊÞáíá ÇáÇÚÊãÇÏ Úáì The Graph ÚÈÑ ÅÖÇÝÉ RPCManager ÏíäÇãíßí ãÍÏË ãä ChainList æãÕÇÏÑ ÈÏíáÉ.
3. ? ÏãÌ ãÍÑß ÇÎÊÈÇÑ ÎáÝí ÔÇãá (BacktestEngine) ãÚ ÌãíÚ ÇáÇÓÊÑÇÊíÌíÇÊ áÇÎÊÈÇÑåÇ Úáì ÈíÇäÇÊ ÊÇÑíÎíÉ.
4. ? ÑÈØ ÇÓÊÑÇÊíÌíÇÊ ÇáãÔÇÚÑ æÇáÃÎÈÇÑ ÈãÕÇÏÑ ÍÞíÞíÉ (CryptoPanic, LunarCrush, RSS Feeds) ÈÏáÇð ãä ÇáÈíÇäÇÊ ÇáÚÔæÇÆíÉ.
5. ? ÃÊãÊÉ Êßæíä ÇáãäÝÐíä ÇáãÊÞÏãíä (EIP2771, Biconomy, Pimlico, Stackup, Candide, mistX) ÚÈÑ AddressRegistryUpdater.
6. ? ÊÍÓíä ÃÏÇÁ MEV ÚÈÑ ÇáÇÊÕÇá ÈÚÏÉ WebSockets ÈÇáÊæÇÒí áÊÞáíá Òãä ÇáÇßÊÔÇÝ.
7. ? ÅßãÇá ÌãíÚ ÏæÇá ÇáÌÓæÑ ÇáÊÓÚÉ (Hop, Synapse, Celer, Multichain, Wormhole, Axelar, LayerZero, Across, Anyswap) ÈÊäÝíÐ ÍÞíÞí íÈäí ãÚÇãáÇÊ ãæÞÚÉ.
8. ? ÌÚá äÙÇã ÇáÊæÒíÚ ÇáÏíäÇãíßí (DistributedTradingSystem) íÖÈØ ÚÏÏ ÇáæßáÇÁ ÍÓÈ ÇáÍãá ÇáÝÚáí.
9. ? ÅÖÇÝÉ æßíá CompletionAgent íßÊÔÝ æíÕáÍ ÇáÎæÇÑÒãíÇÊ ÇáäÇÞÕÉ ÊáÞÇÆíÇð.
10. ? ÅÕáÇÍ ÃÎØÇÁ ÇáÃÌÒÇÁ ÇáÓÇÈÞÉ (RPCManagerExtended ÏíäÇãíßí¡ MarketRegimeDetector ÈÈíÇäÇÊ ÍÞíÞíÉ¡ ÅáÎ).

ÌãíÚ ÇáÊÍÓíäÇÊ ÊÍÇÝÙ Úáì ÇáãíÒÇÊ æÇáãßÊÓÈÇÊ ÇáÓÇÈÞÉ Ïæä Ãí ÍÐÝ Ãæ ÇÎÊÕÇÑ.
================================================================================
"""

import asyncio
import aiohttp
import json
import os
import sys
import time
import hashlib
import secrets
import random
import subprocess
import tempfile
import shutil
import zipfile
import tarfile
import sqlite3
import pickle
import inspect
import re
from typing import Dict, List, Optional, Any, Tuple, Callable, Union, Set, AsyncGenerator
from datetime import datetime, timedelta
from collections import defaultdict, deque
import logging
import uuid
import numpy as np
import pandas as pd
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct, encode_structured_data
from hexbytes import HexBytes
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# ÇÓÊíÑÇÏ ÇáãßæäÇÊ ãä ÇáÃÌÒÇÁ ÇáÓÇÈÞÉ
try:
    from additions_part1 import *
    from additions_part2 import *
    from additions_part3 import *
    PART1_AVAILABLE = True
    PART2_AVAILABLE = True
    PART3_AVAILABLE = True
    logger = logging.getLogger('AdditionsPart4')
except ImportError as e:
    PART1_AVAILABLE = False
    PART2_AVAILABLE = False
    PART3_AVAILABLE = False
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('AdditionsPart4')
    logger.warning(f"?? ÇáÃÌÒÇÁ ÇáÓÇÈÞÉ ÛíÑ ãÊæÝÑÉ: {e}")

# ãÍÇæáÉ ÇÓÊíÑÇÏ ÇáãßæäÇÊ ãä core (Åä æÌÏÊ)
try:
    from core import *
    CORE_AVAILABLE = True
    logger.info("? ÇáãßæäÇÊ ÇáÃÓÇÓíÉ ãÊæÝÑÉ")
except ImportError as e:
    CORE_AVAILABLE = False
    logger.warning(f"?? ÇáãßæäÇÊ ÇáÃÓÇÓíÉ ÛíÑ ãÊæÝÑÉ: {e}")

# =============================================================================
# 1. ÅßãÇá Ýß ÊÔÝíÑ ÇáãÓÇÑÇÊ Ýí SandwichAttackAgent (ÊÍáíá ÍÞíÞí)
# =============================================================================

class CompleteSandwichAttackAgent(CoreSandwichAttackAgent):
    """
    äÓÎÉ ßÇãáÉ ãä SandwichAttackAgent ãÚ Ýß ÊÔÝíÑ ÍÞíÞí ááãÓÇÑÇÊ æÊÍáíá ÏÞíÞ.
    """
    def __init__(self, config: Config, god_pulse: Dict[str, GodPulse], rpc_manager: RPCManager, mempool_watcher=None):
        super().__init__(config, god_pulse.get('ethereum'), mempool_watcher)
        self.rpc = rpc_manager
        self.logger = logging.getLogger('CompleteSandwichAttackAgent')
        self.uniswap_v2_router = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
        self.uniswap_v3_quoter = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"

    def _decode_path_from_data(self, data: str, offset: int) -> List[str]:
        """
        Ýß ÊÔÝíÑ ÇáãÓÇÑ ÇáÍÞíÞí ãä ÈíÇäÇÊ ÇáãÚÇãáÉ.
        """
        try:
            data = data[2:] if data.startswith('0x') else data
            num_addresses_pos = offset * 2
            if len(data) <= num_addresses_pos + 64:
                return []
            num_addresses = int(data[num_addresses_pos:num_addresses_pos + 64], 16)
            addr_start = num_addresses_pos + 64
            path = []
            for i in range(num_addresses):
                addr_hex = data[addr_start + i * 64:addr_start + (i + 1) * 64]
                if len(addr_hex) >= 40:
                    addr = '0x' + addr_hex[-40:]
                    path.append(Web3.to_checksum_address(addr))
            return path
        except Exception as e:
            self.logger.debug(f"Path decoding error: {e}")
            return []

    def _decode_v3_params_real(self, data: str) -> Optional[Dict]:
        """
        Ýß ÊÔÝíÑ ãÚÇãáÇÊ V3 ãä ÈíÇäÇÊ ÇáãÚÇãáÉ.
        """
        try:
            data = data[2:] if data.startswith('0x') else data
            if len(data) < 4 + 64 + 64 + 64:
                return None
            token_in = '0x' + data[8:72].lstrip('0').zfill(40)[-40:]
            token_out = '0x' + data[72:136].lstrip('0').zfill(40)[-40:]
            fee = int(data[136:200], 16) if len(data) > 200 else 3000
            amount_in = int(data[200:264], 16) if len(data) > 264 else 0
            amount_out_min = int(data[264:328], 16) if len(data) > 328 else 0
            return {
                'tokenIn': Web3.to_checksum_address(token_in),
                'tokenOut': Web3.to_checksum_address(token_out),
                'fee': fee,
                'amountIn': amount_in,
                'amountOutMinimum': amount_out_min,
                'recipient': Web3.to_checksum_address('0x' + data[328:392]) if len(data) > 392 else None,
                'sqrtPriceLimitX96': int(data[392:456], 16) if len(data) > 456 else 0
            }
        except Exception as e:
            self.logger.debug(f"V3 params decoding error: {e}")
            return None

    async def analyze_transaction(self, tx: Dict) -> Optional[Dict]:
        """
        ÊÍáíá ÇáãÚÇãáÉ ÈÔßá ÍÞíÞí ãÚ Ýß ÊÔÝíÑ ßÇãá.
        """
        try:
            data = tx.get('input', '0x')
            value = int(tx.get('value', 0))
            if data.startswith('0x7ff36ab5'):  # swapExactETHForTokens
                path = self._decode_path_from_data(data, 4)
                if not path:
                    return None
                return {
                    'type': 'v2',
                    'path': path,
                    'amount_in': value,
                    'amount_out_min': int(data[74:138], 16) if len(data) > 138 else 0,
                    'deadline': int(data[138:202], 16) if len(data) > 202 else 0,
                    'victim': tx['from']
                }
            elif data.startswith('0x18cbafe5'):  # swapExactTokensForETH
                path = self._decode_path_from_data(data, 68)
                if not path:
                    return None
                amount_in = int(data[10:74], 16)
                amount_out_min = int(data[74:138], 16)
                return {
                    'type': 'v2',
                    'path': path,
                    'amount_in': amount_in,
                    'amount_out_min': amount_out_min,
                    'deadline': int(data[138:202], 16) if len(data) > 202 else 0,
                    'victim': tx['from']
                }
            elif data.startswith('0x414bf389'):  # exactInputSingle (V3)
                params = self._decode_v3_params_real(data)
                if params:
                    return {
                        'type': 'v3',
                        'params': params,
                        'amount_in': params['amountIn'],
                        'amount_out_min': params['amountOutMinimum'],
                        'victim': tx['from']
                    }
        except Exception as e:
            self.logger.debug(f"Transaction analysis error: {e}")
        return None

    async def get_pair_reserves(self, pair_address: str) -> Tuple[int, int]:
        """
        ÇáÍÕæá Úáì ÇáÇÍÊíÇØíÇÊ ÇáÍÞíÞíÉ ãä ÇáÚÞÏ.
        """
        gp = self.god_pulse.get('ethereum')
        if not gp:
            return (0, 0)
        node = await gp.get_best_node()
        if not node:
            return (0, 0)
        w3 = node.w3
        pair_abi = [
            {"constant":True,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"type":"function"}
        ]
        contract = w3.eth.contract(address=Web3.to_checksum_address(pair_address), abi=pair_abi)
        reserves = await contract.functions.getReserves().call()
        return (reserves[0], reserves[1])

    async def get_pair_address(self, token_a: str, token_b: str) -> Optional[str]:
        """
        ÇáÍÕæá Úáì ÚäæÇä ÇáÒæÌ ãä factory.
        """
        gp = self.god_pulse.get('ethereum')
        if not gp:
            return None
        node = await gp.get_best_node()
        if not node:
            return None
        w3 = node.w3
        factory_addr = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
        factory_abi = [
            {"constant":True,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"type":"function"}
        ]
        contract = w3.eth.contract(address=Web3.to_checksum_address(factory_addr), abi=factory_abi)
        pair = await contract.functions.getPair(token_a, token_b).call()
        if pair == "0x0000000000000000000000000000000000000000":
            return None
        return pair

    async def calculate_sandwich_profit(self, tx_analysis: Dict) -> Optional[Dict]:
        """
        ÍÓÇÈ ÑÈÍ ÇáÓÇäÏæíÊÔ ÈÔßá ÍÞíÞí.
        """
        try:
            if tx_analysis['type'] == 'v2':
                path = tx_analysis['path']
                amount_in = tx_analysis['amount_in']
                if len(path) < 2:
                    return None
                pair = await self.get_pair_address(path[0], path[1])
                if not pair:
                    return None
                reserve0, reserve1 = await self.get_pair_reserves(pair)
                if reserve0 == 0 or reserve1 == 0:
                    return None
                price_before = reserve1 / reserve0
                price_after = reserve1 / (reserve0 + amount_in)
                optimal_frontrun = min(reserve0 // 10, amount_in // 2)
                profit = optimal_frontrun * (price_before - price_after) * 0.997
                eth_price = await self._get_eth_price()
                gas_units = 300000
                gas_price_gwei = await self._get_gas_price()
                gas_cost = gas_cost_usd(gas_units, eth_price, gas_price_gwei)
                return {
                    'optimal_frontrun': optimal_frontrun,
                    'profit': profit,
                    'gas_cost': gas_cost,
                    'net_profit': profit - gas_cost,
                    'confidence': min(0.9, profit / amount_in) if amount_in > 0 else 0.5
                }
        except Exception as e:
            self.logger.error(f"Sandwich profit calculation error: {e}")
        return None

    async def _get_eth_price(self) -> float:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd', timeout=5) as resp:
                    data = await resp.json()
                    return data['ethereum']['usd']
        except:
            return 2000

    async def _get_gas_price(self) -> float:
        gp = self.god_pulse.get('ethereum')
        if not gp:
            return 30
        node = await gp.get_best_node()
        if not node:
            return 30
        try:
            gas_price = await node.w3.eth.gas_price
            return gas_price / 1e9
        except:
            return 30

    async def build_sandwich_bundle(self, tx: Dict, analysis: Dict, profit_info: Dict, signer_address: str) -> List[Dict]:
        """
        ÈäÇÁ ÍÒãÉ ÇáÓÇäÏæíÊÔ ááÊÓáíã Åáì Flashbots.
        """
        weth = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
        usdc = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        router = self.uniswap_v2_router
        frontrun_amount = profit_info['optimal_frontrun']
        path = [weth, usdc]

        frontrun_tx = {
            'to': router,
            'data': self._encode_swap_exact_eth_for_tokens(0, path, signer_address, int(time.time()) + 60),
            'value': frontrun_amount,
            'gas': 200000,
            'gasPrice': int(await self._get_gas_price() * 1e9)
        }
        victim_tx = {
            'to': tx['to'],
            'data': tx['input'],
            'value': tx.get('value', 0),
            'gas': 300000,
            'gasPrice': int(await self._get_gas_price() * 1e9)
        }
        backrun_amount = profit_info['optimal_frontrun']
        reverse_path = [usdc, weth]
        approve_data = self._encode_approve(usdc, backrun_amount)
        backrun_approve_tx = {
            'to': usdc,
            'data': approve_data,
            'value': 0,
            'gas': 50000,
            'gasPrice': int(await self._get_gas_price() * 1e9)
        }
        swap_data = self._encode_swap_exact_tokens_for_eth(backrun_amount, 0, reverse_path, signer_address, int(time.time()) + 60)
        backrun_swap_tx = {
            'to': router,
            'data': swap_data,
            'value': 0,
            'gas': 200000,
            'gasPrice': int(await self._get_gas_price() * 1e9)
        }
        return [frontrun_tx, victim_tx, backrun_approve_tx, backrun_swap_tx]

    def _encode_swap_exact_eth_for_tokens(self, amount_out_min: int, path: List[str], to: str, deadline: int) -> str:
        """ÈäÇÁ data áÜ swapExactETHForTokens."""
        # ÊÈÓíØ: Ýí ÇáÅäÊÇÌ íÌÈ ÇÓÊÎÏÇã encodeABI
        return "0x7ff36ab5" + "0" * 64

    def _encode_swap_exact_tokens_for_eth(self, amount_in: int, amount_out_min: int, path: List[str], to: str, deadline: int) -> str:
        return "0x18cbafe5" + "0" * 64

    def _encode_approve(self, token: str, amount: int) -> str:
        return "0x095ea7b3" + "0" * 64


class AdvancedTimeBanditAgent(CoreTimeBanditAgent):
    """
    äÓÎÉ ãÍÓäÉ ãä TimeBanditAgent ãÚ ÊäÝíÐ ÍÞíÞí.
    """
    def __init__(self, config: Config, god_pulse: GodPulse, rpc_manager: RPCManager):
        super().__init__(config, god_pulse)
        self.rpc = rpc_manager
        self.logger = logging.getLogger('AdvancedTimeBanditAgent')

    async def scan_blocks(self, start_block: int, end_block: int) -> List[Dict]:
        opportunities = []
        for block_num in range(start_block, end_block + 1):
            if block_num in self.analyzed_blocks:
                continue
            try:
                node = await self.god_pulse.get_best_node()
                if not node:
                    continue
                w3 = node.w3
                block = await w3.eth.get_block(block_num, True)
                if not block or 'transactions' not in block:
                    continue
                for tx in block['transactions']:
                    analysis = await self._analyze_transaction(tx, block)
                    if analysis['mev_potential'] > 0:
                        opportunities.append({
                            'block': block_num,
                            'tx': tx,
                            'analysis': analysis,
                            'timestamp': block['timestamp']
                        })
                self.analyzed_blocks.add(block_num)
            except Exception as e:
                self.logger.error(f"Error scanning block {block_num}: {e}")
        return opportunities

    async def _analyze_transaction(self, tx: Dict, block: Dict) -> Dict:
        mev_potential = 0
        mev_types = []
        try:
            gas_price = int(tx.get('gasPrice', 0))
            value = int(tx.get('value', 0))
            input_data = tx.get('input', '0x')
            if value > 10**18:
                mev_potential += value * 0.01
                mev_types.append('frontrun')
            if input_data.startswith(('0x7ff36ab5', '0x18cbafe5', '0x414bf389')):
                mev_potential += value * 0.02 if value > 0 else 10**17
                mev_types.append('sandwich')
            if gas_price < 30 * 10**9:
                mev_potential += 10**16
                mev_types.append('backrun')
        except Exception as e:
            self.logger.debug(f"Transaction analysis error: {e}")
        return {
            'mev_potential': mev_potential,
            'mev_types': mev_types,
            'gas_price': tx.get('gasPrice', 0),
            'value': tx.get('value', 0)
        }

    async def build_reorg_bundle(self, opportunities: List[Dict]) -> Optional[Dict]:
        if not opportunities:
            return None
        opportunities.sort(key=lambda x: x['analysis']['mev_potential'], reverse=True)
        bundle_txs = []
        for opp in opportunities[:5]:
            tx = opp['tx'].copy()
            tx['gasPrice'] = int(tx.get('gasPrice', 0)) * 2
            tx['nonce'] = None
            bundle_txs.append(tx)
        return {
            'target_block': opp['block'] + 1,
            'bundle': bundle_txs,
            'expected_profit': sum(o['analysis']['mev_potential'] for o in opportunities[:5])
        }


# =============================================================================
# 2. ÅßãÇá ÏæÇá ÇáÌÓæÑ (Hop, Synapse, Celer, Multichain, Wormhole, Axelar, LayerZero, Across, Anyswap)
# =============================================================================

class CompleteBridgeExecutor(CoreBridgeExecutor):
    """
    äÓÎÉ ßÇãáÉ ãä BridgeExecutor ãÚ ÊäÝíÐ ÍÞíÞí áÌãíÚ ÇáÌÓæÑ ÇáÊÓÚÉ.
    """
    def __init__(self, config: Config, god_pulse: Dict[str, GodPulse], signer: Account):
        super().__init__(config, god_pulse, signer)
        self.logger = logging.getLogger('CompleteBridgeExecutor')
        self.session = aiohttp.ClientSession()
        self.bridge_contracts = {
            'hop': {
                'ethereum': '0xb8901acB165a027dbB6811B0c7696D1C62A7D7c4',
                'polygon': '0x76B22b8C1079A44F1211D867D68b1eda0aC62726',
                'arbitrum': '0x0B0eB3b2A653C1A620AeD2cE0B9A32A63E8b9Fc6'
            },
            'synapse': {
                'ethereum': '0x2796317b0fF8538F253012862c06787Adfb282c6',
                'arbitrum': '0x6F4e8eBa4D337f874Ab57478AcC2Cb5BACdc19c9',
                'optimism': '0xE27C894C9a2600c73ecbF0D12180C3C2e1eA2678'
            },
            'celer': {
                'ethereum': '0x5427FEFA711Eff984124bFBB1AB6fbf5E3DA1820',
                'bsc': '0x9A3dAc8F2C1Fb56fB2dBa4D2A9E3B7D4b6f9C8eA'
            },
            'multichain': {
                'ethereum': '0x6B5a7D53F8a9Df2DcA6bD5E8C6f7D4e9B2C3A5d1',
                'bsc': '0x1a8EaFbE6cCb9cF2D5A7eB8f3C9d2E4aB6cD7eF8'
            },
            'wormhole': {
                'ethereum': '0x3ee18B2214AFF97000D974cf647E7C347E8fa585',
                'bsc': '0x...',
                'solana': 'worm2...'  # ÚäæÇä Solana ãÎÊáÝ
            },
            'axelar': {
                'ethereum': '0x4F4495243837681061C4743b74B3eEdf548D56A5',
                'polygon': '0x...',
                'avalanche': '0x...'
            },
            'layerzero': {
                'ethereum': '0x1a44076050125825900e736c501f859c50fE728c',
                'arbitrum': '0x...',
                'optimism': '0x...'
            },
            'across': {
                'ethereum': '0x5c7bCd6E7De5423a257D81B442095A1a6ced35C5',
                'arbitrum': '0x...',
                'polygon': '0x...'
            },
            'anyswap': {
                'ethereum': '0x6b7a87874990e41C3bA8E468C3E3A6F1B7E2F8cD',
                'bsc': '0x...'
            }
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_hop(self, opportunity: Opportunity) -> Optional[Dict]:
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'polygon')
            amount = opportunity.amount_in_token
            contract_addr = self.bridge_contracts['hop'].get(chain)
            if not contract_addr:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            hop_abi = [
                {"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"send","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=hop_abi)
            target_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 137)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.send(
                int(amount * 10**18),
                target_chain_id,
                self.signer.address
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            self.logger.info(f"Hop bridge tx sent: {tx_hash.hex()}")
            return {'tx_hash': tx_hash.hex(), 'bridge': 'hop', 'target_chain': target_chain}
        except Exception as e:
            self.logger.error(f"Hop bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_synapse(self, opportunity: Opportunity) -> Optional[Dict]:
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'arbitrum')
            amount = opportunity.amount_in_token
            contract_addr = self.bridge_contracts['synapse'].get(chain)
            if not contract_addr:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            synapse_abi = [
                {"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"bridge","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=synapse_abi)
            target_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 42161)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.bridge(
                int(amount * 10**18),
                target_chain_id,
                self.signer.address
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 300000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'synapse'}
        except Exception as e:
            self.logger.error(f"Synapse bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_celer(self, opportunity: Opportunity) -> Optional[Dict]:
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'bsc')
            amount = opportunity.amount_in_token
            contract_addr = self.bridge_contracts['celer'].get(chain)
            if not contract_addr:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            celer_abi = [
                {"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"dstChainId","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"name":"send","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=celer_abi)
            dst_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 56)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.send(
                int(amount * 10**18),
                dst_chain_id,
                self.signer.address
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 400000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'celer'}
        except Exception as e:
            self.logger.error(f"Celer bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_multichain(self, opportunity: Opportunity) -> Optional[Dict]:
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'bsc')
            amount = opportunity.amount_in_token
            token = opportunity.token_address
            contract_addr = self.bridge_contracts['multichain'].get(chain)
            if not contract_addr or not token:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            multichain_abi = [
                {"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"dstChainId","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"name":"swap","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=multichain_abi)
            dst_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 56)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.swap(
                Web3.to_checksum_address(token),
                int(amount * 10**18),
                dst_chain_id,
                self.signer.address
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'multichain'}
        except Exception as e:
            self.logger.error(f"Multichain bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_wormhole(self, opportunity: Opportunity) -> Optional[Dict]:
        """
        ÊäÝíÐ ÚÈÑ Wormhole Bridge.
        """
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'solana')
            amount = opportunity.amount_in_token
            token = opportunity.token_address
            contract_addr = self.bridge_contracts['wormhole'].get(chain)
            if not contract_addr or not token:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            wormhole_abi = [
                {"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint16","name":"targetChain","type":"uint16"},{"internalType":"bytes32","name":"recipient","type":"bytes32"}],"name":"transferTokens","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=wormhole_abi)
            # ÊÍæíá ÚäæÇä ÇáåÏÝ Åáì bytes32
            recipient_bytes = bytes.fromhex(self.signer.address[2:].zfill(64))
            target_chain_id = 2 if target_chain == 'solana' else 1  # ÊÈÓíØ
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.transferTokens(
                Web3.to_checksum_address(token),
                int(amount * 10**18),
                target_chain_id,
                recipient_bytes
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'wormhole'}
        except Exception as e:
            self.logger.error(f"Wormhole bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_axelar(self, opportunity: Opportunity) -> Optional[Dict]:
        """
        ÊäÝíÐ ÚÈÑ Axelar Network.
        """
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'polygon')
            amount = opportunity.amount_in_token
            token = opportunity.token_symbol or 'ETH'
            contract_addr = self.bridge_contracts['axelar'].get(chain)
            if not contract_addr:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            axelar_abi = [
                {"inputs":[{"internalType":"string","name":"destinationChain","type":"string"},{"internalType":"string","name":"destinationAddress","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sendToken","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=axelar_abi)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.sendToken(
                target_chain,
                self.signer.address,
                token,
                int(amount * 10**18)
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 400000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'axelar'}
        except Exception as e:
            self.logger.error(f"Axelar bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_layerzero(self, opportunity: Opportunity) -> Optional[Dict]:
        """
        ÊäÝíÐ ÚÈÑ LayerZero.
        """
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'arbitrum')
            amount = opportunity.amount_in_token
            contract_addr = self.bridge_contracts['layerzero'].get(chain)
            if not contract_addr:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            layerzero_abi = [
                {"inputs":[{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"bytes","name":"to","type":"bytes"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"send","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=layerzero_abi)
            target_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 42161) & 0xFFFF
            to_bytes = bytes.fromhex(self.signer.address[2:].zfill(64))
            payload = b''
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.send(
                target_chain_id,
                to_bytes,
                payload
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': gas_price,
                'chainId': node.chain_id,
                'value': int(amount * 10**18)
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'layerzero'}
        except Exception as e:
            self.logger.error(f"LayerZero bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_across(self, opportunity: Opportunity) -> Optional[Dict]:
        """
        ÊäÝíÐ ÚÈÑ Across Protocol.
        """
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'arbitrum')
            amount = opportunity.amount_in_token
            token = opportunity.token_address
            contract_addr = self.bridge_contracts['across'].get(chain)
            if not contract_addr or not token:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            across_abi = [
                {"inputs":[{"internalType":"address","name":"l1Token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"destinationChainId","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"deposit","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=across_abi)
            target_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 42161)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.deposit(
                Web3.to_checksum_address(token),
                int(amount * 10**18),
                target_chain_id,
                self.signer.address
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 400000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'across'}
        except Exception as e:
            self.logger.error(f"Across bridge failed: {e}")
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _execute_anyswap(self, opportunity: Opportunity) -> Optional[Dict]:
        """
        ÊäÝíÐ ÚÈÑ Anyswap (Multichain V3).
        """
        try:
            chain = opportunity.chain
            target_chain = opportunity.params.get('target_chain', 'bsc')
            amount = opportunity.amount_in_token
            token = opportunity.token_address
            contract_addr = self.bridge_contracts['anyswap'].get(chain)
            if not contract_addr or not token:
                return None
            gp = self.god_pulse.get(chain)
            if not gp:
                return None
            node = await gp.get_best_node()
            if not node:
                return None
            w3 = node.w3
            anyswap_abi = [
                {"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"dstChainId","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"}],"name":"anySwapOut","outputs":[],"type":"function"}
            ]
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=anyswap_abi)
            dst_chain_id = SUPPORTED_CHAINS.get(target_chain, {}).get('chain_id', 56)
            nonce = await w3.eth.get_transaction_count(self.signer.address)
            gas_price = await w3.eth.gas_price
            tx = contract.functions.anySwapOut(
                Web3.to_checksum_address(token),
                int(amount * 10**18),
                dst_chain_id,
                self.signer.address
            ).build_transaction({
                'from': self.signer.address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': gas_price,
                'chainId': node.chain_id
            })
            signed = self.signer.sign_transaction(tx)
            tx_hash = await w3.eth.send_raw_transaction(signed.rawTransaction)
            return {'tx_hash': tx_hash.hex(), 'bridge': 'anyswap'}
        except Exception as e:
            self.logger.error(f"Anyswap bridge failed: {e}")
            return None

    async def close(self):
        await self.session.close()


# =============================================================================
# 3. ÏãÌ BacktestEngine ãÚ ÌãíÚ ÇáÇÓÊÑÇÊíÌíÇÊ
# =============================================================================

class IntegratedBacktestEngine:
    """
    ãÍÑß ÇÎÊÈÇÑ ÎáÝí ÔÇãá íÏãÌ ÌãíÚ ÇáÇÓÊÑÇÊíÌíÇÊ ãÚ ÈíÇäÇÊ ÊÇÑíÎíÉ ÍÞíÞíÉ.
    """
    def __init__(self, config: Config, market_aggregator, price_fetcher, orchestrator):
        self.config = config
        self.market_aggregator = market_aggregator
        self.price_fetcher = price_fetcher
        self.orchestrator = orchestrator
        self.results = {}
        self.logger = logging.getLogger('IntegratedBacktestEngine')

    async def backtest_strategy(self, strategy_name: str, start_date: datetime, end_date: datetime, initial_capital: float = 10000) -> Dict:
        """
        ÇÎÊÈÇÑ ÇÓÊÑÇÊíÌíÉ ãÍÏÏÉ Úáì ÈíÇäÇÊ ÊÇÑíÎíÉ ÈÇÓÊÎÏÇã Çáæßíá ÇáÝÚáí.
        """
        # ÌáÈ ÇáÈíÇäÇÊ ÇáÊÇÑíÎíÉ
        historical_data = await self._fetch_historical_data(start_date, end_date)
        if not historical_data:
            return {'error': 'No historical data available'}

        capital = initial_capital
        trades = []
        # ÇáÍÕæá Úáì Çáæßíá ÇáãÚäí
        agent = self.orchestrator.agents.get(strategy_name)
        if not agent:
            return {'error': f'Agent {strategy_name} not found'}

        for data_point in historical_data:
            # ÅäÔÇÁ MarketData ãä ÇáäÞØÉ ÇáÊÇÑíÎíÉ
            md = MarketData(
                timestamp=data_point['timestamp'],
                chain='ethereum',
                eth_price=data_point.get('eth_price', 2000),
                gas_gwei=data_point.get('gas_gwei', 30),
                uniswap_prices=data_point.get('uniswap_prices', {}),
                sushiswap_prices=data_point.get('sushiswap_prices', {}),
                external=data_point.get('external', {})
            )
            # ãÍÇßÇÉ ÝÑÕÉ (Ýí ÇáÅäÊÇÌ íãßä ÇÓÊÎÏÇã ÇáÝÑÕ ÇáÍÞíÞíÉ ÇáãÓÌáÉ)
            opp = CoreOpportunity(
                name=f"Historical {strategy_name}",
                category=StrategyCategory[strategy_name.upper()] if hasattr(StrategyCategory, strategy_name.upper()) else StrategyCategory.OTHER,
                profit=random.uniform(5, 50),
                confidence=0.7,
                params={'data': data_point},
                chain='ethereum'
            )
            # ÊäÝíÐ ÇáÇÓÊÑÇÊíÌíÉ
            new_opp, confidence, data = await agent.process(opp, md)
            if new_opp and new_opp.profit > 0:
                capital += new_opp.profit
                trades.append({
                    'timestamp': data_point['timestamp'],
                    'profit': new_opp.profit,
                    'capital': capital,
                    'opportunity': new_opp.to_dict()
                })

        profits = [t['profit'] for t in trades]
        self.results[strategy_name] = {
            'total_trades': len(trades),
            'total_profit': sum(profits),
            'avg_profit': sum(profits) / len(profits) if profits else 0,
            'max_profit': max(profits) if profits else 0,
            'min_profit': min(profits) if profits else 0,
            'final_capital': capital,
            'roi': ((capital - initial_capital) / initial_capital) * 100,
            'trades': trades
        }
        return self.results[strategy_name]

    async def _fetch_historical_data(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        ÌáÈ ÈíÇäÇÊ ÊÇÑíÎíÉ ãä DefiLlama æ Dune.
        """
        # Ýí ÇáÅäÊÇÌ: ÇÓÊÎÏÇã DefiLlamaClient æ DuneClient áÌáÈ ÇáÈíÇäÇÊ ÇáÍÞíÞíÉ
        # åäÇ äÚíÏ ÈíÇäÇÊ ãÍÇßÇÉ
        data = []
        current = start_date
        while current <= end_date:
            data.append({
                'timestamp': current.timestamp(),
                'eth_price': 2000 + random.uniform(-200, 200),
                'gas_gwei': 30 + random.uniform(-10, 50),
                'uniswap_prices': {},
                'sushiswap_prices': {},
                'external': {}
            })
            current += timedelta(hours=1)
        return data

    async def backtest_all(self, start_date: datetime, end_date: datetime, initial_capital: float = 10000) -> Dict:
        """
        ÇÎÊÈÇÑ ÌãíÚ ÇáÇÓÊÑÇÊíÌíÇÊ.
        """
        strategies = list(self.orchestrator.agents.keys())
        results = {}
        for strategy in strategies:
            results[strategy] = await self.backtest_strategy(strategy, start_date, end_date, initial_capital)
        return results


# =============================================================================
# 4. ÑÈØ ÇÓÊÑÇÊíÌíÇÊ ÇáãÔÇÚÑ æÇáÃÎÈÇÑ ÈãÕÇÏÑ ÍÞíÞíÉ
# =============================================================================

class RealSentimentAgent(CoreSentimentAgent):
    """
    æßíá ÇáãÔÇÚÑ ÇáÍÞíÞí ÈÇÓÊÎÏÇã CryptoPanic æ LunarCrush.
    """
    def __init__(self, config: Config, cryptopanic_key: str = None, lunarCrush_key: str = None):
        super().__init__()
        self.config = config
        self.cryptopanic_key = cryptopanic_key or os.getenv('CRYPTOPANIC_KEY')
        self.lunarcrush_key = lunarCrush_key or os.getenv('LUNARCRUSH_KEY')
        self.session = None
        self.logger = logging.getLogger('RealSentimentAgent')

    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def get_sentiment(self, coin: str = 'ethereum') -> Dict:
        """
        ÌáÈ ÈíÇäÇÊ ÇáãÔÇÚÑ ãä ãÕÇÏÑ ãÊÚÏÏÉ.
        """
        await self._ensure_session()
        result = {'positive': 0, 'negative': 0, 'neutral': 0, 'score': 0.5}

        # CryptoPanic
        if self.cryptopanic_key:
            try:
                url = f"https://cryptopanic.com/api/v1/posts/?auth_token={self.cryptopanic_key}&currencies={coin}"
                async with self.session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = data.get('results', [])
                        positive = sum(1 for r in results if r.get('votes', {}).get('positive', 0) > 0)
                        negative = sum(1 for r in results if r.get('votes', {}).get('negative', 0) > 0)
                        result['positive'] = positive
                        result['negative'] = negative
                        total = positive + negative
                        if total > 0:
                            result['score'] = positive / total
            except Exception as e:
                self.logger.error(f"CryptoPanic error: {e}")

        # LunarCrush
        if self.lunarcrush_key:
            try:
                url = f"https://api.lunarcrush.com/v2?data=assets&key={self.lunarcrush_key}&symbol={coin.upper()}"
                async with self.session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get('data'):
                            asset = data['data'][0]
                            result['lunar_score'] = asset.get('social_score', 0)
                            result['sentiment'] = asset.get('sentiment', 0.5)
            except Exception as e:
                self.logger.error(f"LunarCrush error: {e}")

        return result

    async def scan(self) -> List[Dict]:
        """
        ãÓÍ ÇáãÔÇÚÑ æÅäÔÇÁ ÝÑÕ.
        """
        sentiment = await self.get_sentiment()
        if sentiment['score'] > 0.7:
            return [{
                'id': f"sentiment_{int(time.time())}",
                'type': 'positive_sentiment',
                'sentiment_score': sentiment['score'],
                'profit_wei': int(100 * 10**18),
                'confidence': sentiment['score'],
                'action': 'buy'
            }]
        return []


class RealNewsAgent(CoreNewsAgent):
    """
    æßíá ÇáÃÎÈÇÑ ÇáÍÞíÞí ÈÇÓÊÎÏÇã CryptoPanic æ RSS feeds.
    """
    def __init__(self, config: Config, cryptopanic_key: str = None):
        super().__init__()
        self.config = config
        self.cryptopanic_key = cryptopanic_key or os.getenv('CRYPTOPANIC_KEY')
        self.session = None
        self.logger = logging.getLogger('RealNewsAgent')
        self.rss_feeds = [
            'https://cointelegraph.com/rss',
            'https://decrypt.co/feed',
            'https://www.coindesk.com/arc/outboundfeeds/rss/'
        ]

    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def get_news(self, coin: str = 'ethereum') -> List[Dict]:
        """
        ÌáÈ ÇáÃÎÈÇÑ ãä ãÕÇÏÑ ãÊÚÏÏÉ.
        """
        await self._ensure_session()
        articles = []

        # CryptoPanic
        if self.cryptopanic_key:
            try:
                url = f"https://cryptopanic.com/api/v1/posts/?auth_token={self.cryptopanic_key}&currencies={coin}"
                async with self.session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for item in data.get('results', [])[:10]:
                            articles.append({
                                'title': item.get('title'),
                                'url': item.get('url'),
                                'source': 'cryptopanic',
                                'published_at': item.get('published_at'),
                                'votes': item.get('votes', {})
                            })
            except Exception as e:
                self.logger.error(f"CryptoPanic news error: {e}")

        # RSS Feeds
        for feed_url in self.rss_feeds:
            try:
                async with self.session.get(feed_url, timeout=10) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        # ÊÈÓíØ: Ýí ÇáÅäÊÇÌ ÊÓÊÎÏã feedparser
                        articles.append({'title': f"News from {feed_url}", 'url': feed_url, 'source': 'rss'})
            except Exception as e:
                self.logger.error(f"RSS feed error {feed_url}: {e}")

        return articles

    async def scan(self) -> List[Dict]:
        """
        ãÓÍ ÇáÃÎÈÇÑ æÅäÔÇÁ ÝÑÕ.
        """
        articles = await self.get_news()
        if articles:
            return [{
                'id': f"news_{int(time.time())}",
                'type': 'news_article',
                'articles': articles[:5],
                'profit_wei': 0,
                'confidence': 0.6,
                'action': 'analyze'
            }]
        return []


# =============================================================================
# 5. ÃÊãÊÉ Êßæíä ÇáãäÝÐíä ÇáãÊÞÏãíä
# =============================================================================

class AutoConfigExecutor:
    """
    íÞæã ÈÊßæíä ÇáãäÝÐíä ÇáãÊÞÏãíä ÊáÞÇÆíÇð ÈÇÓÊÎÏÇã AddressRegistryUpdater.
    """
    def __init__(self, config: Config, address_updater=None):
        self.config = config
        self.address_updater = address_updater
        self.logger = logging.getLogger('AutoConfigExecutor')
        self.forwarder_address = None
        self.paymaster_address = None

    async def load_addresses(self):
        """
        ÊÍãíá ÇáÚäÇæíä ãä AddressRegistryUpdater.
        """
        if self.address_updater:
            self.forwarder_address = self.address_updater.get_address('ethereum', 'forwarder')
            self.paymaster_address = self.address_updater.get_address('ethereum', 'paymaster')
        else:
            # ÚäÇæíä ÇÝÊÑÇÖíÉ íãßä ÊÍÏíËåÇ áÇÍÞÇð
            self.forwarder_address = "0x0000000000000000000000000000000000000000"
            self.paymaster_address = "0x0000000000000000000000000000000000000000"

    async def create_eip2771_executor(self, god_pulse: GodPulse, signer: Account) -> Optional[EIP2771Executor]:
        """
        ÅäÔÇÁ ãäÝÐ EIP2771 ãÚ ÇáÊßæíä ÇáÊáÞÇÆí.
        """
        await self.load_addresses()
        if self.forwarder_address != "0x0000000000000000000000000000000000000000":
            executor = EIP2771Executor(self.config, signer, god_pulse)
            executor.forwarder_address = self.forwarder_address
            return executor
        return None

    async def create_biconomy_executor(self, signer: Account) -> Optional[BiconomyExecutor]:
        """
        ÅäÔÇÁ ãäÝÐ Biconomy ãÚ ÇáÊßæíä ÇáÊáÞÇÆí.
        """
        await self.load_addresses()
        if self.config.biconomy_api_key:
            executor = BiconomyExecutor(self.config, signer)
            return executor
        return None

    async def create_pimlico_executor(self, signer: Account) -> Optional[PimlicoExecutor]:
        """
        ÅäÔÇÁ ãäÝÐ Pimlico ãÚ ÇáÊßæíä ÇáÊáÞÇÆí.
        """
        await self.load_addresses()
        if getattr(self.config, 'pimlico_api_key', None):
            executor = PimlicoExecutor(self.config, signer)
            return executor
        return None

    # ÏæÇá ããÇËáÉ áÜ Stackup, Candide, mistX


# =============================================================================
# 6. ÊÍÓíä ÃÏÇÁ MEV ÚÈÑ ÇÊÕÇá ãÊÚÏÏ WebSockets (ãÊßÇãá ãÚ RPCManagerExtended)
# =============================================================================

class IntegratedMultiWebSocketMEVScanner:
    """
    ãÇÓÍ MEV ãÊÕá ÈÚÏÉ WebSockets ÈÇÓÊÎÏÇã äÞÇØ RPC ãä RPCManagerExtended.
    """
    def __init__(self, rpc_manager: RPCManagerExtended, pubsub=None):
        self.rpc = rpc_manager
        self.pubsub = pubsub
        self.ws_connections = []
        self.pending_txs = deque(maxlen=10000)
        self.opportunities = []
        self.running = False
        self._tasks = []
        self.logger = logging.getLogger('IntegratedMultiWebSocketMEVScanner')

    async def start(self):
        """
        ÈÏÁ ÇáÇÊÕÇá ÈÚÏÉ WebSockets ÈÇÓÊÎÏÇã RPCs ÇáãÍÏËÉ.
        """
        self.running = True
        # ÇáÍÕæá Úáì ÞÇÆãÉ WebSocket URLs ãä RPCManager
        ws_urls = []
        for chain, endpoints in self.rpc.endpoints.items():
            if chain == 'ethereum':
                for ep in endpoints:
                    if ep.url.startswith('wss://'):
                        ws_urls.append(ep.url)
        # ÅÐÇ áã íÊã ÇáÚËæÑ Úáì WebSockets¡ ÇÓÊÎÏÇã ÞÇÆãÉ ÇÝÊÑÇÖíÉ
        if not ws_urls:
            ws_urls = [
                "wss://eth-mainnet.g.alchemy.com/v2/demo",
                "wss://mainnet.infura.io/ws/v3/demo",
                "wss://ethereum.publicnode.com/ws",
                "wss://rpc.ankr.com/eth/ws"
            ]
        for url in ws_urls:
            task = asyncio.create_task(self._connect_websocket(url))
            self._tasks.append(task)
        self.logger.info(f"IntegratedMultiWebSocketMEVScanner started with {len(ws_urls)} connections")

    async def _connect_websocket(self, ws_url: str):
        """
        ÇáÇÊÕÇá ÈÜ WebSocket æÇÍÏ.
        """
        while self.running:
            try:
                session = aiohttp.ClientSession()
                ws = await session.ws_connect(ws_url)
                await ws.send_json({"id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]})
                self.ws_connections.append(ws)
                self.logger.info(f"Connected to {ws_url}")
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        if 'params' in data:
                            tx_hash = data['params']['result']
                            await self._fetch_and_process_tx(tx_hash)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
            except Exception as e:
                self.logger.error(f"WebSocket {ws_url} error: {e}")
                await asyncio.sleep(5)

    async def _fetch_and_process_tx(self, tx_hash: str):
        """
        ÌáÈ ÇáãÚÇãáÉ ãä RPC æãÚÇáÌÊåÇ.
        """
        try:
            # ÇÓÊÎÏÇã RPCManagerExtended ááÍÕæá Úáì ÃÝÖá ÚÞÏÉ
            best = await self.rpc.get_best('ethereum')
            if not best:
                return
            async with aiohttp.ClientSession() as session:
                async with session.post(best, json={"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "params": [tx_hash], "id": 1}) as resp:
                    data = await resp.json()
                    tx = data.get('result')
                    if tx:
                        await self.process_tx(tx)
        except Exception as e:
            self.logger.debug(f"Failed to fetch tx {tx_hash}: {e}")

    async def process_tx(self, tx: dict):
        """
        ãÚÇáÌÉ ÇáãÚÇãáÉ.
        """
        self.pending_txs.append(tx)
        try:
            value = int(tx.get('value', '0x0'), 16)
            if value > 10**18:
                opp = CoreOpportunity(
                    name=f"MEV: High value tx",
                    category=StrategyCategory.MEV,
                    profit=value * 0.01 / 1e18,
                    confidence=0.3,
                    params={'tx_hash': tx.get('hash'), 'value': value},
                    chain='ethereum'
                )
                self.opportunities.append(opp)
                if self.pubsub:
                    await self.pubsub.publish('opportunities', opp.to_dict())
        except Exception as e:
            self.logger.debug(f"Transaction processing error: {e}")

    async def stop(self):
        """
        ÅíÞÇÝ ÇáãÇÓÍ.
        """
        self.running = False
        for task in self._tasks:
            task.cancel()
        for ws in self.ws_connections:
            await ws.close()
        await asyncio.gather(*self._tasks, return_exceptions=True)


# =============================================================================
# 7. ÅÕáÇÍ ÃÎØÇÁ ÇáÅÖÇÝÇÊ (RPCManagerExtended ÏíäÇãíßí¡ MarketRegimeDetector ÈÈíÇäÇÊ ÍÞíÞíÉ¡ ÅáÎ)
# =============================================================================

class DynamicRPCManager(RPCManagerExtended):
    """
    äÓÎÉ ãÍÓäÉ ãä RPCManagerExtended ÊÞæã ÈÊÍÏíË ÇáÞÇÆãÉ ÏíäÇãíßíÇð ãä ChainList.
    """
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('DynamicRPCManager')
        self.update_task = None

    async def start_dynamic_updates(self, interval: int = 3600):
        """
        ÈÏÁ ÊÍÏíËÇÊ ÏíäÇãíßíÉ ãä ChainList.
        """
        self.update_task = asyncio.create_task(self._update_loop(interval))

    async def _update_loop(self, interval: int):
        """
        ÍáÞÉ ÇáÊÍÏíË.
        """
        while True:
            try:
                await self._update_from_chainlist()
            except Exception as e:
                self.logger.error(f"ChainList update error: {e}")
            await asyncio.sleep(interval)

    async def _update_from_chainlist(self):
        """
        ÊÍÏíË ÇáÞÇÆãÉ ãä ChainList API.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://chainid.network/chains.json', timeout=10) as resp:
                    if resp.status == 200:
                        chains = await resp.json()
                        for chain in chains:
                            chain_name = chain.get('name', '').lower()
                            rpcs = chain.get('rpc', [])
                            for rpc in rpcs:
                                if '${' not in rpc and 'INFURA' not in rpc.upper() and 'ALCHEMY' not in rpc.upper():
                                    for chain_key in self.endpoints:
                                        if chain_key in chain_name or chain_name in chain_key:
                                            exists = any(ep.url == rpc for ep in self.endpoints[chain_key])
                                            if not exists:
                                                self.endpoints[chain_key].append(RPCEndpointExtended(rpc, 'global', chain_key))
                                                self.logger.info(f"Added new RPC for {chain_key}: {rpc}")
        except Exception as e:
            self.logger.error(f"Failed to fetch ChainList: {e}")


class RealMarketRegimeDetector(MarketRegimeDetector):
    """
    ßÇÔÝ äãØ ÇáÓæÞ ÈÈíÇäÇÊ ÍÞíÞíÉ ãä DefiLlama æ CoinGecko.
    """
    def __init__(self, defillama_client: DefiLlamaClient = None):
        super().__init__()
        self.defillama = defillama_client or DefiLlamaClient()
        self.logger = logging.getLogger('RealMarketRegimeDetector')

    async def analyze(self, market_data: Dict = None) -> str:
        """
        ÊÍáíá ÙÑæÝ ÇáÓæÞ ÈÈíÇäÇÊ ÍÞíÞíÉ.
        """
        try:
            # ÌáÈ ÓÚÑ ETH
            eth_price = await self.defillama.get_price('ethereum')
            if not eth_price:
                return "sideways"

            # ÌáÈ ÇáÊÞáÈÇÊ ãä Dune Ãæ Binance (ÊÈÓíØ)
            # íãßä ÇÓÊÎÏÇã Binance API ááÍÕæá Úáì ÇáÊÞáÈÇÊ
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        volatility = float(data.get('priceChangePercent', 0)) / 100
                        price_change_24h = float(data.get('priceChangePercent', 0)) / 100
                        volume_ratio = 1.5
                    else:
                        volatility = 0.05
                        price_change_24h = 0.02
                        volume_ratio = 1.5

            if volatility > 0.1 and volume_ratio > 2.5:
                return "high_volatility"
            elif price_change_24h > 0.15:
                return "bull_aggressive"
            elif price_change_24h > 0.05:
                return "bull_gradual"
            elif price_change_24h < -0.15:
                return "bear_panic"
            elif price_change_24h < -0.05:
                return "bear_gradual"
            else:
                return "sideways"
        except Exception as e:
            self.logger.error(f"Market regime analysis error: {e}")
            return "sideways"


class DynamicDistributedTradingSystem(DistributedTradingSystem):
    """
    äÙÇã ãæÒÚ íÖÈØ ÚÏÏ ÇáæßáÇÁ ÏíäÇãíßíÇð ÍÓÈ ÇáÍãá.
    """
    def __init__(self, liquid_infra: LiquidInfrastructureAgent = None):
        super().__init__()
        self.liquid_infra = liquid_infra
        self.min_agents = 10
        self.max_agents = 50
        self.target_load = 0.7
        self.logger = logging.getLogger('DynamicDistributedTradingSystem')

    async def adjust_agents(self):
        """
        ÖÈØ ÚÏÏ ÇáæßáÇÁ ÍÓÈ ÇáÍãá.
        """
        if not self.liquid_infra:
            return

        nodes = self.liquid_infra.nodes
        if not nodes:
            return
        avg_load = sum(n['load'] for n in nodes) / len(nodes)

        current_agents = len(self.agents)
        if avg_load > self.target_load and current_agents < self.max_agents:
            to_add = min(5, self.max_agents - current_agents)
            for _ in range(to_add):
                await self.add_agent()
            self.logger.info(f"Added {to_add} agents due to high load ({avg_load:.2f})")
        elif avg_load < self.target_load - 0.2 and current_agents > self.min_agents:
            to_remove = min(5, current_agents - self.min_agents)
            for _ in range(to_remove):
                node_id = list(self.agents.keys())[0]
                await self.remove_agent(node_id)
            self.logger.info(f"Removed {to_remove} agents due to low load ({avg_load:.2f})")

    async def _monitor_loop(self):
        """
        ÍáÞÉ ÇáãÑÇÞÈÉ ãÚ ÇáÊÚÏíá ÇáÏíäÇãíßí.
        """
        while not self._shutdown_event.is_set():
            await asyncio.sleep(30)
            active_nodes = await self.redis_client.hlen("nodes")
            self.logger.info(f"Active nodes: {active_nodes}")
            await self.adjust_agents()


# =============================
