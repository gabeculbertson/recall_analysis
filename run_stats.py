import numpy as np
from numpy import std, mean, sqrt
from scipy.stats import ttest_ind
from scipy.stats.stats import pearsonr
from libs.processed_data_util import get_processed_data_objects, get_data_for_slice
from libs.csv_utils import write_spreadsheet_file
from libs.partial_correlation import partial_correlation

from sklearn.feature_selection import RFE
from sklearn import linear_model

target_measures = [ 
	'translation_semantic',
	'translation_wer',
	'es_recall_wer', 
	'en_recall_wer', 
	'multiple_choice', 
	'self_report' 
]

row_data_objects = get_processed_data_objects('data/processed_data.txt')

def write_correlation_table_for_slice(name, row_in_slice):
	data_columns = get_data_for_slice(row_data_objects, row_in_slice)

	correlation_table = [ [ 'n=' + str(len(data_columns[target_measures[0]])) ] + target_measures ]
	for i, measure_1 in enumerate(target_measures):
		correlation_row = [ measure_1 + '-r' ]
		significance_row = [ measure_1 + '-p' ]
		correlation_table.append(correlation_row)
		correlation_table.append(significance_row)
		for j, measure_2 in enumerate(target_measures):
			if j < i:
				correlation_row.append('')
				significance_row.append('')
				continue

			if measure_1 == measure_2:
				correlation_row.append('-')
				significance_row.append('')
			else:
				correlation = pearsonr(data_columns[measure_1], data_columns[measure_2])
				corr_string = '%.3f' % correlation[0]
				if correlation[1] < 0.001 / 15:
					corr_string += '***'
				correlation_row.append(corr_string)
				significance_row.append(correlation[1])

	write_spreadsheet_file(name, correlation_table)

def write_partial_correlation_for_slice(name, row_in_slice, dependent, independent1, independent2, data):
	data_columns = get_data_for_slice(data, row_in_slice)

	partial_correlations = partial_correlation(data_columns[dependent], 
		data_columns[independent1], data_columns[independent2], independent1, independent2)
	write_spreadsheet_file(name, partial_correlations)


write_correlation_table_for_slice('output/correlations_all.txt', lambda x: True)
write_correlation_table_for_slice('output/correlations_translated_t.txt', lambda row: row['did_translate'] == '1')
write_correlation_table_for_slice('output/correlations_translated_f.txt', lambda row: row['did_translate'] == '2')
write_correlation_table_for_slice('output/correlations_lower_quartiles.txt', lambda row: row['in_upper_quartiles'] == '0')
write_correlation_table_for_slice('output/correlations_upper_quertiles.txt', lambda row: row['in_upper_quartiles'] == '1')

write_partial_correlation_for_slice('output/partial_correlations_all.txt', lambda row: True, 
	'translation_semantic', 'es_recall_wer', 'en_recall_wer', row_data_objects)
write_partial_correlation_for_slice('output/partial_correlations_sem_all.txt', lambda row: True, 
	'translation_semantic', 'es_recall_wer', 'en_recall_wer', row_data_objects)
write_partial_correlation_for_slice('output/partial_correlations_translated_t.txt', lambda row: row['did_translate'] == '1', 
	'translation_semantic', 'es_recall_wer', 'en_recall_wer', row_data_objects)
write_partial_correlation_for_slice('output/partial_correlations_translated_f.txt', lambda row: row['did_translate'] == '2', 
	'translation_semantic', 'es_recall_wer', 'en_recall_wer', row_data_objects)

row_data_objects_items = get_processed_data_objects('data/processed_recall_data.txt')
write_partial_correlation_for_slice('output/partial_recall_correlations_all.txt', lambda row: True, 
	'translation_semantic', 'es_recall_wer', 'duration', row_data_objects_items)