import csv
import inspect
from libs.constants import *
from libs.csv_utils import write_spreadsheet_file
from libs.wer import wer
from libs.wer import clean_extra_words
from libs.translation_util import get_translation_wer_score
from libs.semantic_util import get_total_semantic_score
from numpy import median

IN_FILE_NAME = 'data/filtered_raw_data.csv'
OUT_FILE_NAME = 'data/processed_data.csv'

csv_data = None
with open(IN_FILE_NAME, 'r', encoding="utf-8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	csv_data = list(csv_reader)

participant_count = 0

def add_column(out_data, name, get_value_from_row):
	if len(out_data) == 0:
		out_data.append([])
	out_data[0].append(name)

	column = []

	for row_index in range(0, len(csv_data) - FIRST_DATA_ROW):
		in_row = csv_data[row_index + FIRST_DATA_ROW]

		if len(out_data) <= row_index + 1:
			out_data.append([])
		out_row = out_data[row_index + 1]

		value = None
		if len(inspect.getargspec(get_value_from_row).args) == 2:
			value = get_value_from_row(in_row, out_row)
		else:
			value = get_value_from_row(in_row)
		out_row.append(value)
		column.append(value)
	return column

def add_column_multi(out_data, name, get_value_from_row):
	if len(out_data) == 0:
		out_data.append([])
	out_data[0].append(name)

	column = []

	for row_index in range(0, len(csv_data) - FIRST_DATA_ROW):
		in_row = csv_data[row_index + FIRST_DATA_ROW]
		value = None
		if len(inspect.getargspec(get_value_from_row).args) == 2:
			value = get_value_from_row(in_row, out_row)
		else:
			value = get_value_from_row(in_row)

		for val in value:
			if len(out_data) <= row_index + 1:
				out_data.append([])
			out_row = out_data[row_index + 1]

			out_row.append(value)
			column.append(value)
	return column

def get_id_from_row(row):
	return row[SONA_ID_COLUMN]

def get_multiple_choice_from_row(row):
	score = 0
	for index in range(0, MULTIPLE_CHOICE_COUNT):
		if str(MULTIPLE_CHOICE_ANSWERS[index]) == str(row[FIRST_MULTIPLE_CHOICE_COLUMN + index]):
			score += 1
	return score

def get_self_report_from_row(row):
	self_reported_skill = 0
	if int(row[IS_NATIVE_SPEAKER_OFFSET]) == 1:
		self_reported_skill = 7
	else:
		self_reported_skill = int(row[SPANISH_LEVEL])
	return self_reported_skill

def get_word_count_from_row(row):
	word_count = 0
	for index in range(0, RECALL_COUNT):
		column_index = FIRST_ES_RECALL_COLUMN + index * RECALL_INTERVAL
		hypothesis = row[column_index]
		split_hyp = hypothesis.split(' ')
		for word in split_hyp:
			if word:
				word_count += 1
	return word_count


def get_es_recall_wer_from_row(row):
	score = 0
	for index in range(0, RECALL_COUNT):
		column_index = FIRST_ES_RECALL_COLUMN + index * RECALL_INTERVAL
		reference = column_index_to_es_recall_reference[column_index]
		hypothesis = row[column_index]
		one_minus_wer = 1 - wer(reference, clean_extra_words(reference, hypothesis))
		score += one_minus_wer
	return score

def get_es_recall_wer_list_from_row(row):
	scores = []
	for index in range(0, RECALL_COUNT):
		column_index = FIRST_ES_RECALL_COLUMN + index * RECALL_INTERVAL
		reference = column_index_to_es_recall_reference[column_index]
		hypothesis = row[column_index]
		one_minus_wer = 1 - wer(reference, clean_extra_words(reference, hypothesis))
		scores.append(one_minus_wer)
	return scores

def get_en_recall_wer_from_row(row):
	score = 0
	for index in range(0, RECALL_COUNT):
		column_index = FIRST_EN_RECALL_COLUMN + index * RECALL_INTERVAL
		reference = column_index_to_en_recall_reference[column_index]
		hypothesis = row[column_index]
		one_minus_wer = 1 - wer(reference, clean_extra_words(reference, hypothesis))
		score += one_minus_wer
	return score

def get_translation_from_row(row):
	score = 0
	for index in range(0, TRANSLATION_COUNT):
		column_index = FIRST_TRANSLATION_COLUMN + index
		hypothesis = row[column_index]
		one_minus_wer = 1 - get_translation_wer_score(index, hypothesis)
		score += one_minus_wer
	return score

processed_data = []
add_column(processed_data, 'id', get_id_from_row)
add_column(processed_data, 'multiple_choice', get_multiple_choice_from_row)
add_column(processed_data, 'self_report', get_self_report_from_row)
add_column(processed_data, 'es_recall_wer', get_es_recall_wer_from_row)
add_column(processed_data, 'en_recall_wer', get_en_recall_wer_from_row)

translation_column = add_column(processed_data, 'translation_wer', get_translation_from_row)
add_column(processed_data, 'translation_semantic', lambda row: get_total_semantic_score(row[SONA_ID_COLUMN]))

translation_median = median(translation_column)
print('median translation score:', median(translation_column))
add_column(processed_data, 'in_upper_quartiles', lambda in_row, out_row: 0 if out_row[-2] < translation_median else 1)

add_column(processed_data, 'did_translate', lambda row: row[DID_TRANSLATE])

add_column(processed_data, 'translation_word_count', get_word_count_from_row)

# print(get_translation_wer_score(17, "i'm so sorry,. it's okay. what's ? lydia aguilar"))

write_spreadsheet_file('data/processed_data.txt', processed_data)
print('save successful; columns:', len(processed_data[0]), '; rows: ', len(processed_data) - 1) 
