from src.model.sale_transaction import BuyTransaction, SaleTransaction
from src.model.transactions import Transactions


class TransactionsMatcher:

    def __init__(self, transactions: Transactions):
        self.buy_transactions = [BuyTransaction(t) for t in transactions.get_bought()]
        self.sale_transactions = [SaleTransaction(t) for t in transactions.get_sold()]
        self.__match_transactions()

    def __match_transactions(self):
        for sale_transaction in self.sale_transactions:
            for buy_transaction in self.buy_transactions:
                if buy_transaction.title != sale_transaction.title:
                    raise Exception(f"Trying to match transactions with different title: {buy_transaction.title} and {sale_transaction.title}")
                sale_transaction.add_matching_buy_transaction(buy_transaction)

    def to_matched_transactions(self):
        concat = self.buy_transactions + self.sale_transactions
        return MatchedTransactions(sorted(concat, key = lambda x: x.date))


class MatchedTransactions(Transactions):

    pass


