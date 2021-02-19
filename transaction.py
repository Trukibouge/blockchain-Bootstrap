import hashlib
import time

from key import verify_signature, BitcoinAccount


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, timestamp=time.time(), tx_id=None, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.tx_id = tx_id
        self.signature = signature

    def __repr__(self) -> str:
        string = "Number: " + str(self.tx_id) + " || Sender: " + self.sender + " || Receiver: " + self.receiver + " || Amount: " + str(self.amount) + " || Timestamp: " + str(self.timestamp)
        if self.signature:
            string += " || Signature: " + str(self.signature.hex()) + "\n"
        return string

    def sign(self, wallet: BitcoinAccount):
        message = str(self.sender) + str(self.receiver) + str(self.amount)
        if wallet:
            signature = wallet.sign(message)
            self.signature = signature

    def verify_signature(self):
        message = str(self.sender) + str(self.receiver) + str(self.amount)
        return verify_signature(self.signature.hex(), message, self.sender)


    def to_dict(self) -> dict:
        return {
            "tx_id": self.tx_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }