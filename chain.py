import time
import json
import copy
from block import Block
from transaction import Transaction


class Blockchain:
    def __init__(self, difficulty: int, blocks=[], block_reward=50) -> None:
        self.tokens = {}
        self.blocks = []
        self.transaction_pool = []
        self.difficulty = difficulty
        self.block_reward = block_reward
        for block in blocks:
            new = Block(index=block["index"],prev_hash=block["prev_hash"],nonce=block["nonce"],
                        timestamp=block["timestamp"],transactions=block["transactions"],
                        hash_val=block["hash_val"],miner_name=block["miner_name"], signature=block["signature"])
            self.blocks.append(new)
        self.update_token()

    def __repr__(self):
        out = "Difficulty: " + str(self.difficulty) + "\nBlocks: " + str(self.blocks) + "\nBlock Reward: " + str(self.block_reward)
        return out

    def assign_block_reward(self, block, wallet=None):
        if wallet:
            block.add_transaction(receiver='miner', sender=wallet.to_address(), amount=self.block_reward, timestamp=time.time())
            block.transactions[-1].sign(wallet)
        else:
            block.add_transaction(receiver="me", sender="network", amount=self.block_reward, timestamp=time.time())

    def create_genesis_block(self, wallet=None) -> Block:
        newBlock = Block(0, "")
        self.assign_block_reward(newBlock, wallet)
        newBlock.mine(self.difficulty, wallet)
        self.blocks.append(newBlock)
        self.update_token()
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
        self.assign_block_reward(newBlock, wallet)
        for transaction in self.transaction_pool:
            newBlock.add_transaction(receiver=transaction.receiver, sender=transaction.sender, amount=transaction.amount, timestamp=transaction.timestamp, signature=transaction.signature)
        self.reset_transaction_pool()
        newBlock.mine(self.difficulty, wallet)
        self.blocks.append(newBlock)
        self.update_token()
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

    def update_token(self) -> None:
        self.tokens = {}
        for block in self.blocks:
            for transaction in block.transactions:
                if transaction.receiver == "miner":
                    if self.tokens.get(transaction.sender):
                        self.tokens[transaction.sender] += transaction.amount
                    else:
                        self.tokens[transaction.sender] = transaction.amount

                else:
                    if self.tokens.get(transaction.sender):
                        self.tokens[transaction.sender] -= transaction.amount
                    else:
                        self.tokens[transaction.sender] = -transaction.amount

                    if self.tokens.get(transaction.receiver):
                        self.tokens[transaction.receiver] += transaction.amount
                    else:
                        self.tokens[transaction.receiver] = transaction.amount

    def get_wealth(self, address: str):
        if self.tokens[address]:
            return self.tokens[address]
        else:
            print("Address not found")
            return None

    def export_json(self) -> str:
        j = json.dumps(self.to_dict())
        print(j)
        return j
