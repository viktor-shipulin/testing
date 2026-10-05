class BankAccount:
    def __init__(self, owner, number):
        self.owner = owner        
        self.number = number        
        self.balance = 0            

    def _validate_amount(self, amount):
        """Проверка суммы: должна быть положительным числом."""
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    def deposit(self, amount):
        """Пополнение счёта."""
        self._validate_amount(amount)
        self.balance += amount

    def withdraw(self, amount):
        """Снятие средств со счёта."""
        self._validate_amount(amount)
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount

    def transfer(self, target, amount):
        """Перевод средств на другой счёт.
        Проверки идут до изменения балансов — при ошибке оба счёта не меняются."""
        self._validate_amount(amount)
        if amount > self.balance:
            raise ValueError("Недостаточно средств для перевода")
        self.balance -= amount
        target.balance += amount

    def get_balance(self):
        """Текущий баланс счёта."""
        return self.balance

    def is_empty(self):
        """Счёт пуст, если баланс равен нулю."""
        return self.balance == 0
