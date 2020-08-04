class Transaction:

    COUNTER = 0

    def __init__(self, dealer, type, market_type, deadline, title, note, quantity, price, transaction_value, flag, date, id=None):
        if id is None:
            Transaction.COUNTER += 1
            self.id = Transaction.COUNTER
        else:
            self.id = id
        self.dealer = dealer
        self.type = type
        self.market_type = market_type
        self.deadline = deadline
        self.title = title
        self.note = note
        self.quantity = int(quantity)
        self.price = self.__parse_float(price)
        self.transaction_value = self.__parse_float(transaction_value)
        self.flag = flag
        self.date = date

    def is_buy(self):
        return self.type == 'COMPRA'

    def is_sale(self):
        return self.type == 'VENDA'

    @staticmethod
    def __parse_float(f):
        if type(f) == str:
            return float(f.replace('.', '').replace(',', '.'))
        elif type(f) == float:
            return f
        else:
            raise Exception(f"Expected float value but found {type(f)}")

    def get_formatted(self):
        date = f'{self.date.day:02}/{self.date.month:02}/{self.date.year}'
        return f'{self.id};{self.title};{self.type};{date};{self.flag};{self.quantity};{self.price};{self.transaction_value}\n'


