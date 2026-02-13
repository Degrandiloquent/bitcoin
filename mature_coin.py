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
