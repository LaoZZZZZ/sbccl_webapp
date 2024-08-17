
from members.models import Coupon, CouponUsageRecord, Registration
import datetime

class CouponUtils(object):

    def __coupon_used_in_registration__(coupon_code, matched_registration: Registration):
        """
            Checks if the coupon code is already used by the registration.
        """
        for c in matched_registration.coupons.all():
            if c.code == coupon_code:
                return True
            
        return False
    

    def IsValid(coupon : Coupon):
        return coupon.expiration_date >= datetime.date.today()

    def applyCoupons(original_amount : float, coupons : list[(Coupon, datetime.date)]):
        """
          calculate the actual amount based on the coupons.
          Amount type of coupon will be applied first. 
        """
        amount : float = original_amount
        for (c, used_date) in coupons:
            if c.expiration_date < used_date:
                continue
            if c.type == 'A':
                amount -= c.dollar_amount
                if amount <= 0:
                    break
            else:
                print('Percentage type of coupon is not supported yet')
        return max(amount, 0)
    
    def canBeUsed(coupon : Coupon, usage_history: list[CouponUsageRecord], matched_registration: Registration=None):
        """
         Checks if this coupon can be used for this user.
        """
        for usage in usage_history:
            if usage.coupon.code == coupon.code:
                # Per registration
                if coupon.application_rule == 'PR':
                    return not matched_registration or not CouponUtils.__coupon_used_in_registration__(coupon.code, matched_registration)
                # Per account
                elif coupon.application_rule == 'PA':
                    return False
                else:
                    print("Invalid application rule found: ", coupon.application_rule)
                    return False

        return True