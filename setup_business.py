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