import time
import copy
from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, difficulty: int, blocks=[], block_reward=50) -> None:
        self.blocks = []
        self.transaction_pool = []
        self.difficulty = difficulty
        self.block_reward = block_reward
        self.create_genesis_block()
        for block in blocks:
            self.blocks.append(block)

    def create_genesis_block(self) -> Block:
        newBlock = Block(0, "")
        new_transaction = Transaction("network", "me", amount=self.block_reward, timestamp=time.time())
        newBlock.addTransaction(new_transaction)
        newBlock.mine(self.difficulty)
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

    def mine_block(self) -> Block:
        newBlock = Block(len(self.blocks)-1, self.blocks[-1].hash_val)
        for transaction in self.transaction_pool:
            newBlock.addTransaction(transaction)
        self.reset_transaction_pool()
        reward_transaction = Transaction("network", "me", amount=self.block_reward, timestamp=time.time())
        newBlock.addTransaction(reward_transaction)
        newBlock.mine(self.difficulty)
        self.blocks.append(newBlock)
        return newBlock

    def add_transaction(self, receiver, sender, amount) -> Transaction:
        transaction = Transaction(sender=sender, receiver=receiver, amount=amount, timestamp=time.time(), tx_number=len(self.transaction_pool))
        self.transaction_pool.append(transaction)
        return transaction

    def reset_transaction_pool(self) -> None:
        self.transaction_pool.clear()

    def verify(self) -> bool:
        for block in self.blocks:
            if not block.checkHash():
                block.__repr__()
                return False
        return True

    def export_json(self) -> str:
        pass
