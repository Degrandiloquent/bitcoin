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