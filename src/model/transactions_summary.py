

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

    def __init__(self, month_transactions):
        self.__calculate_summary(month_transactions)

    def __calculate_summary(self, month_transactions):
        self.value_sold = sum([x.transaction_value for x in month_transactions.get_sold()])
        self.value_bought = sum([x.transaction_value for x in month_transactions.get_bought()])
        self.quantity_bought = sum([x.quantity for x in month_transactions.get_bought()])
        self.quantity_sold = sum([x.quantity for x in month_transactions.get_sold()])
        self.buying_value_of_sold_stocks = sum([x.get_total_buying_price() for x in month_transactions.get_sale_transactions()])
        self.buying_quantity_of_sold_stocks = sum([x.get_total_buying_quantity() for x in month_transactions.get_sale_transactions()])
        self.profit = sum([x.get_profit() for x in month_transactions.get_sale_transactions()])
        self.accumulated_loss = self.__calculate_accumulated_loss(month_transactions)
        self.ir_before_accumulated_loss_discount, self.ir = self.__calculate_ir_and_update_accumulated_loss()

    def get_formatted(self):
        s = 'MONTH_QUANTITY_BOUGHT;BUYING_QUANTITY_OF_SOLD_STOCKS;QUANTITY_SOLD\n'
        s += f'{self.quantity_bought};{self.buying_quantity_of_sold_stocks};{self.quantity_sold}\n'
        s += '\n\n'
        s += 'VALUE_BOUGHT;BUYING_VALUE_OF_SOLD_STOCKS;VALUE_SOLD;PROFIT\n'
        s += f'{self.value_bought:+.2f};{self.buying_value_of_sold_stocks:+.2f};{self.value_sold:+.2f};{self.profit:+.2f}\n'
        s += '\n\n'
        s += 'ACCUMULATED_LOSS\n'
        s += f'{self.accumulated_loss}'
        s += '\n\n'
        s += 'IR_BEFORE_ACCUMULATED_LOSS_DISCOUNT;IR\n'
        s += f'{self.ir_before_accumulated_loss_discount};{self.ir}'
        return s

    def __calculate_accumulated_loss(self, month_transactions):
        accumulated_loss = 0
        if self.profit < 0:
            accumulated_loss += self.profit
        previous_accumulated_loss = month_transactions.latest_month_transactions.get_summary().accumulated_loss \
            if month_transactions.latest_month_transactions is not None else 0
        if previous_accumulated_loss < 0:
            accumulated_loss += previous_accumulated_loss
        assert accumulated_loss <= 0
        return accumulated_loss

    def __calculate_ir_and_update_accumulated_loss(self):
        if self.profit > 0 and self.value_sold >= 20000:
            ir_before_accumulated_loss_discount = self.profit * 0.15
            if self.accumulated_loss < 0:
                ir = max(0, ir_before_accumulated_loss_discount + self.accumulated_loss)
                self.accumulated_loss = min(0, self.accumulated_loss + ir_before_accumulated_loss_discount)
            else:
                ir = ir_before_accumulated_loss_discount
            return ir_before_accumulated_loss_discount, ir
        return 0, 0
