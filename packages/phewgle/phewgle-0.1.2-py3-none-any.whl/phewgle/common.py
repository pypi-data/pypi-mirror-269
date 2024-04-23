
import os
from hashlib import md5
from enum import StrEnum
from dotenv import load_dotenv
from keyring import get_password
from keyring import set_password
from keyring import set_keyring
from keyrings.cryptfile.cryptfile import CryptFileKeyring


load_dotenv()


class ActionType(StrEnum):
    BUY = "B"
    SELL = "S"


class APCode(StrEnum):
    COMMON = "1"            # aka 1,000 shares
    AFTER_MARKET = "2"
    ODD = "3"               # single share after market
    EMERGING_MARKET = "4"   # emerging market stock
    INTRA_DAY = "5"         # single share within market open


class TradeType(StrEnum):
    CASH = "0"              # 現股
    MARGIN = "3"            # 融資
    SHORT = "4"             # 融券
    DAY_TRADE_SELL = "A"    # 現股當沖賣


class TradeOption(StrEnum):
    LIMIT = "0"             # limit price
    FLAT = "1"
    LIMIT_DOWN = "2"        # 跌停
    LIMIT_UP = "3"          # 漲停
    MARKET = "4"


class OrderCondition(StrEnum):
    FILL_OR_KILL = "F"
    IMMEDIATE_OR_CANCEL = "I"
    REST_OF_DAY = "R"


def setup_keyring(user_account) -> None:
    """
    Setup keyring for user account.

    @param user_account:
    @return: [None]
    """
    backend = os.getenv('PYTHON_KEYRING_BACKEND')
    if backend == 'keyrings.cryptfile.cryptfile.CryptFileKeyring':
        key_ring = CryptFileKeyring()
        key_ring.keyring_key = os.getenv("KEYRING_CRYPTFILE_PASSWORD") or hash_value(user_account)
        set_keyring(key_ring)


def hash_value(value: str) -> str:
    """
    Hash a string value using md5 hash algorithm.

    @param value: [str] The string to be hashed.
    @return: [str] The hash value.
    """
    return md5(value.encode('utf-8')).hexdigest()


def _get_password(key, user_account) -> str:
    return get_password(f'fugle_trade_sdk:{key}', user_account)


def _check_password(user_account, user_password: str, cert_password: str,
                    service_name: str = "fugle_trade_sdk") -> None:
    """

    @param user_account: The user account
    @param user_password: [str] The user password
    @param cert_password: [str] The certificate password
    @param service_name: [str] The service name, defaults to "fugle_trade_sdk"
    @return: [None]
    """
    if not get_password(service_name, user_account):
        set_password(f"{service_name}:account", user_account, user_password)

    if not get_password(service_name, user_account):
        set_password(f"{service_name}:cert", user_account, cert_password)


def _set_password(user_account, user_password: str, cert_password: str,
                  service_name: str = "fugle_trade_sdk") -> None:
    """

    @param user_account: The user account
    @param user_password: [str] The user password
    @param cert_password: [str] The certificate password
    @param service_name: [str] The service name, defaults to "fugle_trade_sdk"
    @return: [None]
    """
    set_password(f"{service_name}:account", user_account, user_password)
    set_password(f"{service_name}:cert", user_account, cert_password)


class Order:

    ap_code: APCode
    order_condition: OrderCondition
    trade_option: TradeOption
    trade_type: TradeType
    action: ActionType
    price: float
    stock_symbol: str
    quantity: int

    def __init__(self, action: ActionType, price: float, stock_symbol: str, quantity: int,
                 ap_code: APCode = APCode.COMMON, order_condition: OrderCondition = OrderCondition.REST_OF_DAY,
                 trade_option: TradeOption = TradeOption.LIMIT, trade_type: TradeType = TradeType.CASH):

        self.ap_code = ap_code
        self.order_condition = order_condition
        self.trade_option = trade_option
        self.trade_type = trade_type
        self.action = action
        self.price = price
        self.stock_symbol = stock_symbol
        self.quantity = quantity

    def __str__(self):
        return f"Order({self.action}, {self.price}, {self}"

