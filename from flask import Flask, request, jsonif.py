from flask import Flask, request, jsonify
from rpc_helper import rpc
from lnd_helper import LNDClient
import json
import os
from datetime import datetime

app = Flask(__name__)

#BUSINESS INFO 
BUSINESS_NAME = "bytecode"
BITCOIN_WALLET = "bytecode"
LND_NODE = "ByteCode"

# Initialize LND
lnd = LNDClient(LND_NODE)

# Create invoices directory if it doesn't exist
os.makedirs("invoices", exist_ok=True)

#API ENDPOINTS FOR FRONTEND

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if backend is running"""
    return jsonify({
        "status": "online",
        "business": BUSINESS_NAME,
        "time": datetime.now().isoformat()
    })

@app.route('/api/bitcoin/address', methods=['GET'])
def get_bitcoin_address():
    """Get new Bitcoin address for on-chain payments"""
    try:
        address = rpc("getnewaddress", [], wallet=BITCOIN_WALLET)
        return jsonify({
            "success": True,
            "address": address,
            "currency": "BTC",
            "network": "regtest"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/lightning/invoice', methods=['POST'])
def create_lightning_invoice():
    """Create Lightning invoice for instant payments"""
    data = request.json
    amount_sats = data.get('amount')
    description = data.get('description', 'Payment to ByteCode')
    
    try:
        invoice = lnd.create_invoice(amount_sats, description)
        
        if invoice and "payment_request" in invoice:
            # Clean hash for filename
            safe_hash = invoice["r_hash"][:8].replace('/', '_').replace('\\', '_')
            
            # Store invoice
            invoice_data = {
                "timestamp": datetime.now().isoformat(),
                "amount_sats": amount_sats,
                "description": description,
                "payment_hash": invoice["r_hash"],
                "payment_request": invoice["payment_request"],
                "settled": False
            }
            
            with open(f"invoices/{safe_hash}.json", "w") as f:
                json.dump(invoice_data, f)
            
            return jsonify({
                "success": True,
                "payment_request": invoice["payment_request"],
                "payment_hash": invoice["r_hash"],
                "amount": amount_sats,
                "expiry": 3600
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to create invoice"
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/lightning/check/<payment_hash>', methods=['GET'])
def check_lightning_payment(payment_hash):
    """Check if Lightning invoice has been paid"""
    try:
        invoice_status = lnd.check_invoice(payment_hash)
        
        if invoice_status:
            settled = invoice_status.get("settled", False)
            return jsonify({
                "success": True,
                "settled": settled,
                "amount": invoice_status.get("amt_paid_sat", 0),
                "paid_at": datetime.now().isoformat() if settled else None
            })
        else:
            return jsonify({
                "success": False,
                "error": "Invoice not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/bitcoin/balance', methods=['GET'])
def get_balance():
    """Get business Bitcoin balance"""
    try:
        balance = rpc("getbalance", [], wallet=BITCOIN_WALLET)
        return jsonify({
            "success": True,
            "balance": balance,
            "currency": "BTC"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/lightning/balance', methods=['GET'])
def get_lightning_balance():
    """Get business Lightning balance"""
    try:
        wallet_balance = lnd._get("/v1/balance/wallet")
        channel_balance = lnd._get("/v1/balance/channels")
        
        return jsonify({
            "success": True,
            "wallet_balance": wallet_balance.get("confirmed_balance", 0) if wallet_balance else 0,
            "channel_balance": channel_balance.get("balance", 0) if channel_balance else 0,
            "unit": "sats"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get recent transactions"""
    try:
        limit = request.args.get('limit', 10, type=int)
        txs = rpc("listtransactions", ["*", limit], wallet=BITCOIN_WALLET)
        
        transactions = []
        for tx in txs:
            if tx.get("category") in ["receive", "generate"]:
                transactions.append({
                    "txid": tx["txid"],
                    "amount": tx["amount"],
                    "time": datetime.fromtimestamp(tx["time"]).isoformat(),
                    "confirmations": tx["confirmations"],
                    "category": tx["category"]
                })
        
        return jsonify({
            "success": True,
            "transactions": transactions
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)    
    print("="*50)
    print(f"🚀 STARTING BACKEND API FOR {BUSINESS_NAME}")
    print("="*50)
    print("📡 Endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/bitcoin/address")
    print("   POST /api/lightning/invoice")
    print("   GET  /api/lightning/check/<hash>")
    print("   GET  /api/bitcoin/balance")
    print("   GET  /api/lightning/balance")
    print("   GET  /api/transactions")
    print("="*50)
    app.run(host='127.0.0.1', port=5000, debug=True)