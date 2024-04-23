"""Main module."""
import json
from .common import Order
from .common import APCode
from .common import TradeOption
from .common import _get_password
from .common import _set_password
from .common import _check_password
from .common import setup_keyring
from fugle_trade_core.fugle_trade_core import CoreSDK


class FugleTrader:

    def __init__(self, config):
        self._ip: str = str()
        self._account_id = config['User']['Account']
        self._account_password = config['User']['Password']
        self._cert_password = config['User']['CertPassword']

        if not self._account_id:
            raise TypeError("please setup your config before using this SDK")

        setup_keyring(self._account_id)
        _check_password(self._account_id, self._account_password, self._cert_password)

        self._core = CoreSDK(
            config['Core']['Entry'],
            config['User']['Account'],
            config['Cert']['Path'],
            _get_password('cert', self._account_id),
            config['Api']['Key'],
            config['Api']['Secret']
        )

    def cert_info(self) -> dict:
        """
        Get certificate info
        @return: [dict]
        """
        return json.loads(self._core.get_certinfo())

    def reset_password(self) -> None:
        """
        Reset password
        @return: [None]
        """
        _set_password(self._account_id, self._account_password, self._cert_password)
        return

    def place_order(self, order: Order) -> dict:
        """

        @param order: [Order]
        @return: [dict]
        """
        return json.loads(self._core.order(order))['data']

    def cancel_order(self, in_order_result, **kwargs) -> json:
        """
        Cancel an open order
        @param in_order_result:
        @param kwargs:
        @return:
        """
        order_result = self.recover_order_result(in_order_result)
        ap_code = str(order_result["ap_code"])
        unit = self._core.get_volume_per_unit(order_result["stock_no"])
        executed_cel_qty = None

        if "cel_qty" in kwargs and "cel_qty_share" in kwargs:
            raise TypeError("cel_qty or cel_qty_share, not both")

        # if no args, treat it as cancel all
        if "cel_qty" not in kwargs and "cel_qty_share" not in kwargs:
            return json.loads(self._core.modify_volume(order_result, 0))["data"]

        if "cel_qty" in kwargs:
            if ap_code in (APCode.ODD, APCode.EMERGING_MARKET, APCode.INTRA_DAY):
                executed_cel_qty = kwargs["cel_qty"] * unit
            else:
                executed_cel_qty = kwargs["cel_qty"]

        if "cel_qty_share" in kwargs:
            if ap_code in (APCode.ODD, APCode.EMERGING_MARKET, APCode.INTRA_DAY):
                executed_cel_qty = kwargs["cel_qty_share"]
            else:
                if kwargs["cel_qty_share"] % unit != 0:
                    raise TypeError("must be multiples of " + str(unit))
                executed_cel_qty = int(kwargs["cel_qty_share"] / unit)

        if not executed_cel_qty:
            raise TypeError("must provide cel_qty or cel_qty_share")

        return json.loads(self._core.modify_volume(order_result, executed_cel_qty))["data"]

    def login(self):
        """
        Login to the Fugle API
        @return: [None]
        """
        self._core.login(
            self._account_id, _get_password('account', self._account_id)
        )

    def modify_price(self, in_order_result: json, target_price: float = None,
                     trade_option: TradeOption = TradeOption.LIMIT):
        """
        Modify the price of the order
        @param in_order_result: [json]
        @param target_price: [float]
        @param trade_option: [TradeOption]
        @return:
        """
        if target_price is None and trade_option is None:
            raise TypeError("must provide valid arguments")

        if trade_option is not None:
            if type(trade_option) is not trade_option:
                raise TypeError("Please use fugleTrade.constant PriceFlag")
            trade_option = trade_option.value

        order_result = self.recover_order_result(in_order_result)
        return json.loads(self._core.modify_price(order_result, target_price, trade_option))['data']

    def get_order_results(self):
        """get order result data 取得當日委託明細"""
        order_res = self._core.get_order_results()
        return json.loads(order_res)["data"]["order_results"]

    def get_order_results_by_date(self, start, end):
        """get order result data by date 用日期當作篩選條件委託明細"""
        order_res_history = self._core.get_order_result_history("0", start, end)
        return json.loads(order_res_history)["data"]["order_result_history"]

    def get_transactions(self, query_range):
        """get transactions data 成交明細"""
        transactions_res = self._core.get_transactions(query_range)
        return json.loads(transactions_res)["data"]["mat_sums"]

    def get_transactions_by_date(self, start, end):
        """用日期當作篩選條件 get transactions data by date 成交明細"""
        transactions_res = self._core.get_transactions_by_date(start, end)
        return json.loads(transactions_res)["data"]["mat_sums"]

    def get_inventories(self) -> json:
        """
        Get all inventories associated with this account

        @return: [json]
        """
        inventories_res = self._core.get_inventories()
        return json.loads(inventories_res)["data"]["stk_sums"]

    def get_balance(self) -> json:
        """
        Get current balance of the account

        @return: [json]
        """
        inventories_res = self._core.get_balance()
        return json.loads(inventories_res)["data"]

    def get_trade_status(self) -> json:
        """
        Gets trade status
        @return: [json]
        """
        inventories_res = self._core.get_trade_status()
        return json.loads(inventories_res)["data"]

    def get_market_status(self) -> json:
        """
        Gets market status
        @return: [json]
        """
        inventories_res = self._core.get_market_status()
        return json.loads(inventories_res)["data"]

    def get_settlements(self) -> json:
        """
        Gets settlements
        @return: [json]
        """
        settlements_res = self._core.get_settlements()
        return json.loads(settlements_res)["data"]["settlements"]

    def get_key_info(self) -> json:
        """
        Gets key information
        @return: [json]
        """
        key_info_res = self._core.get_key_info()
        return json.loads(key_info_res)["data"]

    def recover_order_result(self, order_result) -> dict:
        """
        @param order_result:
        @return:
        """
        ap_code = order_result["ap_code"]
        stock_no = order_result["stock_no"]
        unit = self._core.get_volume_per_unit(stock_no)
        new_dict = {}
        for key, value in order_result.items():
            if key.endswith("qty"):
                if ap_code in (APCode.ODD, APCode.EMERGING_MARKET, APCode.INTRA_DAY):
                    new_dict[key] = int(value * unit)
                else:
                    new_dict[key] = int(value)
        return {**order_result, **new_dict}
