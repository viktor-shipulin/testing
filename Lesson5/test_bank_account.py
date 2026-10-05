import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Иван", "001")
        self.other = BankAccount("Мария", "002")

    def tearDown(self):
        del self.acc
        del self.other

    def test_create_account(self):
        self.assertEqual(self.acc.owner, "Иван")
        self.assertEqual(self.acc.number, "001")
        self.assertEqual(self.acc.balance, 0)

    def test_new_account_is_empty(self):
        self.assertTrue(self.acc.is_empty())

    def test_deposit_success(self):
        self.acc.deposit(500)
        self.assertEqual(self.acc.get_balance(), 500)

    def test_deposit_multiple(self):
        self.acc.deposit(100)
        self.acc.deposit(200)
        self.assertEqual(self.acc.get_balance(), 300)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(-100)

    def test_deposit_zero(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(0)

    def test_deposit_not_a_number(self):
        with self.assertRaises(ValueError):
            self.acc.deposit("100")

    def test_withdraw_success(self):
        self.acc.deposit(500)
        self.acc.withdraw(200)
        self.assertEqual(self.acc.get_balance(), 300)

    def test_withdraw_all(self):
        self.acc.deposit(500)
        self.acc.withdraw(500)
        self.assertTrue(self.acc.is_empty())

    def test_withdraw_more_than_balance(self):
        self.acc.deposit(100)
        with self.assertRaises(ValueError):
            self.acc.withdraw(200)

        self.assertEqual(self.acc.get_balance(), 100)

    def test_withdraw_negative(self):
        self.acc.deposit(100)
        with self.assertRaises(ValueError):
            self.acc.withdraw(-50)

    def test_transfer_success(self):
        self.acc.deposit(500)
        self.acc.transfer(self.other, 200)
        self.assertEqual(self.acc.get_balance(), 300)
        self.assertEqual(self.other.get_balance(), 200)

    def test_transfer_amount_is_equal(self):
        self.acc.deposit(500)
        before_sender = self.acc.get_balance()
        before_receiver = self.other.get_balance()
        self.acc.transfer(self.other, 150)
        self.assertEqual(before_sender - self.acc.get_balance(), 150)
        self.assertEqual(self.other.get_balance() - before_receiver, 150)

    def test_transfer_insufficient_funds(self):
        self.acc.deposit(100)
        with self.assertRaises(ValueError):
            self.acc.transfer(self.other, 200)
        self.assertEqual(self.acc.get_balance(), 100)
        self.assertEqual(self.other.get_balance(), 0)

    def test_transfer_negative(self):
        self.acc.deposit(100)
        with self.assertRaises(ValueError):
            self.acc.transfer(self.other, -50)
        self.assertEqual(self.acc.get_balance(), 100)
        self.assertEqual(self.other.get_balance(), 0)

    def test_get_balance_after_operations(self):
        self.acc.deposit(1000)
        self.acc.withdraw(300)
        self.acc.deposit(50)
        self.assertEqual(self.acc.get_balance(), 750)

    def test_is_empty_after_deposit(self):
        self.acc.deposit(10)
        self.assertFalse(self.acc.is_empty())

    def test_is_empty_after_withdraw_all(self):
        self.acc.deposit(300)
        self.acc.withdraw(300)
        self.assertTrue(self.acc.is_empty())


if __name__ == '__main__':
    unittest.main()
