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