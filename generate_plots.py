import numpy
import matplotlib.pyplot as plt
import libs.axis_titles as axis_titles
from libs.processed_data_util import get_processed_data_objects, get_data_for_slice

# fig_number = 1

def do_plot(filename, data_slice, measure_x, measure_y, include_trendline=False, fixed_axis=False, max_x=5, max_y=5):
	global fig_number
	fig_number += 1

	plt.figure(fig_number)
	if fixed_axis:
		plt.axis([0, max_x, 0, max_y])
	plt.xlabel(axis_titles.measure_to_title[measure_x], fontsize=axis_titles.half_figure_fontsize)
	plt.ylabel(axis_titles.measure_to_title[measure_y], fontsize=axis_titles.half_figure_fontsize)
	plt.scatter(data_slice[measure_x], data_slice[measure_y], s=8)

	# trendline
	if include_trendline:
		z = numpy.polyfit(data_slice[measure_x], data_slice[measure_y], 1)
		p = numpy.poly1d(z)
		plt.plot(data_slice[measure_x],p(data_slice[measure_x]),"-", color='gray')

	plt.savefig(filename, bbox_inches='tight', dpi=300)

fig_number = 1

row_data_objects = get_processed_data_objects('data/processed_data.txt')
data_slice_all = get_data_for_slice(row_data_objects, lambda x: True)
data_slice_translated_t = get_data_for_slice(row_data_objects, lambda row: row['did_translate'] == '1')
data_slice_translated_f = get_data_for_slice(row_data_objects, lambda row: row['did_translate'] == '2')
data_slice_lower_quartiles = get_data_for_slice(row_data_objects, lambda row: row['in_upper_quartiles'] == '0')
data_slice_upper_quartiles = get_data_for_slice(row_data_objects, lambda row: row['in_upper_quartiles'] == '1')



plt.figure(fig_number)
plt.xlabel(axis_titles.translation_wer_score)
plt.ylabel(axis_titles.recall_wer_score)
plt.scatter(data_slice_all['translation_wer'], data_slice_all['es_recall_wer'], s=2)
plt.savefig('output/tWER-rWER.png', bbox_inches='tight', dpi=300)

do_plot('output/tSem-rWER.png', data_slice_all, 'translation_wer', 'es_recall_wer')

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.translation_wer_score)
plt.ylabel(axis_titles.recall_wer_score)
plt.scatter(data_slice_translated_f['translation_wer'], data_slice_translated_f['es_recall_wer'], s=2, c='b')
plt.scatter(data_slice_translated_t['translation_wer'], data_slice_translated_t['es_recall_wer'], s=2, c='r')
plt.savefig('output/tWER-rWER-colors.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.translation_semantic_score)
plt.ylabel(axis_titles.recall_wer_score)
plt.scatter(data_slice_translated_f['translation_semantic'], data_slice_translated_f['es_recall_wer'], s=2, c='b')
plt.scatter(data_slice_translated_t['translation_semantic'], data_slice_translated_t['es_recall_wer'], s=2, c='r')
plt.savefig('output/tSem-rWER-colors.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.translation_semantic_score)
plt.ylabel(axis_titles.recall_wer_score)
plt.scatter(data_slice_translated_f['translation_semantic'], data_slice_translated_f['es_recall_wer'], s=2)
plt.savefig('output/tSem-rWER.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.multiple_choice_score)
plt.ylabel(axis_titles.recall_wer_score)
plt.scatter(data_slice_all['multiple_choice'], data_slice_all['es_recall_wer'], s=2)
plt.savefig('output/mc-rWER.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.self_report)
plt.ylabel(axis_titles.recall_wer_score)
plt.scatter(data_slice_all['self_report'], data_slice_all['es_recall_wer'], s=2)
plt.savefig('output/self-rWER.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.ylabel(axis_titles.multiple_choice_score)
plt.xlabel(axis_titles.self_report)
plt.scatter(data_slice_all['multiple_choice'], data_slice_all['self_report'], s=2)
plt.savefig('output/mc-self.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.translation_wer_score)
plt.ylabel(axis_titles.multiple_choice_score)
plt.scatter(data_slice_all['translation_wer'], data_slice_all['multiple_choice'], s=2)
plt.savefig('output/tWER-mc.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.axis([0, 5, 0, 5])
plt.xlabel(axis_titles.recall_wer_score, fontsize=axis_titles.half_figure_fontsize)
plt.ylabel(axis_titles.en_recall_count, fontsize=axis_titles.half_figure_fontsize)
plt.scatter(data_slice_lower_quartiles['es_recall_wer'], data_slice_lower_quartiles['en_recall_wer'], s=8)

# trendline
z = numpy.polyfit(data_slice_lower_quartiles['es_recall_wer'], data_slice_lower_quartiles['en_recall_wer'], 1)
p = numpy.poly1d(z)
plt.plot(data_slice_lower_quartiles['es_recall_wer'],p(data_slice_lower_quartiles['es_recall_wer']),"-", color='gray')

plt.savefig('output/en_es_recall_left.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.axis([0, 5, 0, 5])
plt.xlabel(axis_titles.recall_wer_score, fontsize=axis_titles.half_figure_fontsize)
plt.ylabel(axis_titles.en_recall_count, fontsize=axis_titles.half_figure_fontsize)
plt.scatter(data_slice_upper_quartiles['es_recall_wer'], data_slice_upper_quartiles['en_recall_wer'], s=8)

# trendline
z = numpy.polyfit(data_slice_upper_quartiles['es_recall_wer'], data_slice_upper_quartiles['en_recall_wer'], 1)
p = numpy.poly1d(z)
plt.plot(data_slice_upper_quartiles['es_recall_wer'],p(data_slice_upper_quartiles['es_recall_wer']),"-", color='gray')

plt.savefig('output/en_es_recall_right.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.xlabel(axis_titles.recall_wer_score)
plt.ylabel(axis_titles.en_recall_count)
plt.scatter(data_slice_all['es_recall_wer'], data_slice_all['en_recall_wer'], s=2)
plt.savefig('output/en_es_recall.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.axis([0, 5, 0, 5])
plt.xlabel(axis_titles.recall_wer_score, fontsize=axis_titles.half_figure_fontsize)
plt.ylabel(axis_titles.en_recall_count, fontsize=axis_titles.half_figure_fontsize)
plt.scatter(data_slice_translated_f['es_recall_wer'], data_slice_translated_f['en_recall_wer'], s=8)

# trendline
z = numpy.polyfit(data_slice_translated_f['es_recall_wer'], data_slice_translated_f['en_recall_wer'], 1)
p = numpy.poly1d(z)
plt.plot(data_slice_translated_f['es_recall_wer'],p(data_slice_translated_f['es_recall_wer']),"-", color='gray')

plt.savefig('output/en_es_recall_translated_f.png', bbox_inches='tight', dpi=300)

fig_number += 1

plt.figure(fig_number)
plt.axis([0, 5, 0, 5])
plt.xlabel(axis_titles.recall_wer_score, fontsize=axis_titles.half_figure_fontsize)
plt.ylabel(axis_titles.en_recall_count, fontsize=axis_titles.half_figure_fontsize)
plt.scatter(data_slice_translated_t['es_recall_wer'], data_slice_translated_t['en_recall_wer'], s=8)

# trendline
z = numpy.polyfit(data_slice_translated_t['es_recall_wer'], data_slice_translated_t['en_recall_wer'], 1)
p = numpy.poly1d(z)
plt.plot(data_slice_translated_t['es_recall_wer'],p(data_slice_translated_t['es_recall_wer']),"-", color='gray')

plt.savefig('output/en_es_recall_translated_t.png', bbox_inches='tight', dpi=300)

do_plot('output/translation_es_recall_translated_t.png', data_slice_translated_t, 'translation_wer', 'es_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)
do_plot('output/translation_es_recall_translated_f.png', data_slice_translated_f, 'translation_wer', 'es_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)
do_plot('output/translation_en_recall_translated_t.png', data_slice_translated_t, 'translation_wer', 'en_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)
do_plot('output/translation_en_recall_translated_f.png', data_slice_translated_f, 'translation_wer', 'en_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)

do_plot('output/translation_sem_es_recall_translated_t.png', data_slice_translated_t, 'translation_semantic', 'es_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)
do_plot('output/translation_sem_es_recall_translated_f.png', data_slice_translated_f, 'translation_semantic', 'es_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)
do_plot('output/translation_sem_en_recall_translated_t.png', data_slice_translated_t, 'translation_semantic', 'en_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)
do_plot('output/translation_sem_en_recall_translated_f.png', data_slice_translated_f, 'translation_semantic', 'en_recall_wer', include_trendline=True, fixed_axis=True, max_x=18)

plt.show()