from libs.csv_utils import read_spreadsheet_file

spreadsheet_data = read_spreadsheet_file('data/semantic_similarity.txt')
score_by_translation_id = dict()
for row in spreadsheet_data:
	pid = row[0]
	tid = int(row[1])
	score = 0
	try:
		score = float(row[2])
	except:
		pass

	if pid not in score_by_translation_id:
		score_by_translation_id[pid] = dict()
	score_by_translation_id[pid][tid] = score

def get_total_semantic_score(pid):
	score = 0
	if pid in score_by_translation_id:
		print(score_by_translation_id[pid])
		for key, value in score_by_translation_id[pid].items():
			score += value
	return score