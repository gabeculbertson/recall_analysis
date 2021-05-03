import csv
from libs.constants import *

DO_FILTER_EN_NONNATIVE = True
DO_FILTER_ES_NATIVE = False
IN_FILE_NAME = 'data/base_raw_data.csv'
OUT_FILE_NAME = 'data/filtered_raw_data.csv'
OUTLIERS = set([ '18631', '15883', '17653', '16330', '18550', '18598', '17749' ])

csv_data = None
with open(IN_FILE_NAME, 'r', encoding="utf-8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	csv_data = list(csv_reader)

participant_count = 0

with open(OUT_FILE_NAME, 'w', encoding="utf-8") as csv_file:
	csv_writer = csv.writer(csv_file)

	for row_index in range(0, FIRST_DATA_ROW):
		row = csv_data[row_index]
		csv_writer.writerow(row)

	for row_index in range(FIRST_DATA_ROW, len(csv_data)):
		row = csv_data[row_index]

		sona_id = row[SONA_ID_COLUMN]
		if sona_id == "" or row[SONA_ID_COLUMN - 1] == "":
			print('skipping: ', sona_id, ' reason: sona id was not included (not allowed to use data)')
			continue
		if row[LAST_MULTIPLE_CHOICE_COLUMN] == "":
			print('skipping: ', sona_id, ' reason: did not complete multiple choice (older survey version)')
			continue
		if sona_id in OUTLIERS:
			print('skipping: ', sona_id, ' reason: outlier, technical issue, or abnormally low scores')
			continue
		if DO_FILTER_EN_NONNATIVE and row[ENGLISH_NATIVE_SPEAKER_COLUMN] == '2':
			print('skipping: ', sona_id, ' reason: nonnative en speaker')
			continue
		if DO_FILTER_ES_NATIVE and row[IS_NATIVE_SPEAKER_OFFSET] == '1':
			print('skipping: ', sona_id, ' reason: native es speaker')
			continue

		participant_count += 1

		csv_writer.writerow(row)

print('data written; ', participant_count, ' participants')