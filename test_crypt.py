import json
import time
from transaction import Transaction
from block import Block
from key import BitcoinAccount

wallet = BitcoinAccount()

difficulty = 4

first_block = Block(0, "")

first_block.add_transaction(sender=wallet.to_address(), receiver="justine", amount=50)
first_block.transactions[-1].sign(wallet)
print(first_block.transactions[-1].verify_signature())
first_block.mine(difficulty, wallet)
print(first_block.verify_signature())
last_hash = first_block.hash_val
