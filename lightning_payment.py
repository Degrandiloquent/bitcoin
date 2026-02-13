from lnd_helper import LNDClient
import json
from datetime import datetime

# BUSINESS LIGHTNING NODE
business = LNDClient("ByteCode")

def create_invoice(amount_sats, product_name):
    """Create a Lightning invoice for a customer"""
    
    print(f"\n=== CREATING LIGHTNING INVOICE ===")
    print(f"Product: {product_name}")
    print(f"Amount: {amount_sats} sats")
    
    # Create the invoice
    invoice = business.create_invoice(amount_sats, f"Payment for {product_name}")
    
    if invoice and "payment_request" in invoice:
        payment_request = invoice["payment_request"]
        payment_hash = invoice["r_hash"]
        
        print(f"✅ Invoice created!")
        print(f"📋 Payment Request: {payment_request[:50]}...")
        print(f"🔑 Payment Hash: {payment_hash[:20]}...")
        
        # Clean the payment hash for filename (remove invalid characters)
        safe_hash = payment_hash[:8].replace('/', '_').replace('\\', '_')
        
        # Save invoice details
        invoice_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount_sats": amount_sats,
            "product": product_name,
            "payment_hash": payment_hash,
            "payment_request": payment_request,
            "settled": False
        }
        
        filename = f"invoice_{safe_hash}.json"
        with open(filename, "w") as f:
            json.dump(invoice_data, f, indent=2)
        print(f"✅ Invoice saved to {filename}")
        
        return invoice_data
    else:
        print("❌ Failed to create invoice")
        return None

def check_payment(payment_hash):
    """Check if an invoice has been paid"""
    
    print(f"\n=== CHECKING PAYMENT STATUS ===")
    
    invoice_status = business.check_invoice(payment_hash)
    
    if invoice_status:
        settled = invoice_status.get("settled", False)
        if settled:
            print(f"✅ PAYMENT RECEIVED!")
            print(f"💰 Amount: {invoice_status.get('amt_paid_sat', 0)} sats")
            return True
        else:
            print(f"⏳ Waiting for payment...")
            return False
    else:
        print(f"❌ Could not check invoice")
        return False

# ===== TEST IT =====
if __name__ == "__main__":
    # Create a test invoice for 1000 sats
    invoice = create_invoice(1000, "Test Product")
    
    if invoice:
        print(f"\n📋 Full Invoice:")
        print(f"Payment Request: {invoice['payment_request']}")
        
        # Save payment request to text file
        with open("latest_invoice.txt", "w") as f:
            f.write(invoice['payment_request'])
        print(f"✅ Payment request saved to latest_invoice.txt")
        
        print(f"\n🔹 NEXT STEPS:")
        print(f"1. In Polar, click on Customer node")
        print(f"2. Go to Terminal tab")
        print(f"3. Type: payinvoice {invoice['payment_request'][:30]}...")
        print(f"4. Watch payment confirm!")