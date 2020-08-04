from src.model.transaction import Transaction


class MatchingTransaction:

    def __init__(self, transaction, match_quantity):
        self.transaction = transaction
        self.match_quantity = match_quantity


class MatchingTransactions(list):

    def get_mean_price(self):
        prices_quantities = []
        for matching_transaction in self:   # type: MatchingTransaction
            prices_quantities.append((matching_transaction.match_quantity, matching_transaction.transaction.price))
        return sum([x[0]*x[1] for x in prices_quantities])/sum([x[0] for x in prices_quantities])

    def get_total_price(self):
        prices_quantities = []
        for matching_transaction in self:   # type: MatchingTransaction
            prices_quantities.append((matching_transaction.match_quantity, matching_transaction.transaction.price))
        return sum([x[0]*x[1] for x in prices_quantities])

    def get_quantity(self):
        return sum([x.match_quantity for x in self])


class BuyTransaction(Transaction):

    def __init__(self, transaction: Transaction):
        super(BuyTransaction, self).__init__(**transaction.__dict__)
        if not self.is_buy():
            raise Exception("Expected buy transaction")

        self.__missing_match_quantity = self.quantity

    @property
    def missing_match_quantity(self):
        return self.__missing_match_quantity

    def decrement_missing_match_quantity(self, value):
        if value <= 0:
            raise Exception("Error trying to decrement using a negative value")
        elif value > self.__missing_match_quantity:
            raise Exception("Error trying to decrement a value larger than stored")
        self.__missing_match_quantity -= value


class SaleTransaction(Transaction):

    def __init__(self, transaction: Transaction):
        super(SaleTransaction, self).__init__(**transaction.__dict__)
        if not self.is_sale():
            raise Exception("Expected sale transaction")
        self.matching_buy_transactions = MatchingTransactions()
        self.missing_match_quantity = self.quantity

    def add_matching_buy_transaction(self, buy_transaction: BuyTransaction):
        if self.missing_match_quantity < 0:
            raise Exception("Missing match quantity is lower than zero, something went wrong")
        if self.missing_match_quantity == 0:
            return
        if buy_transaction.missing_match_quantity > 0:
            maximum_to_decrement = buy_transaction.missing_match_quantity
            decrement = self.missing_match_quantity if self.missing_match_quantity <= maximum_to_decrement else maximum_to_decrement
            self.matching_buy_transactions.append(MatchingTransaction(buy_transaction, decrement))
            buy_transaction.decrement_missing_match_quantity(decrement)
            self.missing_match_quantity -= decrement

    def get_mean_buying_price(self):
        return self.matching_buy_transactions.get_mean_price()

    def get_total_buying_price(self):
        return self.matching_buy_transactions.get_total_price()

    def get_total_buying_quantity(self):
        return self.matching_buy_transactions.get_quantity()

    def get_profit(self):
        return self.transaction_value - self.get_total_buying_price()

    def get_formatted(self):
        original_formatted = super(SaleTransaction, self).get_formatted().rstrip()
        matching_buy_ids_and_quantities = ','.join([f'{m.transaction.id}:{m.match_quantity}' for m in self.matching_buy_transactions])
        mean_buy_price = self.get_mean_buying_price()
        total_buy_price = self.get_total_buying_price()
        profit = self.get_profit()
        formatted = f'{original_formatted};{matching_buy_ids_and_quantities};{mean_buy_price};{total_buy_price:+.2f};{profit:+.2f};{self.missing_match_quantity}\n'
        return formatted


