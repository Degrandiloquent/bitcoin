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