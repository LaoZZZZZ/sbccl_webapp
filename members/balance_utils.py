from members.models import Payment, Registration, Dropout

class BalanceUtils(object):
    def CalculateBalance(registration : Registration, payment : Payment):
        return payment.original_amount - payment.amount_in_dollar

    # TODO: Add refund logic before the school start (Sep 07, 2024)
    def CalculateRefund(dropout : Dropout, payment : Payment):
        return -payment.amount_in_dollar
