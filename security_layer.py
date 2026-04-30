# =============================================================================
# ÅÖÇÝÇÊ ãÊßÇãáÉ: ØÈÞÉ ÇáÃãÇä ÇáÞÕæì + æßíá ÇáÓÍÈ ÇáÊáÞÇÆí
# =============================================================================

import tempfile
import re
import subprocess
import time
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass

# -----------------------------------------------------------------------------
# 1. ÏæÇá ÅÖÇÝíÉ áÜ ExtendedGodPulse (Åä áã Êßä ãæÌæÏÉ)
# -----------------------------------------------------------------------------
if not hasattr(ExtendedGodPulse, 'get_balance'):
    async def get_balance(self, address: str, chain: str, token_address: Optional[str] = None) -> float:
        """ÇÓÊÑÏÇÏ ÑÕíÏ ETH Ãæ ERC20 áÚäæÇä ãÚíä."""
        if not WEB3_AVAILABLE:
            raise RuntimeError("web3.py not installed")
        rpc_url = os.environ.get(f"{chain.upper()}_RPC_URL")
        if not rpc_url:
            raise ConfigurationError(f"RPC URL for {chain} not set")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            raise ConnectionError(f"Cannot connect to {chain} RPC")
        try:
            if token_address:
                contract = w3.eth.contract(
                    address=Web3.to_checksum_address(token_address),
                    abi=[{
                        "constant": True,
                        "inputs": [{"name": "owner", "type": "address"}],
                        "name": "balanceOf",
                        "outputs": [{"name": "", "type": "uint256"}],
                        "type": "function"
                    }]
                )
                bal_raw = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
                try:
                    dec_contract = w3.eth.contract(
                        address=Web3.to_checksum_address(token_address),
                        abi=[{
                            "constant": True,
                            "inputs": [],
                            "name": "decimals",
                            "outputs": [{"name": "", "type": "uint8"}],
                            "type": "function"
                        }]
                    )
                    decimals = dec_contract.functions.decimals().call()
                except Exception:
                    decimals = 18
                return bal_raw / (10 ** decimals)
            else:
                bal_wei = w3.eth.get_balance(Web3.to_checksum_address(address))
                return bal_wei / 1e18
        except Exception as e:
            logger.warning(f"Failed to get balance for {address} on {chain}: {e}")
            return 0.0
    ExtendedGodPulse.get_balance = get_balance
    logger.info("ExtendedGodPulse.get_balance added")

if not hasattr(ExtendedGodPulse, 'send_transaction'):
    async def send_transaction(
        self,
        to: str,
        value: int = 0,
        data: bytes = b'',
        token_address: Optional[str] = None,
        private_key: Optional[str] = None,
        chain: str = 'ethereum',
        gas_limit: int = 150000,
        gas_price_multiplier: float = 1.2
    ) -> str:
        """ÅÑÓÇá ãÚÇãáÉ (ETH Ãæ ERC20) ÈÇÓÊÎÏÇã ÇáãÝÊÇÍ ÇáÎÇÕ."""
        if not WEB3_AVAILABLE:
            raise RuntimeError("web3.py not installed")
        pk = private_key or os.environ.get('DEPLOYER_PRIVATE_KEY')
        if not pk:
            raise ConfigurationError("No private key provided")
        rpc_url = os.environ.get(f"{chain.upper()}_RPC_URL")
        if not rpc_url:
            raise ConfigurationError(f"RPC URL for {chain} not set")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            raise ConnectionError(f"Cannot connect to {chain} RPC")
        account = Account.from_key(pk)
        nonce = w3.eth.get_transaction_count(account.address)
        if token_address:
            token_contract = w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=[{
                    "constant": False,
                    "inputs": [{"name": "to", "type": "address"}, {"name": "value", "type": "uint256"}],
                    "name": "transfer",
                    "outputs": [{"name": "", "type": "bool"}],
                    "type": "function"
                }]
            )
            try:
                estimated = token_contract.functions.transfer(
                    Web3.to_checksum_address(to), value
                ).estimate_gas({'from': account.address})
                gas_limit = max(gas_limit, int(estimated * 1.2))
            except Exception:
                pass
        try:
            base_fee = w3.eth.get_block('latest')['baseFeePerGas']
            max_priority = w3.eth.max_priority_fee
            max_fee = int((base_fee + max_priority) * gas_price_multiplier)
            tx_params = {
                'from': account.address,
                'nonce': nonce,
                'gas': gas_limit,
                'maxFeePerGas': max_fee,
                'maxPriorityFeePerGas': max_priority
            }
        except Exception:
            gas_price = w3.eth.gas_price
            if gas_price == 0:
                gas_price = 100 * 10**9
            gas_price = int(gas_price * gas_price_multiplier)
            tx_params = {
                'from': account.address,
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price
            }
        if token_address:
            tx = token_contract.functions.transfer(
                Web3.to_checksum_address(to), value
            ).build_transaction(tx_params)
        else:
            tx = {
                **tx_params,
                'to': Web3.to_checksum_address(to),
                'value': value,
                'data': data
            }
        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status != 1:
            raise RuntimeError(f"Transaction failed: {tx_hash.hex()}")
        return tx_hash.hex()
    ExtendedGodPulse.send_transaction = send_transaction
    logger.info("ExtendedGodPulse.send_transaction added")

# -----------------------------------------------------------------------------
# 2. ØÈÞÉ ÇáÃãÇä ÇáÞÕæì (ÌãíÚ ÇáãíÒÇÊ ÇáÊí ÃÑÓáÊåÇ)
# -----------------------------------------------------------------------------
class OpenZeppelinContractGenerator:
    @staticmethod
    def _sanitize(s: str) -> str:
        s = re.sub(r'[^a-zA-Z0-9_]', '', s)
        return s[:64] if s else "Token"

    @staticmethod
    def generate_erc20(name: str, symbol: str, decimals: int = 18, initial_supply: int = 0) -> str:
        name_safe = OpenZeppelinContractGenerator._sanitize(name)
        symbol_safe = OpenZeppelinContractGenerator._sanitize(symbol)
        return f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract {name_safe} is ERC20, Ownable, Pausable, ReentrancyGuard {{
    uint8 private _decimals;
    
    constructor() ERC20("{name_safe}", "{symbol_safe}") Ownable(msg.sender) {{
        _decimals = {decimals};
        if ({initial_supply} > 0) {{
            _mint(msg.sender, {initial_supply} * 10 ** _decimals);
        }}
    }}
    
    function decimals() public view override returns (uint8) {{
        return _decimals;
    }}
    
    function pause() external onlyOwner {{
        _pause();
    }}
    
    function unpause() external onlyOwner {{
        _unpause();
    }}
    
    function mint(address to, uint256 amount) external onlyOwner {{
        _mint(to, amount);
    }}
    
    function burn(uint256 amount) external {{
        _burn(msg.sender, amount);
    }}
    
    function transfer(address to, uint256 amount) public override whenNotPaused nonReentrant returns (bool) {{
        return super.transfer(to, amount);
    }}
    
    function transferFrom(address from, address to, uint256 amount) public override whenNotPaused nonReentrant returns (bool) {{
        return super.transferFrom(from, to, amount);
    }}
}}"""

    @staticmethod
    def generate_defi_pool(token_address: str) -> str:
        return f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract DeFiPool is Ownable, ReentrancyGuard, Pausable {{
    using SafeERC20 for IERC20;
    
    IERC20 public token;
    uint256 public totalDeposits;
    mapping(address => uint256) public deposits;
    mapping(address => uint256) public depositTimestamps;
    
    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event EmergencyWithdrawn(address indexed to, uint256 amount);
    
    constructor(address _token) Ownable(msg.sender) {{
        require(_token != address(0), "Invalid token");
        token = IERC20(_token);
    }}
    
    function deposit(uint256 amount) external nonReentrant whenNotPaused {{
        require(amount > 0, "Amount must be > 0");
        token.safeTransferFrom(msg.sender, address(this), amount);
        deposits[msg.sender] += amount;
        depositTimestamps[msg.sender] = block.timestamp;
        totalDeposits += amount;
        emit Deposited(msg.sender, amount);
    }}
    
    function withdraw(uint256 amount) external nonReentrant {{
        require(amount > 0, "Amount must be > 0");
        require(deposits[msg.sender] >= amount, "Insufficient balance");
        deposits[msg.sender] -= amount;
        totalDeposits -= amount;
        token.safeTransfer(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }}
    
    function emergencyWithdraw(address to) external onlyOwner {{
        uint256 balance = token.balanceOf(address(this));
        require(balance > 0, "No balance");
        token.safeTransfer(to, balance);
        emit EmergencyWithdrawn(to, balance);
    }}
    
    receive() external payable {{
        revert("Cannot receive ETH");
    }}
}}"""

class FormalVerificationEngineAdvanced:
    def __init__(self):
        self._slither_available = None
        self._mythril_available = None
        self._initialized = False

    async def _check_tool(self, tool: str) -> bool:
        try:
            proc = await asyncio.create_subprocess_exec(
                tool, '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            return proc.returncode == 0
        except:
            return False

    async def initialize(self):
        self._slither_available = await self._check_tool('slither')
        self._mythril_available = await self._check_tool('myth')
        self._initialized = True
        if not self._slither_available and not self._mythril_available:
            logger.warning("No formal verification tools found (slither/mythril). Install for enhanced security.")

    async def verify_contract(self, contract_path: str) -> Dict:
        if not self._initialized:
            await self.initialize()
        results = {'slither': None, 'mythril': None, 'overall_score': 0.0, 'is_verified': False}
        total_score = 0.0
        tools_found = 0

        if self._slither_available:
            try:
                proc = await asyncio.create_subprocess_exec(
                    'slither', contract_path, '--json', '-',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
                if proc.returncode == 0:
                    data = json.loads(stdout.decode())
                    detectors = data.get('results', {}).get('detectors', [])
                    score = max(0.0, 100.0 - len(detectors) * 5.0)
                    results['slither'] = {'vulnerabilities': len(detectors), 'detectors': detectors, 'score': score}
                    total_score += score
                    tools_found += 1
                else:
                    results['slither'] = {'error': stderr.decode()}
            except Exception as e:
                results['slither'] = {'error': str(e)}

        if self._mythril_available:
            try:
                proc = await asyncio.create_subprocess_exec(
                    'myth', 'analyze', contract_path, '--json',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=180)
                if proc.returncode == 0:
                    data = json.loads(stdout.decode())
                    issues = data.get('issues', [])
                    score = max(0.0, 100.0 - len(issues) * 10.0)
                    results['mythril'] = {'issues': len(issues), 'details': issues, 'score': score}
                    total_score += score
                    tools_found += 1
                else:
                    results['mythril'] = {'error': stderr.decode()}
            except Exception as e:
                results['mythril'] = {'error': str(e)}

        if tools_found > 0:
            results['overall_score'] = total_score / tools_found
            results['is_verified'] = results['overall_score'] >= 90.0
        return results

class TimelockController:
    @staticmethod
    def generate_timelock_controller(min_delay: int = 86400, proposers: Optional[List[str]] = None, executors: Optional[List[str]] = None) -> str:
        proposers = proposers or ['0x0000000000000000000000000000000000000000']
        executors = executors or ['0x0000000000000000000000000000000000000000']
        proposers_str = ', '.join([f'"{p}"' for p in proposers])
        executors_str = ', '.join([f'"{e}"' for e in executors])
        return f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/governance/TimelockController.sol";

contract AlKhaledTimelock is TimelockController {{
    constructor() TimelockController({min_delay}, [{proposers_str}], [{executors_str}], msg.sender) {{}}
}}"""

class HardwareSecurityModule:
    def __init__(self):
        self._master_key = None
        self._initialized = False
    async def initialize(self, master_key_hex: str):
        self._master_key = bytes.fromhex(master_key_hex)
        self._initialized = True
    async def sign_transaction(self, tx_hash: bytes) -> bytes:
        if not self._initialized:
            raise RuntimeError("HSM not initialized")
        return secrets.token_bytes(64)  # ãÍÇßÇÉ
    async def get_public_key(self) -> str:
        return "0x" + secrets.token_hex(64)

class UltraSecureDeployer:
    def __init__(self, god_pulse: ExtendedGodPulse, hsm: Optional[HardwareSecurityModule] = None):
        self.god_pulse = god_pulse
        self.hsm = hsm or HardwareSecurityModule()
        self.formal_verifier = FormalVerificationEngineAdvanced()
        self.deployment_history = {}

    async def _transfer_ownership(self, contract_address: str, new_owner: str, chain: str, private_key: str) -> bool:
        try:
            from web3 import Web3
            from eth_account import Account
        except ImportError:
            logger.error("web3.py not installed")
            return False
        rpc_url = os.environ.get(f"{chain.upper()}_RPC_URL")
        if not rpc_url:
            return False
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            return False
        account = Account.from_key(private_key)
        abi = [{
            "constant": False,
            "inputs": [{"name": "newOwner", "type": "address"}],
            "name": "transferOwnership",
            "outputs": [],
            "type": "function"
        }]
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
        try:
            nonce = w3.eth.get_transaction_count(account.address)
            tx = contract.functions.transferOwnership(new_owner).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 100000,
                'gasPrice': w3.eth.gas_price
            })
            signed = account.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            return receipt.status == 1
        except Exception as e:
            logger.error(f"Ownership transfer failed: {e}")
            return False

    async def deploy_contract(
        self,
        contract_type: str,
        params: Dict[str, Any],
        chain: str,
        use_timelock: bool = True,
        timelock_delay: int = 86400,
        simulate_only: bool = False,
        require_formal_verification: bool = True,
        require_slither_score: float = 90.0
    ) -> Dict[str, Any]:
        result = {'success': False, 'steps': {}, 'error': None, 'contract_address': None, 'timelock_address': None}
        # 1. ÊæáíÏ ÇáÚÞÏ
        logger.info("Step 1: Generating contract using OpenZeppelin templates")
        if contract_type == 'erc20':
            source = OpenZeppelinContractGenerator.generate_erc20(
                params.get('name', 'Token'),
                params.get('symbol', 'TKN'),
                params.get('decimals', 18),
                params.get('initial_supply', 0)
            )
        elif contract_type == 'defi_pool':
            source = OpenZeppelinContractGenerator.generate_defi_pool(params.get('token_address', '0x0000000000000000000000000000000000000000'))
        else:
            result['error'] = f"Unsupported contract type: {contract_type}"
            return result
        result['steps']['generated'] = {'source_hash': hashlib.sha256(source.encode()).hexdigest()}

        # 2. ÇáÊÍÞÞ ÇáÑÓãí
        verification = {'overall_score': 0, 'is_verified': False}
        if require_formal_verification:
            logger.info("Step 2: Running formal verification (Slither, Mythril)")
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sol', delete=False) as f:
                f.write(source)
                temp_path = f.name
            try:
                await self.formal_verifier.initialize()
                verification = await self.formal_verifier.verify_contract(temp_path)
                result['steps']['formal_verification'] = verification
                if verification.get('overall_score', 0) < require_slither_score:
                    result['error'] = f"Formal verification failed: score {verification.get('overall_score', 0)} < {require_slither_score}"
                    return result
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        else:
            result['steps']['formal_verification'] = {'skipped': True}

        # 3. ãÍÇßÇÉ (äãæÐÌíÉ)
        logger.info("Step 3: Simulation (basic checks)")
        result['steps']['simulation'] = {'status': 'skipped', 'message': 'Full simulation requires ganache-cli'}

        # 4. äÔÑ Timelock
        timelock_address = None
        if use_timelock:
            logger.info(f"Step 4: Deploying TimelockController with {timelock_delay}s delay")
            timelock_source = TimelockController.generate_timelock_controller(timelock_delay)
            if simulate_only:
                timelock_address = f"SIMULATED_TIMELOCK_{secrets.token_hex(8)}"
            else:
                private_key = os.environ.get('DEPLOYER_PRIVATE_KEY')
                if not private_key:
                    result['error'] = "DEPLOYER_PRIVATE_KEY not set for Timelock deployment"
                    return result
                try:
                    timelock_address = await self.god_pulse.deploy_contract(timelock_source, chain, private_key, simulate=False)
                except Exception as e:
                    result['error'] = f"Timelock deployment failed: {e}"
                    return result
            result['steps']['timelock'] = {'address': timelock_address, 'delay': timelock_delay}

        # 5. äÔÑ ÇáÚÞÏ ÇáÑÆíÓí
        if not simulate_only:
            logger.info("Step 5: Deploying main contract")
            private_key = os.environ.get('DEPLOYER_PRIVATE_KEY')
            if not private_key:
                result['error'] = "DEPLOYER_PRIVATE_KEY not set"
                return result
            try:
                contract_address = await self.god_pulse.deploy_contract(source, chain, private_key, simulate=False)
                result['contract_address'] = contract_address
                result['success'] = True
                self.deployment_history[contract_address] = {
                    'deployed_at': time.time(),
                    'chain': chain,
                    'type': contract_type,
                    'verification_score': verification.get('overall_score', 0),
                    'timelock': timelock_address
                }
                if timelock_address and not timelock_address.startswith("SIMULATED"):
                    transferred = await self._transfer_ownership(contract_address, timelock_address, chain, private_key)
                    result['steps']['ownership_transfer'] = {'status': 'success' if transferred else 'failed'}
                else:
                    result['steps']['ownership_transfer'] = {'status': 'not_needed'}
            except Exception as e:
                result['error'] = f"Deployment failed: {e}"
                return result
        else:
            result['success'] = True
            result['contract_address'] = f"SIMULATED_{secrets.token_hex(16)}"

        logger.info(f"Deployment completed with security score {verification.get('overall_score', 0)}")
        return result

# -----------------------------------------------------------------------------
# 3. æßíá ÊÍæíá ÇáÃãæÇá (FundSweeperAgent)
# -----------------------------------------------------------------------------
class FundSweeperAgent(BaseAgent if AGENTS_AVAILABLE else object):
    def __init__(
        self,
        god_pulse: ExtendedGodPulse,
        experience_db: Optional[ExperienceDB],
        execution_engine: Optional[ExecutionEngine],
        orchestrator: Optional[AgentOrchestrator],
        secondary_wallet: str,
        token_whitelist: Optional[List[str]] = None,
        check_interval: int = 60,
        min_balance_threshold_eth: float = 0.01,
        min_balance_threshold_tokens: Optional[Dict[str, float]] = None,
        gas_limit: int = 200000,
        gas_price_multiplier: float = 1.2
    ):
        self.god_pulse = god_pulse
        self.experience_db = experience_db
        self.execution_engine = execution_engine
        self.orchestrator = orchestrator
        if not WEB3_AVAILABLE:
            raise RuntimeError("web3.py required")
        self.secondary_wallet = Web3.to_checksum_address(secondary_wallet)
        self.token_whitelist = token_whitelist or []
        self.check_interval = check_interval
        self.min_balance_threshold_eth = min_balance_threshold_eth
        self.min_balance_threshold_tokens = min_balance_threshold_tokens or {}
        self.gas_limit = gas_limit
        self.gas_price_multiplier = gas_price_multiplier

        self.contracts_to_monitor: Dict[str, Dict] = {}
        self.running = False
        self._task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self._decimals_cache: Dict[Tuple[str, str], int] = {}

    async def _get_token_decimals(self, token: str, chain: str) -> int:
        key = (token, chain)
        if key in self._decimals_cache:
            return self._decimals_cache[key]
        try:
            rpc_url = os.environ.get(f"{chain.upper()}_RPC_URL")
            if rpc_url and WEB3_AVAILABLE:
                w3 = Web3(Web3.HTTPProvider(rpc_url))
                if w3.is_connected():
                    contract = w3.eth.contract(
                        address=Web3.to_checksum_address(token),
                        abi=[{
                            "constant": True,
                            "inputs": [],
                            "name": "decimals",
                            "outputs": [{"name": "", "type": "uint8"}],
                            "type": "function"
                        }]
                    )
                    decimals = contract.functions.decimals().call()
                    self._decimals_cache[key] = decimals
                    return decimals
        except Exception:
            pass
        return 18

    async def _sweep_contract(self, contract_address: str, chain: str, tokens: set):
        # ETH
        eth_bal = await self.god_pulse.get_balance(contract_address, chain)
        if eth_bal > self.min_balance_threshold_eth:
            amount_raw = int(eth_bal * 1e18)
            if amount_raw > 0:
                logger.info(f"Sweeping {eth_bal:.6f} ETH from {contract_address}")
                try:
                    tx_hash = await self.god_pulse.send_transaction(
                        to=self.secondary_wallet,
                        value=amount_raw,
                        chain=chain,
                        gas_limit=self.gas_limit,
                        gas_price_multiplier=self.gas_price_multiplier
                    )
                    if self.experience_db:
                        trade = TradeRecord(
                            opportunity_id=f"sweep_eth_{contract_address}_{int(time.time())}",
                            profit_usd=0, gas_cost_usd=0, tx_hash=tx_hash,
                            chain=chain, executor="fund_sweeper",
                            metadata={"type": "eth", "amount": eth_bal}
                        )
                        await self.experience_db.record_trade(trade)
                except Exception as e:
                    logger.error(f"ETH sweep failed for {contract_address}: {e}")

        # ÇáÑãæÒ
        to_check = tokens if tokens else set(self.token_whitelist)
        for token in to_check:
            bal = await self.god_pulse.get_balance(contract_address, chain, token)
            threshold = self.min_balance_threshold_tokens.get(token, self.min_balance_threshold_eth)
            if bal > threshold:
                decimals = await self._get_token_decimals(token, chain)
                amount_raw = int(bal * (10 ** decimals))
                if amount_raw > 0:
                    logger.info(f"Sweeping {bal:.6f} of {token} from {contract_address}")
                    try:
                        tx_hash = await self.god_pulse.send_transaction(
                            to=self.secondary_wallet,
                            value=amount_raw,
                            token_address=token,
                            chain=chain,
                            gas_limit=self.gas_limit,
                            gas_price_multiplier=self.gas_price_multiplier
                        )
                        if self.experience_db:
                            trade = TradeRecord(
                                opportunity_id=f"sweep_token_{token}_{contract_address}_{int(time.time())}",
                                profit_usd=0, gas_cost_usd=0, tx_hash=tx_hash,
                                chain=chain, executor="fund_sweeper",
                                metadata={"type": "erc20", "token": token, "amount": bal}
                            )
                            await self.experience_db.record_trade(trade)
                    except Exception as e:
                        logger.error(f"Token sweep failed for {token} on {contract_address}: {e}")

    async def add_contract(self, address: str, chain: str, tokens: Optional[List[str]] = None):
        async with self._lock:
            if address not in self.contracts_to_monitor:
                self.contracts_to_monitor[address] = {'chain': chain, 'tokens': set(tokens or [])}
                logger.info(f"Added contract {address} on {chain} to sweep monitor")
            elif tokens:
                self.contracts_to_monitor[address]['tokens'].update(tokens)

    async def remove_contract(self, address: str):
        async with self._lock:
            self.contracts_to_monitor.pop(address, None)

    async def sweep_now(self, address: str, chain: str, tokens: Optional[List[str]] = None):
        async with self._lock:
            await self._sweep_contract(address, chain, set(tokens or []))

    async def _monitor_loop(self):
        while self.running:
            try:
                async with self._lock:
                    contracts = list(self.contracts_to_monitor.items())
                for addr, data in contracts:
                    await self._sweep_contract(addr, data['chain'], data['tokens'])
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception(f"Monitor loop error: {e}")
            await asyncio.sleep(self.check_interval)

    async def start(self):
        if self.running:
            return
        self.running = True
        self._task = asyncio.create_task(self._monitor_loop())
        logger.info("FundSweeperAgent started")

    async def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await asyncio.wait_for(self._task, timeout=5)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
        logger.info("FundSweeperAgent stopped")

# -----------------------------------------------------------------------------
# 4. ÑÈØ ÊáÞÇÆí ÈÜ UltimateOrchestrator (ÊÚÏíá ØÝíÝ ÝÞØ áÅÖÇÝÉ ÇáãÊÛíÑÇÊ)
# -----------------------------------------------------------------------------
# äÖíÝ ÇáÎÇÕíÊíä Åáì UltimateOrchestrator ÅÐÇ áã ÊßæäÇ ãæÌæÏÊíä
if not hasattr(UltimateOrchestrator, 'ultra_secure_deployer'):
    # äÎÒä ÇáãÑÌÚ ÇáÃÕáí áÜ __init__ æ initialize æ stop
    _orig_init = UltimateOrchestrator.__init__
    _orig_initialize = UltimateOrchestrator.initialize
    _orig_stop = UltimateOrchestrator.stop

    def _new_init(self, *args, **kwargs):
        _orig_init(self, *args, **kwargs)
        self.ultra_secure_deployer = UltraSecureDeployer(self.god_pulse)
        secondary_wallet = os.environ.get('SECONDARY_WALLET')
        if secondary_wallet:
            self.fund_sweeper = FundSweeperAgent(
                god_pulse=self.god_pulse,
                experience_db=self.experience_db,
                execution_engine=self.execution_engine,
                orchestrator=self.orchestrator,
                secondary_wallet=secondary_wallet,
                check_interval=60,
                min_balance_threshold_eth=0.01
            )
            self._sweeper_started = False
        else:
            self.fund_sweeper = None
            self._sweeper_started = True

    async def _new_initialize(self):
        result = await _orig_initialize(self)
        if hasattr(self, 'fund_sweeper') and self.fund_sweeper and not getattr(self, '_sweeper_started', False):
            await self.fund_sweeper.start()
            self._sweeper_started = True
        return result

    async def _new_stop(self, timeout=10):
        if hasattr(self, 'fund_sweeper') and self.fund_sweeper:
            await self.fund_sweeper.stop()
        return await _orig_stop(self, timeout)

    UltimateOrchestrator.__init__ = _new_init
    UltimateOrchestrator.initialize = _new_initialize
    UltimateOrchestrator.stop = _new_stop
    logger.info("Military?grade security and FundSweeperAgent integrated into UltimateOrchestrator")
