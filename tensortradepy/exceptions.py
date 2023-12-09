# Exceptions to send more explicit errors

class WrongAPIKeyException(Exception):
    """
    Raised if no working API key is provided (the Tensor server returns 403
    errors)
    """
    pass


class NotListedException(Exception):
    """
    Raised if the related NFT is not listed on Tensor Trade. It is raised even
    if the NFT is listed on another marketplace like Magic Eden.
    """
    pass


class TransactionFailedException(Exception):
    """
    Raised when the Solana transaction fails to execute.
    """
    pass
