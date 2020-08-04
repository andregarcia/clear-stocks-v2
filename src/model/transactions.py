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

    def get_sale_transactions(self) -> List[SaleTransaction]:
        return [x for x in self if type(x) == SaleTransaction]

    def get_summary(self) -> MonthTransactionsSummary:
        value_sold = sum([x.transaction_value for x in self.get_sold()])
        value_bought = sum([x.transaction_value for x in self.get_bought()])
        quantity_bought = sum([x.quantity for x in self.get_bought()])
        quantity_sold = sum([x.quantity for x in self.get_sold()])
        buying_value_of_sold_stocks = sum([x.get_total_buying_price() for x in self.get_sale_transactions()])
        buying_quantity_of_sold_stocks = sum([x.get_total_buying_quantity() for x in self.get_sale_transactions()])
        profit = sum([x.get_profit() for x in self.get_sale_transactions()])
        return MonthTransactionsSummary(quantity_bought, quantity_sold, value_bought, value_sold,
                                        buying_value_of_sold_stocks, buying_quantity_of_sold_stocks, profit)
