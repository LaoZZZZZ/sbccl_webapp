
from members.models import Coupon
import datetime

class CouponUtils(object):
    def IsValid(coupon : Coupon):
        return coupon.expiration_date >= datetime.date.today()

    def applyCoupons(original_amount : float, coupons : list[Coupon]):
        """
          calculate the actual amount based on the coupons.
          Amount type of coupon will be applied first. 
        """
        amount : float = original_amount
        for c in coupons:
            if not CouponUtils.IsValid(c):
                continue
            if c.type == 'A':
                amount -= c.dollar_amount
            else:
                print('Percentage type of coupon is not supported yet')
        return amount
