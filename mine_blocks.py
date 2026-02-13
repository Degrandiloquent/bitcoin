from rpc_helper import rpc

# Mine 6 more blocks to confirm the LND deposit
addr = rpc("getnewaddress", [], wallet="bytecode")
blocks = rpc("generatetoaddress", [6, addr])
print(f"Mined {len(blocks)} blocks")