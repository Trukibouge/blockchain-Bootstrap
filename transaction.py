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
        string = "\nNumber: " + str(self.tx_id) + "\nSender: " + self.sender + "\nReceiver: " + self.receiver + "\nAmount: " + str(self.amount) + "\nTimestamp: " + str(self.timestamp)
        if self.signature:
            string += "\nSignature: " + str(self.signature) + "\n"
        return string

    def sign(self, wallet: BitcoinAccount):
        message = str(self.sender) + str(self.receiver) + str(self.amount)
        if wallet:
            self.signature = wallet.sign(message).hex()

    def verify_signature(self):
        message = str(self.sender) + str(self.receiver) + str(self.amount)
        return verify_signature(self.signature, message, self.sender)


    def to_dict(self) -> dict:
        return {
            "tx_id": self.tx_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }