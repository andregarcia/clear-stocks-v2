from typing import List

from src.model.sale_transaction import SaleTransaction
from src.model.transactions_summary import TransactionsSummary, MonthTransactionsSummary


class Transactions(list):

    def get_bought(self):
        return [x for x in self if x.type == 'COMPRA']

    def get_sold(self):
        return [x for x in self if x.type == 'VENDA']

    def get_summary(self) -> TransactionsSummary:
        value_bought = sum([x.transaction_value for x in self.get_bought()])
        quantity_bought = sum([x.quantity for x in self.get_bought()])
        value_sold = sum([x.transaction_value for x in self.get_sold()])
        quantity_sold = sum([x.quantity for x in self.get_sold()])
        return TransactionsSummary(quantity_bought, quantity_sold, value_bought, value_sold)


class MonthTransactions(Transactions):

    def __init__(self, year, month, l=None, latest_month_transactions=None):
        self.month = month
        self.year = year
        self.latest_month_transactions = latest_month_transactions
        self.summary = None
        super(MonthTransactions, self).__init__(l or [])

    def set_latest_month_transactions(self, latest_month_transactions):
        self.latest_month_transactions = latest_month_transactions

    def get_year_month_as_string(self):
        return f'{self.year}-{self.month}'

    def get_sale_transactions(self) -> List[SaleTransaction]:
        return [x for x in self if type(x) == SaleTransaction]

    def get_summary(self) -> MonthTransactionsSummary:
        if self.summary is None:
            self.summary = MonthTransactionsSummary(self)
        return self.summary

    def should_pay_ir(self):
        summary = self.get_summary()
        if summary.value_sold >= 20000 and summary.ir > 0:
            return True

    def has_profit(self):
        summary = self.get_summary()
        if summary.profit > 0:
            return True

    def has_loss(self):
        return not self.has_profit()
