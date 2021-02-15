from key import verify_signature


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float, tx_number: int, timestamp=0):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.tx_number = tx_number

    def __repr__(self) -> str:
        string = "Number: " + str(self.tx_number) + "Sender: " + self.sender + "Receiver: " + self.receiver + "Amount: " + str(self.amount) + "Timestamp: " + str(self.timestamp)
        return string

    def to_dict(self) -> dict:
        tx_dict = {
            "tx_number": self.tx_number,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        return tx_dict
