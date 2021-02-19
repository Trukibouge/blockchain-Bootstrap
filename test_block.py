import json
import time
from transaction import Transaction
from block import Block
from key import BitcoinAccount

wallet = BitcoinAccount()

difficulty = 4

first_block = Block(0, "")

first_block.add_transaction("mohamed", "justine", 50, time.time())
first_block.mine(difficulty)

print("First block is: ")

print(first_block)

last_hash = first_block.hash_val

second_block = Block(1, last_hash)

second_block.mine(difficulty)

print("Second block is: ")

print(second_block)

print(json.dumps(second_block.to_dict()))


