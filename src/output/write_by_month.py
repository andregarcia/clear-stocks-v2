from typing import List

from src.model.parsed_file import ParsedFile
from src.model.transactions import Transactions
from src.model.transactions_matcher import TransactionsMatcher
from src.aggregator import grouper
import shutil
import os

from src.aggregator.grouper import group_transactions_by_month


class GroupedByMonthWriter:

    ROOT_DIR = 'output_data/by_month'

    @classmethod
    def write(cls, parsed_files: List[ParsedFile]):
        shutil.rmtree(cls.ROOT_DIR)
        os.makedirs(cls.ROOT_DIR)
        grouped_by_title = grouper.group_operations_by_title(parsed_files)
        all_transactions = []
        for title, transactions in grouped_by_title.items():
            transactions = TransactionsMatcher(transactions).to_matched_transactions()
            all_transactions.extend(transactions)
        grouped_by_month = group_transactions_by_month(all_transactions)
        for month, transactions in grouped_by_month.items():
            cls.__write(month, transactions)

    @classmethod
    def __write(cls, title, transactions: Transactions):
        text = ''
        for transaction in transactions:
            text += transaction.get_formatted()
        text += '\n\n\n\n\n\n'
        transactions_summary = transactions.get_summary()
        text += transactions_summary.get_formatted()

        with open(f'{cls.ROOT_DIR}/{title}.csv', 'w') as f:
            f.write(text)

