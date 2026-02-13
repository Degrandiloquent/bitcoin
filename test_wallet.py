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