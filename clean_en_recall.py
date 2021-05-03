import csv
from libs.constants import *
from libs.csv_utils import write_spreadsheet_file
from libs.translation_util import clean
from libs.wer import clean_extra_words

IN_FILE_NAME = 'data/filtered_raw_data.csv'

csv_data = None
with open(IN_FILE_NAME, 'r', encoding="utf-8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	csv_data = list(csv_reader)

recalls = []
for row_index in range(0, len(csv_data) - FIRST_DATA_ROW):
	row = csv_data[row_index + FIRST_DATA_ROW]
	for index in range(0, RECALL_COUNT):
		column_index = FIRST_EN_RECALL_COLUMN + index * RECALL_INTERVAL
		reference = column_index_to_en_recall_reference[column_index]
		hypothesis = row[column_index]
		recalls.append([ clean(reference) ])
		recalls.append([ clean(hypothesis) ])
		recalls.append([ clean_extra_words(reference, hypothesis) ])

write_spreadsheet_file('output/en_recall_sentences.txt', recalls)