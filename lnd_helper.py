import requests
import codecs
import json

class LNDClient:
    """Connect to LND node for Lightning payments"""
    
    def __init__(self, node_name="ByteCode"):
        """Initialize LND connection for your business node"""
        
        # ===== YOUR ACTUAL PATH FROM POLAR =====
        self.base_path = "C:/Users/roris/.polar/networks/2/volumes/lnd"
        
        # Node-specific paths
        if node_name == "ByteCode":
            self.cert_path = f"{self.base_path}/ByteCode/tls.cert"
            self.macaroon_path = f"{self.base_path}/ByteCode/data/chain/bitcoin/regtest/admin.macaroon"
            self.port = 8081
            self.node_alias = "ByteCode (Business)"
            
        elif node_name == "Customer":
            self.cert_path = f"{self.base_path}/Customer/tls.cert"
            self.macaroon_path = f"{self.base_path}/Customer/data/chain/bitcoin/regtest/admin.macaroon"
            self.port = 8082
            self.node_alias = "Customer"
        else:
            raise ValueError(f"Unknown node: {node_name}")
        
        self.url = f"https://127.0.0.1:{self.port}"
        
        # Load macaroon
        try:
            with open(self.macaroon_path, 'rb') as f:
                macaroon_bytes = f.read()
                self.macaroon = codecs.encode(macaroon_bytes, 'hex').decode()
            self.headers = {
                'Grpc-Metadata-macaroon': self.macaroon,
                'Content-Type': 'application/json'
            }
            print(f"✅ Loaded {self.node_alias} LND credentials")
        except Exception as e:
            print(f"❌ Error loading LND credentials: {e}")
            print(f"   Path tried: {self.macaroon_path}")
            self.macaroon = None
            self.headers = {}
    
    def _get(self, endpoint):
        """Make GET request to LND API"""
        try:
            response = requests.get(
                f"{self.url}{endpoint}",
                headers=self.headers,
                verify=self.cert_path,
                timeout=10
            )
            return response.json()
        except Exception as e:
            print(f"LND GET Error: {e}")
            return None
    
    def _post(self, endpoint, data):
        """Make POST request to LND API"""
        try:
            response = requests.post(
                f"{self.url}{endpoint}",
                headers=self.headers,
                json=data,
                verify=self.cert_path,
                timeout=10
            )
            return response.json()
        except Exception as e:
            print(f"LND POST Error: {e}")
            return None
    
    def get_info(self):
        """Get LND node information"""
        return self._get("/v1/getinfo")
    
    def create_invoice(self, amount_sats, memo=""):
        """Create a Lightning invoice"""
        data = {
            "value": amount_sats,
            "memo": memo
        }
        return self._post("/v1/invoices", data)
    
    def check_invoice(self, payment_hash):
        """Check if an invoice has been paid"""
        return self._get(f"/v1/invoice/{payment_hash}")
    
    def get_balance(self):
        """Get channel balance"""
        return self._get("/v1/balance/channels")

#TEST CONNECTION
if __name__ == "__main__":
    print("="*50)
    print("LND CONNECTION TEST")
    print("="*50)
    
    # Test business node (ByteCode)
    print("\n1. Testing Business Node (ByteCode)...")
    business = LNDClient("ByteCode")
    info = business.get_info()
    
    if info:
        print("✅ SUCCESS! Connected to your Business LND node!")
        print(f"   Node Alias: {info.get('alias', 'Unknown')}")
        print(f"   Public Key: {info.get('identity_pubkey', '')[:20]}...")
        print(f"   Synced: {info.get('synced_to_chain', False)}")
        print(f"   Block Height: {info.get('block_height', 0)}")
    else:
        print("❌ Could not connect to Business LND node")
    
    # Test Customer node
    print("\n2. Testing Customer Node...")
    customer = LNDClient("Customer")
    info = customer.get_info()
    
    if info:
        print("✅ SUCCESS! Connected to Customer LND node!")
    else:
        print("❌ Could not connect to Customer LND node")