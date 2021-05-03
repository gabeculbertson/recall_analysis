from libs.csv_utils import read_spreadsheet_file

def num(s):
	try:
		return int(s)
	except TypeError:
		return None
	except ValueError:
		pass
	try:
		return float(s)
	except TypeError:
		return None

def get_processed_data_objects(filename):
	processed_data_table = read_spreadsheet_file(filename)
	row_headers = []
	for index in range(0, len(processed_data_table[0])):
		row_headers.append(processed_data_table[0][index])
	row_objects = []
	for row_index in range(1, len(processed_data_table)):
		row = processed_data_table[row_index]
		row_object = { '_row': row }
		for header_index in range(0, len(row_headers)):
			row_object[row_headers[header_index]] = row[header_index]
		row_objects.append(row_object)
	return row_objects

def get_data_for_slice(row_data_objects, row_in_slice):
	data_columns = dict()
	for row_object in row_data_objects:
		if not row_in_slice(row_object): continue

		for key in row_object:
			if key not in data_columns:
				data_columns[key] = []
			data_columns[key].append(num(row_object[key]))
	return data_columns