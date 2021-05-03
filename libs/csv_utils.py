def to_line(arr, delimiter='\t'):
	return delimiter.join(map(lambda x: str(x), arr))

def array_to_text(arr, delimiter='\t'):
	return '\n'.join(map(lambda x: to_line(x, delimiter), arr))

def write_spreadsheet_file(name, arr, delimiter='\t'):
	with open(name, 'w') as file:
		file.write(array_to_text(arr, delimiter))

def read_spreadsheet_file(name, delimiter='\t'):
	out = []
	with open(name, 'r') as file:
		for line in file:
			out.append(line.replace('\n', '').replace('\r', '').split(delimiter))
	return out