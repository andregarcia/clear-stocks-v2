

class TransactionsSummary:

    def __init__(self, quantity_bought, quantity_sold, value_bought, value_sold):
        self.quantity_bought = quantity_bought
        self.quantity_sold = quantity_sold
        self.value_bought = value_bought
        self.value_sold = value_sold
        self.quantity_left = quantity_bought - quantity_sold
        self.profit = value_sold - value_bought

    def get_formatted(self):
        s = 'QUANTITY_BOUGHT;QUANTITY_SOLD;QUANTITY_LEFT\n'
        s += f'{self.quantity_bought};{self.quantity_sold};{self.quantity_left}\n'
        s += '\n\n\n\n'
        s += 'VALUE_BOUGHT;VALUE_SOLD;PROFIT\n'
        s += f'{self.value_bought};{self.value_sold};{self.profit}\n'
        return s


class MonthTransactionsSummary:

    def __init__(self, quantity_bought, quantity_sold, value_bought, value_sold, buying_value_of_sold_stocks,
                 buying_quantity_of_sold_stocks, profit):
        self.quantity_bought = quantity_bought
        self.quantity_sold = quantity_sold
        self.value_bought = value_bought
        self.value_sold = value_sold
        self.buying_value_of_sold_stocks = buying_value_of_sold_stocks
        self.buying_quantity_of_sold_stocks = buying_quantity_of_sold_stocks
        self.profit = profit

    def get_formatted(self):
        s = 'MONTH_QUANTITY_BOUGHT;BUYING_QUANTITY_OF_SOLD_STOCKS;QUANTITY_SOLD\n'
        s += f'{self.quantity_bought};{self.buying_quantity_of_sold_stocks};{self.quantity_sold}\n'
        s += '\n\n\n\n'
        s += 'VALUE_BOUGHT;BUYING_VALUE_OF_SOLD_STOCKS;VALUE_SOLD;PROFIT\n'
        s += f'{self.value_bought:+.2f};{self.buying_value_of_sold_stocks:+.2f};{self.value_sold:+.2f};{self.profit:+.2f}\n'
        return s

