from typing import List

from src.model.parsed_file import ParsedFile
from src.model.transactions import Transactions, MonthTransactions
from src.model.transactions_matcher import TransactionsMatcher
from src.aggregator import grouper
import shutil
import os

from src.aggregator.grouper import group_transactions_by_month


class GroupedByMonthWriter:

    ROOT_DIR = 'output_data/by_month'
    SHOULD_PAY_IR_DIR = 'output_data/by_month/should_pay_ir'
    HAS_PROFIT_DIR = 'output_data/by_month/has_profit'
    HAS_LOSS_DIR = 'output_data/by_month/has_loss'

    @classmethod
    def write(cls, parsed_files: List[ParsedFile]):
        shutil.rmtree(cls.ROOT_DIR)
        os.makedirs(cls.ROOT_DIR)
        os.makedirs(cls.SHOULD_PAY_IR_DIR)
        os.makedirs(cls.HAS_PROFIT_DIR)
        os.makedirs(cls.HAS_LOSS_DIR)
        grouped_by_title = grouper.group_operations_by_title(parsed_files)
        all_transactions = []
        for title, transactions in grouped_by_title.items():
            transactions = TransactionsMatcher(transactions).to_matched_transactions()
            all_transactions.extend(transactions)
        transactions_by_month = group_transactions_by_month(all_transactions)
        for transactions in transactions_by_month:
            cls.__write(transactions.get_year_month_as_string(), transactions)

    @classmethod
    def __write(cls, title, transactions: MonthTransactions):
        text = ''
        for transaction in transactions:
            text += transaction.get_formatted()
        text += '\n\n\n\n\n\n'
        transactions_summary = transactions.get_summary()
        text += transactions_summary.get_formatted()

        def write_to_file(file, text):
            with open(file, 'w') as f:
                f.write(text)

        write_to_file(f'{cls.ROOT_DIR}/{title}.csv', text)

        if transactions.should_pay_ir():
            write_to_file(f'{cls.SHOULD_PAY_IR_DIR}/{title}.csv', text)
        if transactions.has_profit():
            write_to_file(f'{cls.HAS_PROFIT_DIR}/{title}.csv', text)
        if transactions.has_loss():
            write_to_file(f'{cls.HAS_LOSS_DIR}/{title}.csv', text)
