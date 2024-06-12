import unittest
from members.models import Coupon, CouponUsageRecord, User, Registration, Member
import datetime
from members.coupon_utils import CouponUtils

class CouponUtilsTest(unittest.TestCase):
    def test_validation(self):
        coupon = Coupon(type='A', dollar_amount=50, code='early_bird')
        coupon.expiration_date = datetime.date.today()
        self.assertTrue(CouponUtils.IsValid(coupon))

        coupon.expiration_date = datetime.date.today() - datetime.timedelta(days=1)
        self.assertFalse(CouponUtils.IsValid(coupon))

    def test_applyCoupons(self):
        coupon = Coupon(type='A', dollar_amount=50, code='early_bird')
        coupon.expiration_date = datetime.date.today()

        # Both percentage and expired coupon are skipped for the calculation.
        percentage_coupon = Coupon(type='P', percentage=50, code='early_bird')
        percentage_coupon.expiration_date = datetime.date.today()

        expired_coupon = Coupon(type='A', dollar_amount=50, code='early_bird')
        expired_coupon.expiration_date = datetime.date.today() - datetime.timedelta(days=1)

        original_amount = 100
        self.assertEqual(CouponUtils.applyCoupons(original_amount, [coupon, expired_coupon, percentage_coupon]),
                        100 - 50)
        
        # make sure negative balance is not generated.
        original_amount = 0
        self.assertEqual(CouponUtils.applyCoupons(original_amount, [coupon, expired_coupon, percentage_coupon]),
                         0)
        
    def test_canBeUsed(self):
        coupon = Coupon(type='A', dollar_amount=50, code='early_bird', application_rule='PA')
        coupon.expiration_date = datetime.date.today()

        self.assertTrue(CouponUtils.canBeUsed(coupon, []))
        user = User(username='test')
        member = Member(user_id=user)
        registration = Registration()

        usage = CouponUsageRecord(user=member, registration=registration, coupon=coupon)
        self.assertFalse(CouponUtils.canBeUsed(coupon, [usage]))

        pr_coupon = Coupon(type='A', dollar_amount=50, code='early_bird', application_rule='PR')
        pr_coupon.expiration_date = datetime.date.today()
        self.assertTrue(CouponUtils.canBeUsed(pr_coupon, [usage]))


if __name__ == '__main__':
    unittest.main()