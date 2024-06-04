


class BookNotInitiatedError(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        


class IncorrectLevelDataType(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)