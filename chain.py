import time
import json
import copy
from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, difficulty: int, blocks=[], block_reward=50) -> None:
        self.blocks = []
        self.transaction_pool = []
        self.difficulty = difficulty
        self.block_reward = block_reward
        for block in blocks:
            new = Block(index=block["index"],prev_hash=block["prev_hash"],nonce=block["nonce"],
                        timestamp=block["timestamp"],transactions=block["transactions"],
                        hash_val=block["hash_val"],miner_name=block["miner_name"])
            self.blocks.append(new)

    def __repr__(self):
        out = "Difficulty: " + str(self.difficulty) + "\nBlocks: " + str(self.blocks) + "\nBlock Reward: " + str(self.block_reward)
        return out

    def create_genesis_block(self, wallet=None) -> Block:
        newBlock = Block(0, "")
        if wallet:
            newBlock.add_transaction(receiver=wallet.to_address(), sender="network", amount=self.block_reward, timestamp=time.time())
        else:
            newBlock.add_transaction(receiver="me", sender="network", amount=self.block_reward, timestamp=time.time())
        newBlock.mine(self.difficulty, wallet)


        self.blocks.append(newBlock)
        return newBlock

    def addPeerBlock(self, block: Block) -> Block:
        lastBlock = self.blocks[-1]
        if block.timestamp < lastBlock.timestamp:
            raise ValueError("Timestamp of new block before timestamp of last")
        if block.index != lastBlock.index + 1:
            raise ValueError("Index error")
        if block.prev_hash != lastBlock.hash_val:
            raise ValueError("Hash inconsistence")
        if not block.checkHash(block.nonce):
            raise ValueError("Corrupted Block")
        self.blocks.append(block)
        return block

    def mine_block(self, wallet=None) -> Block:
        newBlock = Block(len(self.blocks), self.blocks[-1].hash_val)
        newBlock.add_transaction(receiver="me", sender="network", amount=self.block_reward, timestamp=time.time())
        for transaction in self.transaction_pool:
            newBlock.add_transaction(receiver=transaction.receiver, sender=transaction.sender, amount=transaction.amount, timestamp=transaction.timestamp, signature=transaction.signature)
        self.reset_transaction_pool()
        newBlock.mine(self.difficulty, wallet)
        self.blocks.append(newBlock)
        return newBlock

    def add_transaction(self, receiver, sender, amount, signature=None) -> Transaction:
        transaction = Transaction(sender=sender, receiver=receiver, amount=amount, timestamp=time.time(), tx_id=len(self.transaction_pool), signature=signature)
        self.transaction_pool.append(transaction)
        return transaction

    # def add_transaction(self, transaction: Transaction):
    #     newTrans = Transaction(receiver=transaction.receiver, sender=transaction.sender, amount=transaction.amount, timestamp=transaction.amount, signature=transaction.signature)
    #     self.transaction_pool.append(newTrans)

    def reset_transaction_pool(self) -> None:
        self.transaction_pool.clear()

    def verify(self) -> bool:
        for block in self.blocks:
            if not block.checkHash(block.nonce) or not block.verify_signature():
                block.__repr__()
                return False
        return True

    def to_dict(self) -> dict:
        dic = {
            "difficulty": self.difficulty,
            "block_reward": self.block_reward,
            "transaction_pool": [],
            "blocks": [],
        }
        for transaction in self.transaction_pool:
            dic["transaction_pool"].append(transaction.to_dict())
        for block in self.blocks:
            dic["blocks"].append(block.to_dict())
        return dic

    def export_json(self) -> str:
        j = json.dumps(self.to_dict())
        print(j)
        return j
