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