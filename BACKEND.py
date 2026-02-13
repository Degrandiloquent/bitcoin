import requests
import json

def rpc(method, params=None, wallet=None):
    """Connect to Bitcoin Core RPC"""
    
    # Base URL for Bitcoin Core
    if wallet:
        # For wallet-specific commands
        url = f"http://127.0.0.1:18443/wallet/{wallet}"
    else:
        # For general commands
        url = "http://127.0.0.1:18443/"
    
    # RPC authentication - Polar default
    auth = ("polaruser", "polarpass")
    
    # Prepare the JSON-RPC request
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "1.0",
        "id": "explorer",
        "method": method,
        "params": params or []
    }
    
    try:
        # Send the request
        response = requests.post(url, 
                               json=payload, 
                               headers=headers, 
                               auth=auth)
        
        # Check for errors
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            return None
            
        # Parse JSON response
        result = response.json()
        
        # Check for RPC error
        if result.get("error"):
            print(f"RPC Error: {result['error']}")
            return None
            
        # Return the result
        return result["result"]
        
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

# Test the connection
if __name__ == "__main__":
    print("Testing Bitcoin Core connection...")
    info = rpc("getblockchaininfo")
    if info:
        print("✅ Connected to Bitcoin Core!")
        print(f"Chain: {info['chain']}")
        print(f"Blocks: {info['blocks']}")
    else:
        print("❌ Could not connect to Bitcoin Core")

from rpc_helper import rpc

#Business info
BUSINESS_NAME = "bytecode" 

print("="*50)
print("BUSINESS WALLET SETUP")
print("="*50)

# Step 1: Check if wallet exists and load it
print(f"\n1. Setting up wallet: {BUSINESS_NAME}")

try:
    rpc("loadwallet", [BUSINESS_NAME])
    print(f"✅ Loaded existing wallet: {BUSINESS_NAME}")
except:
    try:
        rpc("createwallet", [BUSINESS_NAME])
        print(f"✅ Created new wallet: {BUSINESS_NAME}")
    except Exception as e:
        print(f"ℹ️ Wallet status: {e}")

# Step 2: Generate a receiving address
print(f"\n2. Generating receiving address...")
try:
    address = rpc("getnewaddress", [], wallet=BUSINESS_NAME)
    print(f"✅ Business Bitcoin Address: {address}")
    
    # Save address to file
    with open(f"{BUSINESS_NAME}_address.txt", "w") as f:
        f.write(address)
    print(f"✅ Address saved to {BUSINESS_NAME}_address.txt")
except Exception as e:
    print(f"❌ Error getting address: {e}")
    address = None

# Step 3: Check current balance
print(f"\n3. Checking balance...")
try:
    balance = rpc("getbalance", [], wallet=BUSINESS_NAME)
    print(f"💰 Current Balance: {balance} BTC")
except Exception as e:
    print(f"❌ Error getting balance: {e}")

# Step 4: Mine initial blocks if balance is zero
if address and balance == 0:
    print(f"\n4. Mining initial blocks to fund business...")
    try:
        result = rpc("generatetoaddress", [101, address])
        print(f"✅ Mined {len(result)} blocks")
        
        # Check new balance
        balance = rpc("getbalance", [], wallet=BUSINESS_NAME)
        print(f"💰 New Balance: {balance} BTC")
    except Exception as e:
        print(f"❌ Error mining blocks: {e}")

print("\n" + "="*50)
print("SETUP COMPLETE")
print("="*50)
print(f"\nBusiness Name: {BUSINESS_NAME}")
if address:
    print(f"Receive Address: {address}")
if balance:
    print(f"Balance: {balance} BTC")
        
from rpc_helper import rpc

print("="*50)
print("CREATE/VERIFY WALLETS")
print("="*50)

# Business wallet - THIS IS THE ONLY ONE YOU NEED
BUSINESS_NAME = "bytecode"

print(f"\n=== SETTING UP BUSINESS WALLET: {BUSINESS_NAME} ===")
 
try:
      result = rpc("loadwallet", [BUSINESS_NAME])
      print(f"✅ Loaded existing wallet: {BUSINESS_NAME}")
except:
      # If load fails, create new wallet
      try:
          result = rpc("createwallet", [BUSINESS_NAME])
          print(f"✅ Created new wallet: {BUSINESS_NAME}")
      except Exception as e:
          print(f"ℹ️ Wallet status: {e}")

  # Get address
try:
      address = rpc("getnewaddress", [], wallet=BUSINESS_NAME)
      print(f"📍 Business address: {address}")
      
      # Save to file
      with open(f"{BUSINESS_NAME}_address.txt", "w") as f:
          f.write(address)
      print(f"✅ Address saved to {BUSINESS_NAME}_address.txt")
except Exception as e:
      print(f"❌ Error: {e}")

  # Get balance
try:
      balance = rpc("getbalance", [], wallet=BUSINESS_NAME)
      print(f"💰 Balance: {balance} BTC")
except Exception as e:
      print(f"❌ Error: {e}")

from rpc_helper import rpc

print("="*50)
print("WALLET FUNCTIONALITY TEST")
print("="*50)

BUSINESS_NAME = "bytecode"

  # Test 1: Get wallet info
print("\n1. TEST: Get wallet info")

try:
      info = rpc("getwalletinfo", [], wallet=BUSINESS_NAME)
      print(f"✅ Wallet name: {info.get('walletname', 'N/A')}")
      print(f"✅ Transaction count: {info.get('txcount', 0)}")
except Exception as e:
      print(f"❌ Error: {e}")

  # Test 2: Generate new address
print("\n2. TEST: Generate new address")

try:
      addr1 = rpc("getnewaddress", [], wallet=BUSINESS_NAME)
      addr2 = rpc("getnewaddress", ["", "bech32"], wallet=BUSINESS_NAME)
      print(f"✅ Default address: {addr1}")
      print(f"✅ SegWit address: {addr2}")
except Exception as e:
      print(f"❌ Error: {e}")

  # Test 3: Check balance
print("\n3. TEST: Check balance")

try:
      balance = rpc("getbalance", [], wallet=BUSINESS_NAME)
      print(f"✅ Balance: {balance} BTC")
except Exception as e:
      print(f"❌ Error: {e}")

  # Test 4: List transactions
print("\n4. TEST: List recent transactions")
  
try:
      txs = rpc("listtransactions", ["*", 10], wallet=BUSINESS_NAME)
      print(f"✅ Found {len(txs)} transactions")
      for tx in txs[:3]:  # Show first 3
          print(f"   {tx['category']}: {tx['amount']} BTC - {tx.get('txid', '')[:10]}...")
except Exception as e:
      print(f"❌ Error: {e}")

print("\n" + "="*50)
print("TESTS COMPLETE")
print("="*50)    

from rpc_helper import rpc

print("="*50)
print("WALLET CHECK")
print("="*50)

#Business wallet
BUSINESS_NAME = "bytecode"

# 1. List all wallets on the node
print("\n1. ALL WALLETS ON NODE:")
try:
    wallets = rpc("listwalletdir")
    print(wallets)
except Exception as e:
    print(f"Error: {e}")

# 2. List currently loaded wallets
print("\n2. CURRENTLY LOADED WALLETS:")
try:
    loaded = rpc("listwallets")
    print(loaded)
except Exception as e:
    print(f"Error: {e}")

# 3. Check if business wallet is loaded
print(f"\n3. CHECKING BUSINESS WALLET: {BUSINESS_NAME}")
if BUSINESS_NAME in loaded:
    print(f"✅ {BUSINESS_NAME} is loaded")
else:
    print(f"❌ {BUSINESS_NAME} is NOT loaded")
    # Try to load it
    try:
        rpc("loadwallet", [BUSINESS_NAME])
        print(f"✅ Loaded {BUSINESS_NAME}")
    except Exception as e:
        print(f"❌ Could not load: {e}")

# 4. Get business wallet info
print(f"\n4. BUSINESS WALLET INFO:")
try:
    balance = rpc("getbalance", [], wallet=BUSINESS_NAME)
    print(f"💰 Balance: {balance} BTC")
    
    address = rpc("getnewaddress", [], wallet=BUSINESS_NAME)
    print(f"📍 Address: {address}")
except Exception as e:
    print(f"Error: {e}")
    
from rpc_helper import rpc
import json
import time
from datetime import datetime

BUSINESS_NAME = "bytecode"
BUSINESS_ADDRESS = "bcrt1qx4z6zgqnkcealmny9cfyj0qnqr79ysz6e0ugg"

 # File to store payment history
HISTORY_FILE = "payment_history.json"

def load_payment_history():
     """Load existing payment history"""
     try:
         with open(HISTORY_FILE, "r") as f:
             return json.load(f)
     except:
         return {"payments": [], "total_received": 0}

def save_payment_history(history):
     """Save payment history"""
     with open(HISTORY_FILE, "w") as f:
         json.dump(history, f, indent=2)

def check_new_payments():
     """Check for new payments to your business address"""
     print("\n=== CHECKING FOR NEW PAYMENTS ===")
     
     # Get all transactions for wallet
     try:
         txs = rpc("listtransactions", ["*", 100], wallet=BUSINESS_NAME)
         
         history = load_payment_history()
         existing_txids = [p["txid"] for p in history["payments"]]
         
         new_payments = []
         
         for tx in txs:
             # Check if it's a payment to business
             if tx.get("category") in ["receive", "generate", "immature", "mine"]:
                 # Skip immature coins (not spendable yet)
                 if tx.get("category") == "immature" and tx.get("confirmations", 0) < 100:
                     continue
                     
                 # Check if we haven't recorded this transaction yet
                 if tx["txid"] not in existing_txids:
                     payment = {
                         "txid": tx["txid"],
                         "amount": tx["amount"],
                         "time": datetime.fromtimestamp(tx["time"]).strftime("%Y-%m-%d %H:%M:%S"),
                         "address": tx.get("address", "coinbase"),
                         "confirmations": tx["confirmations"]
                     }
                     new_payments.append(payment)
                     history["payments"].append(payment)
                     history["total_received"] += tx["amount"]
         
         if new_payments:
             save_payment_history(history)
             print(f"✅ Found {len(new_payments)} new payment(s)!")
             for p in new_payments:
                 print(f"   +{p['amount']} BTC - {p['time']} - {p['txid'][:10]}...")
         else:
             print("ℹ️ No new payments found")
             
         print(f"\n💰 Total Received All Time: {history['total_received']} BTC")
         print(f"📊 Total Transactions: {len(history['payments'])}")
         
     except Exception as e:
         print(f"❌ Error checking payments: {e}")

def show_business_summary():
     """Show current business status"""
     print("\n=== BUSINESS SUMMARY ===")
     print(f"🏢 Business: {BUSINESS_NAME}")
     print(f"📍 Address: {BUSINESS_ADDRESS[:15]}...")
     
     # Current balance
     try:
         balance = rpc("getbalance", [], wallet=BUSINESS_NAME)
         print(f"💰 Current Balance: {balance} BTC")
     except Exception as e:
         print(f"❌ Error getting balance: {e}")
     
     # Payment history summary
     history = load_payment_history()
     print(f"📈 Total Received: {history['total_received']} BTC")
     print(f"📋 Total Payments: {len(history['payments'])}")
     
     # Last 3 payments
     if history["payments"]:
         print("\n🕒 Recent Payments:")
         for p in history["payments"][-3:]:
             print(f"   {p['time']} - {p['amount']} BTC")

def record_manual_payment(amount, customer_name):
     """Record a manual/cash payment for credit score"""
     history = load_payment_history()
     
     payment = {
         "txid": f"manual_{datetime.now().strftime('%Y%m%d%H%M%S')}",
         "amount": amount,
         "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
         "address": "cash_payment",
         "confirmations": 1,
         "customer": customer_name,
         "type": "manual"
     }
     
     history["payments"].append(payment)
     history["total_received"] += amount
     save_payment_history(history)
     
     print(f"✅ Recorded manual payment: {amount} BTC from {customer_name}")

 # Test it
if __name__ == "__main__":
     show_business_summary()
     check_new_payments()   

     import requests
     import codecs
     import json

     class LNDClient:
         """Connect to LND node for Lightning payments"""
         
         def __init__(self, node_name="ByteCode"):
             """Initialize LND connection for your business node"""
             
             # ===== YOUR ACTUAL PATH FROM POLAR =====
             self.base_path = "C:/Users/roris/.polar/networks/2/volumes/lnd"
             
             # Node-specific paths
             if node_name == "ByteCode":
                 self.cert_path = f"{self.base_path}/ByteCode/tls.cert"
                 self.macaroon_path = f"{self.base_path}/ByteCode/data/chain/bitcoin/regtest/admin.macaroon"
                 self.port = 8081
                 self.node_alias = "ByteCode (Business)"
                 
             elif node_name == "Customer":
                 self.cert_path = f"{self.base_path}/Customer/tls.cert"
                 self.macaroon_path = f"{self.base_path}/Customer/data/chain/bitcoin/regtest/admin.macaroon"
                 self.port = 8082
                 self.node_alias = "Customer"
             else:
                 raise ValueError(f"Unknown node: {node_name}")
             
             self.url = f"https://127.0.0.1:{self.port}"
             
             # Load macaroon
             try:
                 with open(self.macaroon_path, 'rb') as f:
                     macaroon_bytes = f.read()
                     self.macaroon = codecs.encode(macaroon_bytes, 'hex').decode()
                 self.headers = {
                     'Grpc-Metadata-macaroon': self.macaroon,
                     'Content-Type': 'application/json'
                 }
                 print(f"✅ Loaded {self.node_alias} LND credentials")
             except Exception as e:
                 print(f"❌ Error loading LND credentials: {e}")
                 print(f"   Path tried: {self.macaroon_path}")
                 self.macaroon = None
                 self.headers = {}
         
         def _get(self, endpoint):
             """Make GET request to LND API"""
             try:
                 response = requests.get(
                     f"{self.url}{endpoint}",
                     headers=self.headers,
                     verify=self.cert_path,
                     timeout=10
                 )
                 return response.json()
             except Exception as e:
                 print(f"LND GET Error: {e}")
                 return None
         
         def _post(self, endpoint, data):
             """Make POST request to LND API"""
             try:
                 response = requests.post(
                     f"{self.url}{endpoint}",
                     headers=self.headers,
                     json=data,
                     verify=self.cert_path,
                     timeout=10
                 )
                 return response.json()
             except Exception as e:
                 print(f"LND POST Error: {e}")
                 return None
         
         def get_info(self):
             """Get LND node information"""
             return self._get("/v1/getinfo")
         
         def create_invoice(self, amount_sats, memo=""):
             """Create a Lightning invoice"""
             data = {
                 "value": amount_sats,
                 "memo": memo
             }
             return self._post("/v1/invoices", data)
         
         def check_invoice(self, payment_hash):
             """Check if an invoice has been paid"""
             return self._get(f"/v1/invoice/{payment_hash}")
         
         def get_balance(self):
             """Get channel balance"""
             return self._get("/v1/balance/channels")

     #TEST CONNECTION
     if __name__ == "__main__":
         print("="*50)
         print("LND CONNECTION TEST")
         print("="*50)
         
         # Test business node (ByteCode)
         print("\n1. Testing Business Node (ByteCode)...")
         business = LNDClient("ByteCode")
         info = business.get_info()
         
         if info:
             print("✅ SUCCESS! Connected to your Business LND node!")
             print(f"   Node Alias: {info.get('alias', 'Unknown')}")
             print(f"   Public Key: {info.get('identity_pubkey', '')[:20]}...")
             print(f"   Synced: {info.get('synced_to_chain', False)}")
             print(f"   Block Height: {info.get('block_height', 0)}")
         else:
             print("❌ Could not connect to Business LND node")
         
         # Test Customer node
         print("\n2. Testing Customer Node...")
         customer = LNDClient("Customer")
         info = customer.get_info()
         
         if info:
             print("✅ SUCCESS! Connected to Customer LND node!")
         else:
             print("❌ Could not connect to Customer LND node")
             
from rpc_helper import rpc
from lnd_helper import LNDClient
import time
import sys  # Add this for exit()

# ===== YOUR BUSINESS =====
BITCOIN_WALLET = "bytecode"
LND_NODE = "ByteCode"

print("="*50)
print("FUND YOUR LIGHTNING NODE")
print("="*50)

# Step 0: Load Bitcoin wallet
print("\n0. Loading Bitcoin wallet...")
try:
    rpc("loadwallet", [BITCOIN_WALLET])
    print(f"✅ Wallet '{BITCOIN_WALLET}' loaded")
except:
    print("ℹ️ Wallet already loaded")

# Step 1: Get a deposit address from LND
print("\n1. Getting LND deposit address...")
lnd = LNDClient(LND_NODE)
deposit_info = lnd._get("/v1/newaddress")  # Removed ?type=bech32

if deposit_info and "address" in deposit_info:
    deposit_address = deposit_info["address"]
    print(f"✅ LND deposit address: {deposit_address}")
else:
    print("❌ Could not get deposit address")
    print(f"Response: {deposit_info}")
    sys.exit(1)  # Fixed exit()

# Step 2: Send Bitcoin from busiess wallet to LND address
print(f"\n2. Sending 10 BTC from {BITCOIN_WALLET} to LND...")
try:
    txid = rpc("sendtoaddress", [deposit_address, 10], wallet=BITCOIN_WALLET)
    print(f"✅ Transaction sent! TXID: {txid}")
except Exception as e:
    print(f"❌ Error sending: {e}")
    sys.exit(1)  # Fixed exit()

# Step 3: Mine a block to confirm
print("\n3. Mining confirmation block...")
try:
    mining_address = rpc("getnewaddress", [], wallet=BITCOIN_WALLET)
    block = rpc("generatetoaddress", [1, mining_address])
    print(f"✅ Block mined: {block[0][:10]}...")
except Exception as e:
    print(f"❌ Error mining: {e}")
    sys.exit(1)  # Fixed exit()

# Step 4: Check LND balance
print("\n4. Checking LND wallet balance...")
time.sleep(3)
wallet_balance = lnd._get("/v1/balance/wallet")

if wallet_balance:
    confirmed = wallet_balance.get("confirmed_balance", "0")
    unconfirmed = wallet_balance.get("unconfirmed_balance", "0")
    print(f"💰 LND Wallet Balance: {confirmed} sats confirmed")
    print(f"⏳ Unconfirmed: {unconfirmed} sats")
else:
    print("❌ Could not get balance")

print("\n" + "="*50)
print("NEXT STEP: Open a channel with Customer")
print("="*50)             

from rpc_helper import rpc

print("="*50)
print("MATURING COINBASE REWARDS")
print("="*50)

wallet = "bytecode"

# Step 1: Load the wallet
print("\n1. Loading wallet...")
try:
    rpc("loadwallet", [wallet])
    print(f"✅ Wallet '{wallet}' loaded")
except:
    print(f"ℹ️ Wallet already loaded or creating...")
    rpc("createwallet", [wallet])

# Step 2: Get a new address for mining
print("\n2. Getting mining address...")
address = rpc("getnewaddress", [], wallet=wallet)
print(f"✅ Mining address: {address}")

# Step 3: Check current spendable balance
print("\n3. Checking spendable balance...")
balance = rpc("getbalance", [], wallet=wallet)
print(f"💰 Current spendable balance: {balance} BTC")

# Step 4: Mine blocks if needed
if balance < 10:
    print(f"\n4. Mining 100 blocks to mature coins...")
    blocks = rpc("generatetoaddress", [100, address])
    print(f"✅ Mined {len(blocks)} blocks")
    
    # Check new balance
    new_balance = rpc("getbalance", [], wallet=wallet)
    print(f"💰 New spendable balance: {new_balance} BTC")
else:
    print(f"\n4. ✅ Enough spendable balance!")

print("\n" + "="*50)
print("Now you can run fund_lnd.py!")
print("="*50)

from lnd_helper import LNDClient
import time
import sys

# BUSINESS LND NODE
LND_NODE = "ByteCode"
CUSTOMER_NODE = "Customer"

print("="*50)
print("OPEN LIGHTNING CHANNEL WITH CUSTOMER")
print("="*50)
 
# Step 1: Connect to your node and customer node
print("\n1. Connecting to LND nodes...")
business = LNDClient(LND_NODE)
customer = LNDClient(CUSTOMER_NODE)

# Step 2: Get Customer's pubkey
print("\n2. Getting Customer's public key...")
customer_info = customer.get_info()
if customer_info:
    customer_pubkey = customer_info.get("identity_pubkey")
    print(f"✅ Customer pubkey: {customer_pubkey[:20]}...")
else:
    print("❌ Could not get Customer info")
    sys.exit(1)

# Step 3: Connect business to customer
print(f"\n3. Connecting Business to Customer...")
try:
    connect_result = business._post("/v1/peers", {
        "addr": {
            "pubkey": customer_pubkey,
            "host": "127.0.0.1:9736"  # Customer's P2P port from Polar
        }
    })
    print("✅ Connected to Customer")
except Exception as e:
    print(f"ℹ️ Already connected or error: {e}")

# Step 4: Open channel
print("\n4. Opening 5,000,000 sat channel...")
try:
    channel = business._post("/v1/channels", {
        "node_pubkey": customer_pubkey,
        "local_funding_amount": 5000000,  # 5M sats = 0.05 BTC
        "push_sat": 0,  # Don't push any sats to customer yet
        "private": False
    })
    print(f"✅ Channel opening initiated!")
    print(f"   Funding tx: {channel.get('funding_txid', '')[:20]}...")
except Exception as e:
    print(f"❌ Error opening channel: {e}")
    sys.exit(1)

# Step 5: Mine blocks to confirm channel
print("\n5. Mining 6 blocks to confirm channel...")
from rpc_helper import rpc
mining_address = rpc("getnewaddress", [], wallet="bytecode")
blocks = rpc("generatetoaddress", [6, mining_address])
print(f"✅ Mined {len(blocks)} blocks")

# Step 6: Check channel balance
print("\n6. Checking channel balance...")
time.sleep(2)
channels = business._get("/v1/channels")
if channels and "channels" in channels:
    for ch in channels["channels"]:
        if ch.get("remote_pubkey")[:10] == customer_pubkey[:10]:
            print(f"✅ Channel active!")
            print(f"   Capacity: {ch.get('capacity', 0)} sats")
            print(f"   Local balance: {ch.get('local_balance', 0)} sats")
            print(f"   Remote balance: {ch.get('remote_balance', 0)} sats")
            break
else:
    print("⏳ Waiting for channel to appear...")

print("\n" + "="*50)
print("CHANNEL OPENED! READY TO RECEIVE LIGHTNING PAYMENTS! ⚡")
print("="*50)

from rpc_helper import rpc

# Mine 6 more blocks to confirm the LND deposit
addr = rpc("getnewaddress", [], wallet="bytecode")
blocks = rpc("generatetoaddress", [6, addr])
print(f"Mined {len(blocks)} blocks")