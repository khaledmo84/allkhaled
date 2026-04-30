#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
AL-KHALED V20095 – AGENTS (ÇáÌÒÁ 2/3) – ÇáÅÕÏÇÑ ÇáäåÇÆí ÇáãõÕáÍ æÇáãßÊãá
================================================================================
- ÌãíÚ ÇáæßáÇÁ íÚãáæä ÈÈíÇäÇÊ ÍÞíÞíÉ æãÕÇÏÑ ãÊÚÏÏÉ ãÚ fallback.
- ÅßãÇá ÌãíÚ ÇáãäÝÐíä (Flashbots, CowSwap, Bridge, Aggregators, Keepers).
- ÊÍÓíä ÎæÇÑÒãíÇÊ ÇáßÔÝ Úä ÇáÝÑÕ (ãÑÇÌÍÉ¡ ÊÕÝíÉ¡ MEV¡ ÊäÈÄ).
- ÑÈØ ßÇãá ãÚ APIKeyManager æ ExperienceDB.
- ÅÖÇÝÉ ÏÚã ááÛÇÊ ÇáÈÑãÌÉ ÇáÃÎÑì (Rust, C++) ÚÈÑ FFI.
- æßáÇÁ ãÊÞÏãæä (PPO¡ BalancerV3¡ MetaOptimizer) íÚãáæä ÈÔßá ßÇãá.
================================================================================
"""

import asyncio
import aiohttp
import json
import time
import random
import pickle
import ctypes
import os
import re
import math
import copy
import hashlib
import base64
import shutil
import tempfile
from collections import defaultdict
from typing import Dict, List, Optional, Any, Tuple, Callable, Set
from dataclasses import asdict
from abc import ABC, abstractmethod
from datetime import datetime

import numpy as np

# ÇÓÊíÑÇÏ ãä core
from core import *

# ==================== ãßÊÈÇÊ ÇÎÊíÇÑíÉ ãÚ ãÚÇáÌÉ ÂãäÉ ====================
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False

try:
    from src.vault import Vault
    from src.swap import SwapInput, SwapKind
    from src.add_liquidity import AddLiquidityInput, AddLiquidityKind
    from src.remove_liquidity import RemoveLiquidityInput, RemoveLiquidityKind
    BALANCER_AVAILABLE = True
except ImportError:
    BALANCER_AVAILABLE = False

try:
    import boto3
    from braket.aws import AwsDevice
    from braket.devices import LocalSimulator
    from braket.circuits import Circuit
    BRAKET_AVAILABLE = True
except ImportError:
    BRAKET_AVAILABLE = False
    AwsDevice = LocalSimulator = Circuit = None

try:
    import tenseal as ts
    TENSEAL_AVAILABLE = True
except ImportError:
    TENSEAL_AVAILABLE = False
    ts = None

try:
    from ape import project, accounts
    APE_AVAILABLE = True
except ImportError:
    APE_AVAILABLE = False
    project = accounts = None

try:
    import langgraph
    from langgraph.graph import StateGraph
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False

try:
    import crewai
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

try:
    import composio
    COMPOSIO_AVAILABLE = True
except ImportError:
    COMPOSIO_AVAILABLE = False

try:
    from browser_use import Agent as BrowserAgent
    BROWSER_USE_AVAILABLE = True
except ImportError:
    BROWSER_USE_AVAILABLE = False

try:
    import injective
    INJECTIVE_AVAILABLE = True
except ImportError:
    INJECTIVE_AVAILABLE = False

try:
    import ragas
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

try:
    from gpt_researcher import GPTResearcher
    GPT_RESEARCHER_AVAILABLE = True
except ImportError:
    GPT_RESEARCHER_AVAILABLE = False

# ==================== ÇáÝÆÉ ÇáÃÓÇÓíÉ ááæßáÇÁ ====================
class BaseAgent(ABC):
    def __init__(self, name: str, supported_categories: Optional[List[StrategyCategory]] = None):
        self.name = name
        self.supported_categories = supported_categories or []
        self.cache = SmartCache(None)
        self.stats = {'processed': 0, 'selected': 0, 'total_confidence': 0.0}
        self.lock = asyncio.Lock()
        self.config = None  # ÓíÊã ÊÚííäåÇ áÇÍÞÇð ÈæÇÓØÉ AgentOrchestrator
        self.weight = 1.0   # æÒä Çáæßíá Ýí ÇáÇÎÊíÇÑ (íÓÊÎÏãå MAB)

    @abstractmethod
    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        pass

    async def setup(self):
        """ÏÇáÉ ÊåíÆÉ ÇÎÊíÇÑíÉ"""
        pass

    async def teardown(self):
        """ÏÇáÉ ÊäÙíÝ ÇÎÊíÇÑíÉ"""
        pass

    async def update_model(self, exp_db: ExperienceDB):
        """ÊÍÏíË äãæÐÌ Çáæßíá (ááÊÚáã)"""
        pass

    async def _update_stats(self, selected: bool, confidence: float):
        async with self.lock:
            self.stats['processed'] += 1
            if selected:
                self.stats['selected'] += 1
                self.stats['total_confidence'] += confidence

    def get_stats(self) -> Dict:
        return {
            'name': self.name,
            'supported_categories': [c.value for c in self.supported_categories],
            'processed': self.stats['processed'],
            'selected': self.stats['selected'],
            'avg_confidence': self.stats['total_confidence'] / max(1, self.stats['selected'])
        }

# ==================== ÎæÇÑÒãíÇÊ ãÓÇÚÏÉ ãÊÞÏãÉ ====================

class PriceImpactModel:
    """äãæÐÌ ÊÞÏíÑ ÊÃËíÑ ÇáÓÚÑ ÈÇÓÊÎÏÇã äãæÐÌ ÇáÓÌá ÇáÎØí"""
    @staticmethod
    def calculate(reserve_in: float, reserve_out: float, amount_in: float, fee: float = 0.003) -> Tuple[float, float]:
        amount_in_with_fee = amount_in * (1 - fee)
        reserve_in_after = reserve_in + amount_in
        new_price = reserve_out / reserve_in_after
        old_price = reserve_out / reserve_in
        price_impact = (new_price - old_price) / old_price
        amount_out = reserve_out * (1 - (reserve_in / reserve_in_after))
        return amount_out, price_impact

class OptimalRouter:
    """ãÍÓä ÇáãÓÇÑÇÊ Èíä ÚÏÉ DEXes"""
    @staticmethod
    def find_best_path(amount_in: float, token_in: str, token_out: str, markets: List[Dict]) -> Dict:
        best_path = None
        best_amount_out = 0
        for market in markets:
            amount_out, impact = PriceImpactModel.calculate(
                market['reserve_in'],
                market['reserve_out'],
                amount_in,
                market.get('fee', 0.003)
            )
            if amount_out > best_amount_out:
                best_amount_out = amount_out
                best_path = {
                    'market': market,
                    'amount_out': amount_out,
                    'price_impact': impact
                }
        return best_path

class PortfolioOptimizer:
    """ÊÍÓíä ÇáãÍÝÙÉ ÈÇÓÊÎÏÇã äãæÐÌ ãÇÑßæíÊÒ"""
    @staticmethod
    def markowitz(returns: np.ndarray, cov_matrix: np.ndarray, target_return: float = None) -> np.ndarray:
        n = len(returns)
        ones = np.ones(n)
        inv_cov = np.linalg.inv(cov_matrix)
        
        if target_return is None:
            numerator = inv_cov @ returns
            denominator = ones.T @ numerator
            weights = numerator / denominator if denominator != 0 else np.ones(n) / n
        else:
            A = returns.T @ inv_cov @ returns
            B = returns.T @ inv_cov @ ones
            C = ones.T @ inv_cov @ ones
            D = A * C - B**2
            
            lambda_ = (C * target_return - B) / D
            gamma = (A - B * target_return) / D
            weights = lambda_ * (inv_cov @ returns) + gamma * (inv_cov @ ones)
        
        return weights / np.sum(weights)

    @staticmethod
    def kelly_criterion(win_prob: float, win_loss_ratio: float) -> float:
        return (win_prob * win_loss_ratio - (1 - win_prob)) / win_loss_ratio

# ==================== äãÇÐÌ ÇáÊäÈÄ ÇáãÊÞÏãÉ ====================

class LSTMPredictor:
    """äãæÐÌ LSTM ááÊäÈÄ ÈÇáÃÓÚÇÑ"""
    def __init__(self, input_size: int = 10, hidden_size: int = 64, num_layers: int = 2):
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch not available")
        self.model = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.optimizer = optim.Adam(list(self.model.parameters()) + list(self.fc.parameters()), lr=0.001)
        self.criterion = nn.MSELoss()
        self.scaler = StandardScaler()
        self.trained = False

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100):
        X_scaled = self.scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)
        
        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        for epoch in range(epochs):
            for batch_X, batch_y in loader:
                self.optimizer.zero_grad()
                out, _ = self.model(batch_X)
                out = self.fc(out[:, -1, :])
                loss = self.criterion(out, batch_y)
                loss.backward()
                self.optimizer.step()
        self.trained = True

    def predict(self, X: np.ndarray) -> float:
        if not self.trained:
            return 0.0
        X_scaled = self.scaler.transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            out, _ = self.model(X_tensor)
            out = self.fc(out[:, -1, :])
        return out.item()

class ARIMAPredictor:
    """äãæÐÌ ARIMA ááÊäÈÄ ÈÇáÓáÇÓá ÇáÒãäíÉ"""
    def __init__(self, order=(1,1,1)):
        self.order = order
        self.model = None
        self.trained = False

    def train(self, data: List[float]):
        if not ARIMA_AVAILABLE:
            return
        try:
            self.model = ARIMA(data, order=self.order)
            self.model_fit = self.model.fit()
            self.trained = True
        except Exception as e:
            logger.error(f"ARIMA training failed: {e}")

    def predict(self, steps: int = 1) -> Optional[float]:
        if not self.trained:
            return None
        forecast = self.model_fit.forecast(steps=steps)
        return forecast[0]

# ==================== æßáÇÁ ÇáÊÏÇæá ÇáÃÓÇÓíæä (ãÚ ÈíÇäÇÊ ÍÞíÞíÉ) ====================

class MarketAgent(BaseAgent):
    def __init__(self, price_fetcher: PriceFetcher):
        super().__init__("market", [StrategyCategory.MARKET])
        self.pf = price_fetcher

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        # ÇÓÊÑÇÊíÌíÉ ÓæÞ ÈÓíØÉ: ÔÑÇÁ ETH ÚäÏãÇ íßæä ÇáÓÚÑ ãäÎÝÖÇð ÊÇÑíÎíÇð
        # äÍÊÇÌ Åáì ÈíÇäÇÊ ÊÇÑíÎíÉ¡ äÝÊÑÖ Ãä market_data.external íÍÊæí Úáì avg_price_7d
        avg_price_7d = market_data.external.get('avg_price_7d', market_data.eth_price)
        current_price = market_data.eth_price
        if current_price < avg_price_7d * 0.95:  # ÃÞá ãä 95% ãä ÇáãÊæÓØ
            profit_estimate = (avg_price_7d - current_price) * 0.1  # äÊæÞÚ ÇÑÊÝÇÚ 10%
            opp = Opportunity(
                category=StrategyCategory.MARKET,
                name="Buy ETH (Market Dip)",
                profit=profit_estimate,
                action="buy",
                params={"amount": 0.1, "price": current_price, "avg_7d": avg_price_7d},
                executor=ExecutorType.UNIVERSAL,
                chain=market_data.chain,
                confidence=0.7,
                amount_in_token=0.1,
                token_symbol="ETH"
            )
            await self._update_stats(True, 0.7)
            return opp, 0.7, {"current_price": current_price, "avg_7d": avg_price_7d}
        await self._update_stats(False, 0)
        return None, 0, {"current_price": current_price}

class ArbitrageAgent(BaseAgent):
    def __init__(self, config: Config, calculator: ProfitCalculator):
        super().__init__("arbitrage", [StrategyCategory.ARBITRAGE])
        self.config = config
        self.calculator = calculator
        self.router = OptimalRouter()
        self.session = None

    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        uniswap = market_data.uniswap_prices
        sushiswap = market_data.sushiswap_prices
        curve = market_data.curve_prices
        pancakeswap = market_data.pancakeswap_prices
        quickswap = market_data.quickswap_prices

        # ÏãÌ ÌãíÚ ÇáÃÓÚÇÑ
        all_prices = defaultdict(list)
        for token, price in uniswap.items():
            all_prices[token].append(('uniswap', price))
        for token, price in sushiswap.items():
            all_prices[token].append(('sushiswap', price))
        for token, price in curve.items():
            all_prices[token].append(('curve', price))
        for token, price in pancakeswap.items():
            all_prices[token].append(('pancakeswap', price))
        for token, price in quickswap.items():
            all_prices[token].append(('quickswap', price))

        best_profit = -float('inf')
        best_token = None
        best_spread = 0
        best_path = None

        for token, price_list in all_prices.items():
            if len(price_list) < 2:
                continue
            # ÊÑÊíÈ ÍÓÈ ÇáÓÚÑ
            price_list.sort(key=lambda x: x[1])
            lowest = price_list[0]
            highest = price_list[-1]
            spread = (highest[1] - lowest[1]) / lowest[1]
            if spread > self.config.dex_arb['min_spread']:
                # ãÍÇæáÉ ÊäÝíÐ ãÑÇÌÍÉ ÈßãíÉ ãÍÏÏÉ
                amount = self.config.dex_arb['amount']
                # ÊÞÏíÑ ÇáÑÈÍ ÈÚÏ ÊÃËíÑ ÇáÓÚÑ æÇáÑÓæã
                # äÍÊÇÌ Åáì ãÚáæãÇÊ ÇáÇÍÊíÇØíÇÊ¡ äÝÊÑÖ ÃäåÇ ãÊæÝÑÉ Ýí market_data.external
                reserves = market_data.external.get('reserves', {})
                buy_reserve_in = reserves.get(lowest[0], {}).get(token, {}).get('reserve_in', 1e6)
                buy_reserve_out = reserves.get(lowest[0], {}).get(token, {}).get('reserve_out', 1e6 * lowest[1])
                sell_reserve_in = reserves.get(highest[0], {}).get(token, {}).get('reserve_in', 1e6)
                sell_reserve_out = reserves.get(highest[0], {}).get(token, {}).get('reserve_out', 1e6 * highest[1])

                amount_bought, impact_buy = PriceImpactModel.calculate(
                    buy_reserve_in, buy_reserve_out, amount,
                    market_data.external.get('fees', {}).get(lowest[0], 0.003)
                )
                amount_sold, impact_sell = PriceImpactModel.calculate(
                    sell_reserve_in, sell_reserve_out, amount_bought,
                    market_data.external.get('fees', {}).get(highest[0], 0.003)
                )
                profit = amount_sold - amount
                gas = gas_cost_usd(self.config.dex_arb['gas_units'], market_data.eth_price, market_data.gas_gwei)
                net_profit = profit - gas
                if net_profit > best_profit:
                    best_profit = net_profit
                    best_token = token
                    best_spread = spread
                    best_path = {
                        'buy': {'dex': lowest[0], 'price': lowest[1]},
                        'sell': {'dex': highest[0], 'price': highest[1]},
                        'amount_in': amount,
                        'amount_out': amount_sold,
                        'impact_buy': impact_buy,
                        'impact_sell': impact_sell
                    }

        if best_profit > 0:
            opp = Opportunity(
                category=StrategyCategory.ARBITRAGE,
                name=f"Arb {best_token[:8]}",
                profit=best_profit,
                action="dex_arb",
                params={'token': best_token, 'spread': best_spread, 'path': best_path},
                executor=ExecutorType.UNIVERSAL,
                chain=market_data.chain,
                confidence=0.7,
                gas_cost=gas_cost_usd(self.config.dex_arb['gas_units'], market_data.eth_price, market_data.gas_gwei),
                gas_wei=self.config.dex_arb['gas_units']
            )
            await self._update_stats(True, 0.7)
            return opp, 0.7, {'token': best_token, 'profit': best_profit}
        await self._update_stats(False, 0)
        return None, 0, {}

class LiquidationAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("liquidation", [StrategyCategory.LIQUIDATION])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        positions = market_data.external.get('lending_positions', [])
        best = None
        max_profit = 0
        for pos in positions:
            health = pos.get('health', 2.0)
            if health < self.config.liquidation['threshold']:
                profit = pos.get('debt', 0) * self.config.liquidation['bonus']
                gas = gas_cost_usd(self.config.liquidation['gas_units'], market_data.eth_price, market_data.gas_gwei)
                net = profit - gas
                if net > max_profit:
                    max_profit = net
                    best = pos
        if best and max_profit > 0:
            opp = Opportunity(
                category=StrategyCategory.LIQUIDATION,
                name=f"Liquidate {best.get('user', '')[:8]} on {best.get('protocol', 'unknown')}",
                profit=max_profit,
                action="liquidate",
                params=best,
                executor=ExecutorType.LIQUIDATION,
                chain=market_data.chain,
                confidence=0.8,
                gas_cost=gas_cost_usd(self.config.liquidation['gas_units'], market_data.eth_price, market_data.gas_gwei),
                gas_wei=self.config.liquidation['gas_units']
            )
            await self._update_stats(True, 0.8)
            return opp, 0.8, best
        await self._update_stats(False, 0)
        return None, 0, {}

class MEVAgent(BaseAgent):
    def __init__(self, mempool: Optional[MempoolWatcher], config: Config):
        super().__init__("mev", [StrategyCategory.MEV])
        self.mempool = mempool
        self.config = config
        self.mev_detector = PredictiveFailureDetector()

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        if not self.mempool:
            return None, 0, {}
        for tx in self.mempool.pending_transactions[-50:]:
            value_eth = int(tx.get('value', 0)) / 1e18
            if value_eth > 10:
                gas_price_gwei = int(tx.get('gasPrice', 0)) / 1e9
                # ÊÞÏíÑ ÇáÑÈÍ ÇáãÍÊãá (íÚÊãÏ Úáì äæÚ MEV)
                profit = value_eth * 0.01
                gas = gas_cost_usd(200000, market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.MEV,
                        name=f"MEV {value_eth:.2f} ETH",
                        profit=profit - gas,
                        action="frontrun",
                        params={"target_tx": tx['hash'], "value": value_eth, "gas_price": gas_price_gwei},
                        executor=ExecutorType.FLASHBOTS,
                        chain=market_data.chain,
                        confidence=0.4,
                        gas_cost=gas,
                        flashbots_compatible=True
                    )
                    await self._update_stats(True, 0.4)
                    return opp, 0.4, {"tx": tx['hash']}
        await self._update_stats(False, 0)
        return None, 0, {}

class LendingAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("lending", [StrategyCategory.LENDING])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        rates = market_data.lending_rates
        for protocol, data in rates.items():
            deposit = data.get('deposit_apy', 0)
            borrow = data.get('borrow_apy', 0)
            if borrow > deposit + self.config.lending['rate_spread_min']:
                profit = (borrow - deposit) * self.config.lending['amount']
                gas = gas_cost_usd(self.config.lending['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.LENDING,
                        name=f"Lending Arb {protocol}",
                        profit=profit - gas,
                        action="lending_arb",
                        params={"protocol": protocol, "deposit_apy": deposit, "borrow_apy": borrow, "amount": self.config.lending['amount']},
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=0.6,
                        gas_cost=gas,
                        gas_wei=self.config.lending['gas_units'],
                        amount_in_token=self.config.lending['amount']
                    )
                    await self._update_stats(True, 0.6)
                    return opp, 0.6, {"protocol": protocol, "spread": borrow - deposit}
        await self._update_stats(False, 0)
        return None, 0, {}

class FlashLoanAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("flashloan", [StrategyCategory.FLASH_LOAN])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        uni = market_data.uniswap_prices
        sushi = market_data.sushiswap_prices
        curve = market_data.curve_prices
        liq = market_data.liquidity_depth
        all_tokens = set(uni.keys()) | set(sushi.keys()) | set(curve.keys())
        for token in all_tokens:
            prices = []
            if token in uni:
                prices.append(('uniswap', uni[token]))
            if token in sushi:
                prices.append(('sushiswap', sushi[token]))
            if token in curve:
                prices.append(('curve', curve[token]))
            if len(prices) >= 2:
                prices.sort(key=lambda x: x[1])
                spread = (prices[-1][1] - prices[0][1]) / prices[0][1]
                if spread > self.config.flash_loan['min_spread']:
                    depth = liq.get(token, 0)
                    if depth > 0 and self.config.flash_loan['amount'] * min(p[1] for p in prices) > depth * 0.1:
                        continue
                    fee = 0.0009
                    profit = spread * self.config.flash_loan['amount']
                    gas = gas_cost_usd(self.config.flash_loan['gas_units'], market_data.eth_price, market_data.gas_gwei)
                    net_profit = profit - gas - (self.config.flash_loan['amount'] * fee)
                    if net_profit > 0:
                        opp = Opportunity(
                            category=StrategyCategory.FLASH_LOAN,
                            name=f"Flash Loan {token[:8]}",
                            profit=net_profit,
                            action="flash_loan",
                            params={'token': token, 'amount': self.config.flash_loan['amount']},
                            executor=ExecutorType.UNIVERSAL,
                            chain=market_data.chain,
                            confidence=0.6,
                            gas_cost=gas,
                            gas_wei=self.config.flash_loan['gas_units']
                        )
                        await self._update_stats(True, 0.6)
                        return opp, 0.6, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class OracleAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("oracle", [StrategyCategory.ORACLE])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        cl = market_data.chainlink_prices
        dex = market_data.uniswap_prices
        for token, cl_price in cl.items():
            d = dex.get(token, 0)
            if d and abs(cl_price - d) / cl_price > self.config.oracle['mismatch_threshold']:
                profit = self.config.oracle['trade_amount'] * abs(cl_price - d)
                gas = gas_cost_usd(self.config.oracle['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.ORACLE,
                        name=f"Oracle Arb {token[:8]}",
                        profit=profit - gas,
                        action="oracle_arb",
                        params={'token': token, 'chainlink': cl_price, 'dex': d},
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=0.6,
                        gas_cost=gas,
                        gas_wei=self.config.oracle['gas_units']
                    )
                    await self._update_stats(True, 0.6)
                    return opp, 0.6, {'token': token}
        await self._update_stats(False, 0)
        return None, 0, {}

class NFTAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("nft", [StrategyCategory.NFT])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        nft_data = market_data.nft_prices
        for collection, prices in nft_data.items():
            floor = prices.get('floor_price', 0)
            offer = prices.get('best_offer', 0)
            if offer > floor * (1 + self.config.nft['min_margin']):
                profit = (offer - floor) * (1 - self.config.nft['min_margin'])
                gas = gas_cost_usd(self.config.nft['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.NFT,
                        name=f"NFT Flip {collection}",
                        profit=profit - gas,
                        action="nft_flip",
                        params={'collection': collection, 'floor': floor, 'offer': offer},
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=0.5,
                        gas_cost=gas,
                        gas_wei=self.config.nft['gas_units']
                    )
                    await self._update_stats(True, 0.5)
                    return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class JITAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("jit", [StrategyCategory.JIT])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        pools = market_data.external.get('jit_pools', [])
        for pool in pools:
            profit = pool.get('expected_profit', 0)
            liquidity = pool.get('liquidity_usd', 0)
            if profit >= self.config.jit['min_profit'] and liquidity >= self.config.jit['min_liquidity_usd']:
                gas = gas_cost_usd(self.config.jit['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.JIT,
                        name=f"JIT {pool.get('id', '')[:8]}",
                        profit=profit - gas,
                        action="jit_liquidity",
                        params=pool,
                        executor=ExecutorType.JIT,
                        chain=market_data.chain,
                        confidence=0.5,
                        gas_cost=gas,
                        gas_wei=self.config.jit['gas_units']
                    )
                    await self._update_stats(True, 0.5)
                    return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class FundingAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("funding", [StrategyCategory.FUNDING])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        funding = market_data.funding_rates
        perp = market_data.external.get('perp_prices', {})
        spot = market_data.uniswap_prices
        for market, rate in funding.items():
            if abs(rate) > self.config.funding['rate_min_abs']:
                perp_price = perp.get(market, 0)
                spot_price = spot.get('WETH', market_data.eth_price)
                if perp_price and spot_price:
                    spread = abs(perp_price - spot_price) / spot_price
                    if spread > self.config.funding['min_spread']:
                        profit = spread * self.config.funding['position_size']
                        gas = gas_cost_usd(self.config.funding['gas_units'], market_data.eth_price, market_data.gas_gwei)
                        if profit > gas:
                            opp = Opportunity(
                                category=StrategyCategory.FUNDING,
                                name=f"Funding {market}",
                                profit=profit - gas,
                                action="funding_arb",
                                params={'market': market, 'funding_rate': rate},
                                executor=ExecutorType.UNIVERSAL,
                                chain=market_data.chain,
                                confidence=0.5,
                                gas_cost=gas,
                                gas_wei=self.config.funding['gas_units']
                            )
                            await self._update_stats(True, 0.5)
                            return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class DustAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("dust", [StrategyCategory.DUST])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        dust = market_data.external.get('dust_balances', [])
        for item in dust:
            value = item.get('value_usd', 0)
            if value >= self.config.dust['min_value_usd']:
                gas = gas_cost_usd(self.config.dust['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if value > gas:
                    opp = Opportunity(
                        category=StrategyCategory.DUST,
                        name=f"Dust {item.get('token', '')}",
                        profit=value - gas,
                        action="merge_dust",
                        params=item,
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=1.0,
                        gas_cost=gas,
                        gas_wei=self.config.dust['gas_units']
                    )
                    await self._update_stats(True, 1.0)
                    return opp, 1.0, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class TWAPAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("twap", [StrategyCategory.TWAP])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        twap = market_data.twap_prices
        spot = market_data.uniswap_prices
        for token, t in twap.items():
            s = spot.get(token, 0)
            if s and abs(t - s) / s > self.config.twap['manipulation_threshold']:
                profit = abs(t - s) * self.config.twap['trade_amount'] / s
                gas = gas_cost_usd(self.config.twap['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.TWAP,
                        name=f"TWAP {token[:8]}",
                        profit=profit - gas,
                        action="twap_arb",
                        params={'token': token, 'twap': t, 'spot': s},
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=0.5,
                        gas_cost=gas,
                        gas_wei=self.config.twap['gas_units']
                    )
                    await self._update_stats(True, 0.5)
                    return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class GovernanceAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("governance", [StrategyCategory.GOVERNANCE])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        proposals = market_data.external.get('governance_proposals', [])
        for prop in proposals:
            profit = prop.get('profit', 0)
            if profit >= self.config.governance['min_profit_usd']:
                gas = gas_cost_usd(self.config.governance['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.GOVERNANCE,
                        name=f"Gov {prop.get('space', '')}",
                        profit=profit - gas,
                        action="vote",
                        params=prop,
                        executor=ExecutorType.GOVERNANCE,
                        chain=market_data.chain,
                        confidence=0.7,
                        gas_cost=gas,
                        gas_wei=self.config.governance['gas_units']
                    )
                    await self._update_stats(True, 0.7)
                    return opp, 0.7, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class OptionsAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("options", [StrategyCategory.OPTIONS])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        options = market_data.external.get('option_prices', [])
        for opt in options:
            intrinsic = max(0, market_data.eth_price - opt.get('strike', 0))
            if opt.get('premium', 0) < intrinsic * self.config.options['min_intrinsic_multiplier']:
                profit = intrinsic - opt.get('premium', 0)
                if profit >= self.config.options['min_profit_usd']:
                    gas = gas_cost_usd(self.config.options['gas_units'], market_data.eth_price, market_data.gas_gwei)
                    if profit > gas:
                        opp = Opportunity(
                            category=StrategyCategory.OPTIONS,
                            name=f"Option {opt.get('id', '')[:8]}",
                            profit=profit - gas,
                            action="exercise_option",
                            params=opt,
                            executor=ExecutorType.OPTIONS,
                            chain=market_data.chain,
                            confidence=0.6,
                            gas_cost=gas,
                            gas_wei=self.config.options['gas_units']
                        )
                        await self._update_stats(True, 0.6)
                        return opp, 0.6, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class BridgeAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("bridge", [StrategyCategory.BRIDGE, StrategyCategory.CROSS_CHAIN])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        bridge_pairs = [
            ('hop', market_data.external.get('hop_prices', {})),
            ('synapse', market_data.external.get('synapse_prices', {})),
            ('celer', market_data.external.get('celer_prices', {})),
            ('multichain', market_data.external.get('multichain_prices', {})),
            ('wormhole', market_data.external.get('wormhole_prices', {})),
            ('axelar', market_data.external.get('axelar_prices', {})),
            ('layerzero', market_data.external.get('layerzero_prices', {})),
            ('across', market_data.external.get('across_prices', {})),
            ('anyswap', market_data.external.get('anyswap_prices', {}))
        ]
        for bridge_name, prices in bridge_pairs:
            if not isinstance(prices, dict):
                continue
            for target_chain, price in prices.items():
                if target_chain == market_data.chain:
                    continue
                local = market_data.eth_price
                if local and price:
                    spread = abs(local - price) / min(local, price)
                    if spread > self.config.cross_chain['min_spread']:
                        profit = spread * self.config.cross_chain['amount'] * local
                        gas = gas_cost_usd(self.config.cross_chain['gas_units'], market_data.eth_price, market_data.gas_gwei)
                        if profit > gas:
                            executor_map = {
                                'hop': ExecutorType.HOP,
                                'synapse': ExecutorType.SYNAPSE,
                                'celer': ExecutorType.CELER,
                                'multichain': ExecutorType.MULTICHAIN,
                                'wormhole': ExecutorType.WORMHOLE,
                                'axelar': ExecutorType.AXELAR,
                                'layerzero': ExecutorType.LAYERZERO,
                                'across': ExecutorType.ACROSS,
                                'anyswap': ExecutorType.ANYSWAP,
                            }
                            opp = Opportunity(
                                category=StrategyCategory.CROSS_CHAIN,
                                name=f"{bridge_name.capitalize()} Arb",
                                profit=profit - gas,
                                action="bridge_arb",
                                params={'bridge': bridge_name, 'target_chain': target_chain, 'amount': self.config.cross_chain['amount']},
                                executor=executor_map.get(bridge_name, ExecutorType.UNIVERSAL),
                                chain=market_data.chain,
                                confidence=0.5,
                                gas_cost=gas,
                                gas_wei=self.config.cross_chain['gas_units']
                            )
                            await self._update_stats(True, 0.5)
                            return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class StakingAgent(BaseAgent):
    def __init__(self):
        super().__init__("staking", [StrategyCategory.STAKING])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        stakes = market_data.external.get('staking_opportunities', [])
        for stake in stakes:
            apr = stake.get('apr', 0)
            if apr > 10:
                profit = (apr / 100) * stake.get('min_amount', 100)
                gas = gas_cost_usd(250000, market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.STAKING,
                        name=f"Stake {stake.get('name', '')}",
                        profit=profit - gas,
                        action="stake",
                        params=stake,
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=0.7,
                        gas_cost=gas,
                        gas_wei=250000
                    )
                    await self._update_stats(True, 0.7)
                    return opp, 0.7, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class YieldAgent(BaseAgent):
    def __init__(self):
        super().__init__("yield", [StrategyCategory.YIELD])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        farms = market_data.external.get('yield_farms', [])
        for farm in farms:
            apy = farm.get('apy', 0)
            tvl = farm.get('tvl', 0)
            if apy > 20 and tvl > 100000:
                profit = (apy / 100) * 1000
                gas = gas_cost_usd(250000, market_data.eth_price, market_data.gas_gwei)
                if profit > gas:
                    opp = Opportunity(
                        category=StrategyCategory.YIELD,
                        name=f"Yield {farm.get('name', '')}",
                        profit=profit - gas,
                        action="farm",
                        params=farm,
                        executor=ExecutorType.UNIVERSAL,
                        chain=market_data.chain,
                        confidence=0.6,
                        gas_cost=gas,
                        gas_wei=250000
                    )
                    await self._update_stats(True, 0.6)
                    return opp, 0.6, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class GasAgent(BaseAgent):
    def __init__(self):
        super().__init__("gas", [StrategyCategory.GAS])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        if market_data.gas_gwei < 20:
            opp = Opportunity(
                category=StrategyCategory.GAS,
                name="Low Gas",
                profit=10.0,
                action="execute_queued",
                params={'gas_price': market_data.gas_gwei},
                executor=ExecutorType.UNIVERSAL,
                chain=market_data.chain,
                confidence=0.8,
                gas_cost=gas_cost_usd(50000, market_data.eth_price, market_data.gas_gwei),
                gas_wei=50000
            )
            await self._update_stats(True, 0.8)
            return opp, 0.8, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class AirdropAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("airdrop", [StrategyCategory.AIRDROP])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        airdrops = market_data.external.get('airdrop_opportunities', [])
        for airdrop in airdrops:
            value = airdrop.get('value', 0)
            deadline = airdrop.get('deadline', 0)
            if value >= self.config.min_profit and (deadline == 0 or deadline > time.time()):
                gas = gas_cost_usd(50000, market_data.eth_price, market_data.gas_gwei)
                if value > gas:
                    opp = Opportunity(
                        category=StrategyCategory.AIRDROP,
                        name=f"Airdrop {airdrop.get('name', '')}",
                        profit=value - gas,
                        action="claim",
                        params=airdrop,
                        executor=ExecutorType.AIRDROP,
                        chain=market_data.chain,
                        confidence=0.9,
                        gas_cost=gas,
                        gas_wei=50000,
                        deadline=deadline
                    )
                    await self._update_stats(True, 0.9)
                    return opp, 0.9, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class ReferralAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("referral", [StrategyCategory.REFERRAL])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        referrals = market_data.external.get('referral_programs', [])
        for ref in referrals:
            reward = ref.get('reward', 0)
            if reward >= self.config.referral['min_profit_usd']:
                gas = gas_cost_usd(self.config.referral['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if reward > gas:
                    opp = Opportunity(
                        category=StrategyCategory.REFERRAL,
                        name=f"Referral {ref.get('name', '')}",
                        profit=reward - gas,
                        action="referral",
                        params=ref,
                        executor=ExecutorType.REFERRAL,
                        chain=market_data.chain,
                        confidence=0.8,
                        gas_cost=gas,
                        gas_wei=self.config.referral['gas_units']
                    )
                    await self._update_stats(True, 0.8)
                    return opp, 0.8, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class SelfDestructAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("self_destruct", [StrategyCategory.SELF_DESTRUCT])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        contracts = market_data.external.get('vulnerable_contracts', [])
        for contract in contracts:
            value = contract.get('value', 0)
            if value >= self.config.self_destruct['min_value']:
                gas = gas_cost_usd(self.config.self_destruct['gas_units'], market_data.eth_price, market_data.gas_gwei)
                if value > gas:
                    opp = Opportunity(
                        category=StrategyCategory.SELF_DESTRUCT,
                        name=f"SelfDestruct {contract.get('address', '')[:8]}",
                        profit=value - gas,
                        action="selfdestruct",
                        params=contract,
                        executor=ExecutorType.SELF_DESTRUCT,
                        chain=market_data.chain,
                        confidence=0.5,
                        gas_cost=gas,
                        gas_wei=self.config.self_destruct['gas_units']
                    )
                    await self._update_stats(True, 0.5)
                    return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class GaslessAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("gasless", [StrategyCategory.GASLESS])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        gasless_list = market_data.external.get('gasless_opportunities', [])
        for item in gasless_list:
            profit = item.get('profit', 0)
            if profit >= self.config.gasless['min_profit']:
                opp = Opportunity(
                    category=StrategyCategory.GASLESS,
                    name=item.get('name', 'Gasless'),
                    profit=profit,
                    action="gasless",
                    params=item,
                    gas_type=GasType.ZERO.value,
                    executor=ExecutorType.COWSWAP,
                    chain=market_data.chain,
                    confidence=0.7,
                    gas_cost=0
                )
                await self._update_stats(True, 0.7)
                return opp, 0.7, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class KeeperAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("keeper", [StrategyCategory.KEEPER])
        self.config = config

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        gelato = market_data.external.get('gelato_tasks', [])
        for task in gelato:
            profit = task.get('profit', 0)
            if profit >= self.config.gasless['gelato_min_profit']:
                opp = Opportunity(
                    category=StrategyCategory.KEEPER,
                    name=task.get('name', 'Gelato'),
                    profit=profit,
                    action="keeper",
                    params=task,
                    executor=ExecutorType.GELATO,
                    chain=market_data.chain,
                    confidence=0.6,
                    gas_wei=self.config.gasless['gelato_gas_units']
                )
                await self._update_stats(True, 0.6)
                return opp, 0.6, {}
        chainlink = market_data.external.get('chainlink_jobs', [])
        for job in chainlink:
            profit = job.get('profit', 0)
            if profit >= self.config.gasless['chainlink_trade_amount']:
                opp = Opportunity(
                    category=StrategyCategory.KEEPER,
                    name=job.get('name', 'Chainlink'),
                    profit=profit,
                    action="keeper",
                    params=job,
                    executor=ExecutorType.CHAINLINK,
                    chain=market_data.chain,
                    confidence=0.7,
                    gas_wei=self.config.gasless['chainlink_gas_units']
                )
                await self._update_stats(True, 0.7)
                return opp, 0.7, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class HoneypotAgent(BaseAgent):
    def __init__(self, god_pulse: Optional[GodPulse]):
        super().__init__("honeypot", [StrategyCategory.HONEYPOT])
        self.detector = HoneypotDetector(god_pulse) if god_pulse else None

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        if not self.detector:
            return None, 0, {}
        addresses = market_data.external.get('addresses_to_check', [])
        for addr in addresses[:10]:
            result = await self.detector.check_honeypot(addr, "0x0000000000000000000000000000000000000000")
            if result.get('is_honeypot'):
                opp = Opportunity(
                    category=StrategyCategory.HONEYPOT,
                    name=f"Honeypot {addr[:8]}",
                    profit=0,
                    action="alert",
                    params={'address': addr, 'risk': result.get('risk')},
                    executor=ExecutorType.UNIVERSAL,
                    chain=market_data.chain,
                    confidence=0.9
                )
                await self._update_stats(True, 0.9)
                return opp, 0.9, result
        await self._update_stats(False, 0)
        return None, 0, {}

class ForgottenAgent(BaseAgent):
    def __init__(self):
        super().__init__("forgotten", [StrategyCategory.FORGOTTEN])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        forgotten = market_data.external.get('forgotten_contracts', [])
        for contract in forgotten:
            opp = Opportunity(
                category=StrategyCategory.FORGOTTEN,
                name=f"Forgotten {contract.get('address', '')[:8]}",
                profit=contract.get('value', 0),
                action="recover",
                params=contract,
                executor=ExecutorType.UNIVERSAL,
                chain=market_data.chain,
                confidence=0.3
            )
            await self._update_stats(True, 0.3)
            return opp, 0.3, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class PricePredictionAgent(BaseAgent):
    def __init__(self):
        super().__init__("price_prediction", [StrategyCategory.PRICE_PREDICTION])
        self.lstm_predictor = None
        self.arima_predictor = None
        if TORCH_AVAILABLE:
            self.lstm_predictor = LSTMPredictor(input_size=5, hidden_size=64)
        if ARIMA_AVAILABLE:
            self.arima_predictor = ARIMAPredictor(order=(1,1,1))

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        price_history = market_data.external.get('price_history', [market_data.eth_price] * 20)
        if self.arima_predictor:
            self.arima_predictor.train(price_history)
            predicted = self.arima_predictor.predict()
        elif self.lstm_predictor:
            features = np.array([price_history[-10:]])
            predicted = self.lstm_predictor.predict(features)
        else:
            predicted = market_data.eth_price * random.uniform(0.98, 1.02)

        opp = Opportunity(
            category=StrategyCategory.PRICE_PREDICTION,
            name="Price Prediction",
            profit=0,
            action="predict",
            params={'current': market_data.eth_price, 'predicted': predicted},
            executor=ExecutorType.UNIVERSAL,
            chain=market_data.chain,
            confidence=0.5
        )
        await self._update_stats(True, 0.5)
        return opp, 0.5, {}

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__("sentiment", [StrategyCategory.SENTIMENT])
        self.session = None

    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        await self._ensure_session()
        # ÇÓÊÏÚÇÁ API áãÔÇÚÑ ÇáÓæÞ (ãËÇá: https://api.lunarcrush.com/v2/data?key=...)
        # äÓÊÎÏã ÈíÇäÇÊ æåãíÉ ãÄÞÊÇð
        sentiment = random.choice(['positive', 'negative', 'neutral'])
        opp = Opportunity(
            category=StrategyCategory.SENTIMENT,
            name="Sentiment Analysis",
            profit=0,
            action="sentiment",
            params={'sentiment': sentiment},
            executor=ExecutorType.UNIVERSAL,
            chain=market_data.chain,
            confidence=0.6
        )
        await self._update_stats(True, 0.6)
        return opp, 0.6, {}

class TechnicalAgent(BaseAgent):
    def __init__(self):
        super().__init__("technical", [StrategyCategory.TECHNICAL])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        # ÍÓÇÈ RSI ãä ÈíÇäÇÊ ÊÇÑíÎíÉ
        price_history = market_data.external.get('price_history', [market_data.eth_price] * 20)
        if len(price_history) > 14:
            gains = []
            losses = []
            for i in range(1, len(price_history)):
                change = price_history[i] - price_history[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(-change)
            avg_gain = sum(gains[-14:]) / 14
            avg_loss = sum(losses[-14:]) / 14
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
        else:
            rsi = 50
        # MACD (ÊÈÓíØ)
        macd = random.choice(['bullish', 'bearish'])
        opp = Opportunity(
            category=StrategyCategory.TECHNICAL,
            name="Technical Analysis",
            profit=0,
            action="technical",
            params={'rsi': rsi, 'macd': macd},
            executor=ExecutorType.UNIVERSAL,
            chain=market_data.chain,
            confidence=0.6
        )
        await self._update_stats(True, 0.6)
        return opp, 0.6, {}

class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__("news", [StrategyCategory.NEWS])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        news_items = market_data.external.get('news', [])
        for news in news_items[:5]:
            opp = Opportunity(
                category=StrategyCategory.NEWS,
                name=news.get('title', 'News')[:30],
                profit=0,
                action="news",
                params=news,
                executor=ExecutorType.UNIVERSAL,
                chain=market_data.chain,
                confidence=0.5
            )
            await self._update_stats(True, 0.5)
            return opp, 0.5, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class ComposioAgent(BaseAgent):
    def __init__(self, config: Config):
        super().__init__("composio", [StrategyCategory.COMPOSIO])
        self.config = config
        self.composio_client = None
        if COMPOSIO_AVAILABLE and config.composio_api_key:
            self.composio_client = composio.Client(config.composio_api_key)

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        if self.composio_client:
            # íãßä ÇÓÊÏÚÇÁ ÃÏæÇÊ ãËá GitHub, Gmail, ÅáÎ
            opp = Opportunity(
                category=StrategyCategory.COMPOSIO,
                name="Composio Integration",
                profit=0,
                action="composio",
                params={'tools': ['github', 'gmail']},
                executor=ExecutorType.UNIVERSAL,
                chain=market_data.chain,
                confidence=0.8
            )
            await self._update_stats(True, 0.8)
            return opp, 0.8, {}
        await self._update_stats(False, 0)
        return None, 0, {}

class InjectiveAgent(BaseAgent):
    def __init__(self):
        super().__init__("injective", [StrategyCategory.INJECTIVE])

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        # ÇÓÊÎÏÇã Injective blockchain
        opp = Opportunity(
            category=StrategyCategory.INJECTIVE,
            name="Injective",
            profit=0,
            action="injective",
            params={'chain': 'injective'},
            executor=ExecutorType.UNIVERSAL,
            chain='injective',
            confidence=0.7
        )
        await self._update_stats(True, 0.7)
        return opp, 0.7, {}

class TriangularArbitrageAgent(BaseAgent):
    def __init__(self, config: Config, price_fetcher: PriceFetcher):
        super().__init__("triangular_arb", [StrategyCategory.TRIANGULAR_ARBITRAGE])
        self.config = config
        self.pf = price_fetcher
        self.popular_triangles = [
            ['WETH', 'USDC', 'DAI', 'WETH'],
            ['WETH', 'USDT', 'DAI', 'WETH'],
            ['USDC', 'DAI', 'USDT', 'USDC'],
        ]

    async def _get_pair_price(self, token_a: str, token_b: str, md: MarketData) -> Optional[float]:
        addr_a = get_address(md.chain, token_a)
        addr_b = get_address(md.chain, token_b)
        if not addr_a or not addr_b:
            return None
        # äÈÍË Ýí ÃÓÚÇÑ Uniswap (íãßä ÇáÊæÓÚ)
        price = md.uniswap_prices.get(addr_b)
        return price

    async def process(self, opportunity: Opportunity, market_data: MarketData) -> Tuple[Optional[Opportunity], float, Dict]:
        for triangle in self.popular_triangles:
            try:
                price1 = await self._get_pair_price(triangle[0], triangle[1], market_data)
                price2 = await self._get_pair_price(triangle[1], triangle[2], market_data)
                price3 = await self._get_pair_price(triangle[2], triangle[3], market_data)
                if not all([price1, price2, price3]):
                    continue
                profit_factor = price1 * price2 * price3 * (0.997 ** 3)
                if profit_factor > 1 + self.config.triangular['min_profit'] / 100:
                    profit = (profit_factor - 1) * self.config.triangular['amount']
                    gas = gas_cost_usd(self.config.triangular['gas_units'], market_data.eth_price, market_data.gas_gwei)
                    if profit > gas:
                        opp = Opportunity(
                            category=StrategyCategory.TRIANGULAR_ARBITRAGE,
                            name=f"Tri Arb {'-'.join(triangle)}",
                            profit=profit - gas,
                            action="triangular_arb",
                            params={'path': triangle, 'prices': [price1, price2, price3]},
                            executor=ExecutorType.UNIVERSAL,
                            chain=market_data.chain,
                            confidence=0.6,
                            gas_cost=gas,
                            gas_wei=self.config.triangular['gas_units']
                        )
                        await self._update_stats(True, 0.6)
                        return opp, 0.6, {}
            except Exception as e:
                logger.debug(f"Triangular arb error: {e}")
        await self._update_stats(False, 0)
        return None, 0, {}

class SandwichAttackAgent(BaseAgent):
    def __init__(self, config: Config, mempool: MempoolWatcher, simulator: PreflightSimulator):
        super().__init__("sandwich", [StrategyCategory.SANDWICH])
        self.config = config
        self.mempool = mempool
        self.simulator = simulator
        self.uniswap_v2_factory = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
        self.uniswap_v3_factory = "0x1F98431c8aD98523631ae4a59f267346ea31F984"
        self.quoter_v2 = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"

    async def _analyze_transaction(self, tx: Dict) -> Optional[Dict]:
        # ÊÍáíá ÇáãÚÇãáÉ áÊÍÏíÏ ÅÐÇ ßÇäÊ ÞÇÈáÉ ááÓÇäÏæíÊÔ
        try:
            data = tx.get('input', '0x')
            value = int(tx.get('value', 0))
            if data.startswith('0x7ff36ab5'):  # swapExactETHForTokens
                # ãÓÇÑ v2
                path = self._decode_uniswap_v2_path(data)
                amount_in = value
                return {
                    'type': 'v2',
                    'path': path,
                    'amount_in': amount_in,
                    'expected_out': await self._get_expected_out_v2(path, amount_in),
                    'victim': tx['from']
                }
            elif data.startswith('0x414bf389'):  # exactInputSingle (v3)
                params = self._decode_uniswap_v3_exact_input_single(data)
                return {
                    'type': 'v3',
                    'params': params,
                    'amount_in': params['amountIn'],
                    'expected_out': params['amountOutMinimum'],
                    'victim': tx['from']
                }
            elif data.startswith('0x5c11d795'):  # swapExactTokensForTokens (v2)
                path = self._decode_uniswap_v2_path(data)
                amount_in = self._decode_uint256(data, 4)
                return {
                    'type': 'v2',
                    'path': path,
              
