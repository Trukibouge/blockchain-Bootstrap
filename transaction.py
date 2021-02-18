from key import verify_signature


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: int, timestamp=0, tx_id=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.tx_id = tx_id

    def __repr__(self) -> str:
        string = "Number: " + str(self.tx_id) + " || Sender: " + self.sender + " || Receiver: " + self.receiver + " || Amount: " + str(self.amount) + " || Timestamp: " + str(self.timestamp)
        return string

    def to_dict(self) -> dict:
        return {
            "tx_id": self.tx_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }