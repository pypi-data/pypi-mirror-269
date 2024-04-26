# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     validators.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from utils import logger
from decimal import Decimal
from capp_ui.fee import flight_fee

__all__ = ["FlightTicketValidator"]


class FlightTicketValidator(object):
    """机票校验器"""

    @classmethod
    def validator_payment_with_deduction(cls, pre_sale_amount: Decimal, actual_amount: Decimal,
                                         deduction_amount: Decimal) -> bool:
        """支付校验, 抵扣场景，默认积分抵扣场景，可以抵扣10.00元"""
        if deduction_amount >= 10.00:
            expected_amount = pre_sale_amount + flight_fee.get("fuel_fee") + flight_fee.get(
                "airport_fee") - deduction_amount
            if expected_amount >= actual_amount:
                logger.info("订单的实际支付金额<{}>小于或等于预期的支付金额<{}>，可以正常交易.".format(
                    actual_amount, expected_amount)
                )
                return True
            else:
                logger.error(
                    "订单的实际支付金额<{}>大于预期的支付金额<{}>，交易需要取消.".format(actual_amount, expected_amount))
                return False
        else:
            if deduction_amount > 0:
                logger.warning("抵扣金额<{}>不足10.00元.".format(deduction_amount))
            else:
                logger.error("获取到的抵扣金额<{}>有异常.".format(deduction_amount))
            return False

    @classmethod
    def validator_payment_with_wallet(cls, pre_sale_amount: Decimal, actual_amount: Decimal) -> bool:
        """支付校验, 钱包场景"""
        expected_amount = pre_sale_amount + flight_fee.get("fuel_fee") + flight_fee.get("airport_fee")
        if actual_amount >= expected_amount:
            logger.info("钱包的余额<{}>大于或等于预期的支付金额<{}>，可以正常交易.".format(
                actual_amount, expected_amount)
            )
            return True
        else:
            logger.warning(
                "钱包的余额<{}>小于预期的支付金额<{}>，需要切换至银行卡支付.".format(actual_amount, expected_amount))
            return False
