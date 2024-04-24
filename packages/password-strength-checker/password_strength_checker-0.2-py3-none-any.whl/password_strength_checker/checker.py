import re

class PasswordChecker:
    def __init__(self, min_length=8, require_upper=True, require_lower=True, require_digit=True, require_special=True):
        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digit = require_digit
        self.require_special = require_special

    def is_strong_password(self, password):
        # Check minimum length
        if len(password) < self.min_length:
            return False

        # Check for uppercase letters
        if self.require_upper and not re.search(r'[A-Z]', password):
            return False

        # Check for lowercase letters
        if self.require_lower and not re.search(r'[a-z]', password):
            return False

        # Check for digits
        if self.require_digit and not re.search(r'[0-9]', password):
            return False

        # Check for special characters
        if self.require_special and not re.search(r'[\W_]', password):
            return False

        return True
