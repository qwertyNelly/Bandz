class WalletNotFoundError(Exception):
    """Wallet was not found - good luck"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class PositionAlreadyExists(Exception):
    """Position already exists - We cannot create another. You must modify"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
