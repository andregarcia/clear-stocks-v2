import os
import shutil
from typing import List

from src.model.parsed_file import ParsedFile
from src.model.transactions import Transactions
from src.model.transactions_matcher import TransactionsMatcher
from src.aggregator import grouper


class GroupedByTitleWriter:

    ROOT_DIR = 'output_data/by_title'
    IN_STOCK_DIR = f'{ROOT_DIR}/in_stock'

    @classmethod
    def write(cls, parsed_files: List[ParsedFile]):
        shutil.rmtree(cls.ROOT_DIR)
        os.makedirs(cls.IN_STOCK_DIR)
        grouped_by_title = grouper.group_operations_by_title(parsed_files)
        for title, transactions in grouped_by_title.items():
            transactions = TransactionsMatcher(transactions).to_matched_transactions()
            cls.__write(title, transactions)

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

        if transactions_summary.quantity_left > 0:
            with open(f'{cls.IN_STOCK_DIR}/{title}.csv', 'w') as f:
                f.write(text)

