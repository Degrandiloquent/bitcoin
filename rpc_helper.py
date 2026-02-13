import requests
import json

def rpc(method, params=None, wallet=None):
    """Connect to Bitcoin Core RPC"""
    
    # Base URL for Bitcoin Core
    if wallet:
        # For wallet-specific commands
        url = f"http://127.0.0.1:18443/wallet/{wallet}"
    else:
        # For general commands
        url = "http://127.0.0.1:18443/"
    
    # RPC authentication - Polar default
    auth = ("polaruser", "polarpass")
    
    # Prepare the JSON-RPC request
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "1.0",
        "id": "explorer",
        "method": method,
        "params": params or []
    }
    
    try:
        # Send the request
        response = requests.post(url, 
                               json=payload, 
                               headers=headers, 
                               auth=auth)
        
        # Check for errors
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            return None
            
        # Parse JSON response
        result = response.json()
        
        # Check for RPC error
        if result.get("error"):
            print(f"RPC Error: {result['error']}")
            return None
            
        # Return the result
        return result["result"]
        
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

# Test the connection
if __name__ == "__main__":
    print("Testing Bitcoin Core connection...")
    info = rpc("getblockchaininfo")
    if info:
        print("✅ Connected to Bitcoin Core!")
        print(f"Chain: {info['chain']}")
        print(f"Blocks: {info['blocks']}")
    else:
        print("❌ Could not connect to Bitcoin Core")