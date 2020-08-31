
from src.parser.notes_parser import parse_all_files
from src.output.write_by_month import GroupedByMonthWriter
from src.output.write_by_title import GroupedByTitleWriter
import sys

path = sys.argv[1]
parsed_files = parse_all_files(path)
GroupedByTitleWriter.write(parsed_files)
GroupedByMonthWriter.write(parsed_files)


