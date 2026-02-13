from rpc_helper import rpc

print("="*50)
print("CREATE/VERIFY WALLETS")
print("="*50)

# Business wallet - THIS IS THE ONLY ONE YOU NEED
BUSINESS_NAME = "bytecode"

print(f"\n=== SETTING UP BUSINESS WALLET: {BUSINESS_NAME} ===")

# Try to load existing wallet
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