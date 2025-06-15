# import web3
# import json
#
# w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:7545'))
#
# if not w3.is_connected():
#     raise Exception("无法连接到以太坊节点，请检查 RPC 端点")
# # abi = "[{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"a\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"b\",\"type\":\"uint256\"}],\"name\":\"add\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"x\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"y\",\"type\":\"uint256\"}],\"name\":\"mul\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"a\",\"type\":\"uint256\"}],\"name\":\"sqr\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"x\",\"type\":\"uint256\"}],\"name\":\"sqrt\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"y\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"a\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"b\",\"type\":\"uint256\"}],\"name\":\"sub\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"}]"
# with open("abi.json", "r") as file:
#     abi = json.load(file)
#
# contract_address = web3.Web3.to_checksum_address('0xb5a0d66b1d3d99865f3c51ce9abcda556bb8efcd')
#
# c = w3.eth.contract(address=contract_address, abi=abi)
#
# a=5
# b=4
#
# rtn= c.caller().add(a,b)
# print(f"{a}+{b}={rtn}")

import web3
import json

print("start")

# 连接到Holesky测试网
w3 = web3.Web3(web3.HTTPProvider('https://holesky.drpc.org'))

if not w3.is_connected():
    raise Exception("can't eth")


# 加载合约ABI
with open("D:\\pythonProject2\\abi3.json", "r") as file:
    abi = json.load(file)

# 合约地址
contract_address = web3.Web3.to_checksum_address('0x94589f02989f5ffb55dff5280bf213446da15aec')

# 创建合约实例
contract = w3.eth.contract(address=contract_address, abi=abi)

# 设置账户地址
account_address = '0x3cc62ea2922ca9bf988FD91Bf38Dff7e3610072F'

# 构建mintNFT交易
metafile = "https://ipfs.io/ipfs/bafybeia5jclv52fxvcxpker5i7v3bpx555rcnw4emawmpr5ztbipubafcm/medal5.json"

# 获取当前nonce
nonce = w3.eth.get_transaction_count(account_address)

# 构建交易
transaction = contract.functions.mintNFT(metafile).build_transaction({
    'from': account_address,
    'nonce': nonce,
    'gas': 20000002,  # 设置足够的gas
    'gasPrice': w3.eth.gas_price,
})

# 使用私钥签名交易
private_key = '98bbc6dbd4dbf4e51ff4d0baaff1393aa27f3530e91fa1426cf9bdd3eb8a2df6'
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
print(f"Transaction sent, hash: {tx_hash.hex()}")

# 等待交易确认
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Transaction confirmed, block number: {receipt.blockNumber}")
