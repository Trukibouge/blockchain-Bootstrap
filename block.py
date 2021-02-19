import hashlib
import time

from transaction import Transaction
from key import verify_signature, BitcoinAccount


class Block:
    def __init__(self, index: int, prev_hash: str, transactions=[], nonce=0, hash_val=None, miner_name=None, timestamp=0, signature=None):
        self.transactions = []
        for transaction in transactions:
            new = Transaction(tx_id=transaction['tx_id'],receiver=transaction['receiver'],
                              sender=transaction['sender'],amount=transaction['amount'],
                              timestamp=transaction['timestamp'])
            self.transactions.append(new)
        self.index = index
        self.hash_val = hash_val
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.miner_name = miner_name
        self.timestamp = timestamp
        self.signature = signature

    def __repr__(self):
        out = "Index: " + str(self.index) + "\nTime: " + str(self.timestamp) + "\nMiner: " + str(self.miner_name) + "\nTransactions: " + str(self.transactions) + "\nPrevious hash: " + self.prev_hash + "\nHash: " + self.hash_val
        if self.signature:
            out += "\nSignature: " + str(self.signature.hex())
        return out

    def add_transaction(self, receiver: str, sender: str, amount: int, timestamp=time.time(), signature=None) -> None:
        transaction = Transaction(receiver=receiver, sender=sender, amount=amount, timestamp=timestamp, signature=signature)
        transaction.tx_id = len(self.transactions)
        self.transactions.append(transaction)

    # def add_transaction(self, transaction: Transaction):
    #     newTrans = Transaction(receiver=transaction.receiver, sender=transaction.sender, amount=transaction.amount, timestamp=transaction.amount, signature=transaction.signature)
    #     newTrans.tx_id = len(self.transactions)
    #     self.transactions.append(newTrans)

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

    def mine(self, difficulty, wallet: BitcoinAccount) -> int:
        self.timestamp = time.time()
        nonce = 0
        prefix = '0' * difficulty
        hash_val = self.hashBlock(nonce)
        while not hash_val.startswith(prefix):
            nonce += 1
            hash_val = self.hashBlock(nonce)
        self.hash_val = hash_val
        self.nonce = nonce
        if wallet:
            self.miner_name = wallet.to_address()
            self.sign(wallet)
        else:
            self.miner_name = "name"
        return nonce

    def sign(self, wallet: BitcoinAccount):
        message = str(self.hash_val)
        self.signature = wallet.sign(message)

    def verify_signature(self):
        result = True
        for transaction in self.transactions:
            if not transaction.verify_signature():
                result = False
        if not verify_signature(self.signature.hex(), str(self.hash_val), self.miner_name):
            result = False
        return result

    def to_dict(self) -> dict:
        dic = {
            "index": self.index,
            "hash_val": self.hash_val,
            "prev_hash": self.prev_hash,
            "miner_name": self.miner_name,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "transactions": []
        }
        for transaction in self.transactions:
            dic['transactions'].append(transaction.to_dict())
        return dic
