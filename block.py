import hashlib
import time

from transaction import Transaction
from key import verify_signature


class Block:
    def __init__(self, index: int, prev_hash: str, transactions=[], nonce=0, hash_val=None, miner_name=None, timestamp=0):
        self.transactions = list(transactions)
        # for elem in transactions:
        #     self.transactions.append(Transaction(elem["sender"],elem["receiver"],elem["amount"],elem["timestamp"],
        #                              elem["tx_number"]))
        self.index = index
        self.hash_val = hash_val
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.miner_name = miner_name
        self.timestamp = timestamp

    def __repr__(self):
        out = "Index: " + str(self.index) + "\nTime: " + str(self.timestamp) + "\nMiner: " + str(self.miner_name) + "\nTransactions: " + str(self.transactions) + "\nPrevious hash: " + self.prev_hash + "\nHash: " + self.hash_val
        return out

    def addTransaction(self, tx: Transaction) -> None:
        transaction = tx
        tx.tx_id = len(self.transactions)
        self.transactions.append(transaction)

    def hashBlock(self, nonce) -> str:
        sha = hashlib.sha256()
        data = str(self.index) + str(self.timestamp) + str(nonce) + str(self.prev_hash)
        for transaction in self.transactions:
            data += str(transaction.sender) + str(transaction.receiver) + str(transaction.amount)
        sha.update(data.encode())
        return sha.hexdigest()

    def checkHash(self, nonce) -> bool:
        computed = self.hashBlock(nonce)
        if computed != self.hash_val:
            return False
        return True

    def mine(self, difficulty) -> int:
        self.timestamp = time.time()
        nonce = 0
        prefix = '0' * difficulty
        hash_val = self.hashBlock(nonce)
        while not hash_val.startswith(prefix):
            nonce += 1
            hash_val = self.hashBlock(nonce)
        self.hash_val = hash_val
        self.nonce = nonce
        self.miner_name = "name"
        return nonce
