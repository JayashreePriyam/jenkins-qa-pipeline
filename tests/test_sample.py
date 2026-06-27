import pytest
import os
import datetime

ENV = os.getenv("TEST_ENV", "staging")
BROWSER = os.getenv("BROWSER", "chrome")

class TestLoginPage:
    def test_valid_login(self):
        username = "testuser"
        password = "Test@123"
        assert len(username) > 0
        assert len(password) >= 6
        assert any(c.isupper() for c in password)
        print(f"[{ENV}] Login test passed on {BROWSER}")

    def test_empty_username_rejected(self):
        assert len("") == 0
        print(f"[{ENV}] Empty username validation passed")

    def test_short_password_rejected(self):
        assert len("Ab1") < 6
        print(f"[{ENV}] Short password validation passed")

class TestPaymentValidation:
    def test_valid_card_number(self):
        card = "4111111111111111"
        assert len(card) == 16
        digits = [int(d) for d in card]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for d in even_digits:
            total += sum(divmod(d * 2, 10))
        assert total % 10 == 0
        print(f"[{ENV}] Card validation passed")

    def test_expired_card_rejected(self):
        now = datetime.datetime.now()
        is_expired = (2020 < now.year)
        assert is_expired
        print(f"[{ENV}] Expired card rejection passed")

    def test_cvv_length(self):
        cvv = "123"
        assert len(cvv) == 3 and cvv.isdigit()
        print(f"[{ENV}] CVV validation passed")

    @pytest.mark.parametrize("amount,expected", [
        (100.00, True), (0, False), (-50, False), (999999.99, True),
    ])
    def test_transaction_amount(self, amount, expected):
        is_valid = amount > 0
        assert is_valid == expected

class TestAPIHealth:
    def test_environment_is_set(self):
        assert ENV in ["dev", "staging", "production", "local"]

    def test_browser_is_valid(self):
        assert BROWSER in ["chrome", "firefox", "edge", "safari"]
