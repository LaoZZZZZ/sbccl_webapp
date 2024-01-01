#!/usr/bin/env python3
import unittest

import request_validator

class TestRequestValidatorMethods(unittest.TestCase):
    def test_phone_number_validation(self):
        self.assertTrue(request_validator.ValidatePhoneNumber("6626094787"))
        self.assertFalse(request_validator.ValidatePhoneNumber("2123"))
        self.assertTrue(request_validator.ValidatePhoneNumber("+1 662-609-4787"))
        self.assertTrue(request_validator.ValidatePhoneNumber("662-609-4787"))
        self.assertFalse(request_validator.ValidatePhoneNumber(""))


if __name__ == '__main__':
    unittest.main()