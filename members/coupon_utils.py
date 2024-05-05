
from members.models import Coupon, CouponUsageRecord
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
    
    def canBeUsed(coupon : Coupon, usage_history: list[CouponUsageRecord]):
        """
         Checks if this coupon can be used for this user.
        """
        for usage in usage_history:
            if usage.coupon.code == coupon.code:
                # Per registration
                if coupon.application_rule == 'PR':
                    return True
                # Per account
                elif coupon.application_rule == 'PA':
                    return False
                else:
                    print("Invalid application rule found: ", coupon.application_rule)
                    return False

        return True