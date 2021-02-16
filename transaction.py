from key import verify_signature


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float, timestamp=0, tx_number=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.tx_id = tx_number

    def __repr__(self) -> str:
        string = "Number: " + str(self.tx_id) + "\nSender: " + self.sender + "\nReceiver: " + self.receiver + "\nAmount: " + str(self.amount) + "\nTimestamp: " + str(self.timestamp)
        return string

    def to_dict(self) -> dict:
        tx_dict = {
            "tx_number": self.tx_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        return tx_dict