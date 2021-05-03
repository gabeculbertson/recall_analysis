from .constants import *
from .csv_utils import read_spreadsheet_file
from .csv_utils import write_spreadsheet_file
from .wer import wer

REFERENCE_TRANSLATION_FILES = [ 
	'data/reference_translations_1.txt', 
	'data/reference_translations_2.txt' 
	]

reference_translations = []

def clean(text):
	return text.replace('\t', ' ').replace('\n', ' ')

def add_reference_to_index(index, reference):
	if reference == '' or reference.isspace():
		return 

	while len(reference_translations) <= index:
		reference_translations.append(set())

	reference_translations[index].add(clean(reference))


for file in REFERENCE_TRANSLATION_FILES:
	table = read_spreadsheet_file(file)

	for row_index in range(1, len(table)):
		row = table[row_index]
		translation_index = int(row[1])
		official_translation = row[3]
		translator_translation = row[7]

		if not official_translation.isspace():
			add_reference_to_index(translation_index, official_translation)
		if not official_translation.isspace():
			add_reference_to_index(translation_index, translator_translation)

def reference_translations_to_table():
	reference_translation_table = []
	for index, translation_set in enumerate(reference_translations):
		reference_translation_table.append(list(translation_set))
		print('size ', index, ':', len(translation_set))
		print(translation_set)
	return reference_translation_table

write_spreadsheet_file('output/reference_translations.txt', reference_translations_to_table())

# get the best WER score from the possible reference translations for a given index
def get_translation_wer_score(index, hypothesis):
	score = 1
	for ref in reference_translations[index]:
		ref_score = wer(ref, hypothesis)
		if ref_score < score:
			score = ref_score
	return score