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
