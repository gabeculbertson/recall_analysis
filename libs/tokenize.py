punctuation = '.,!?<>…:¿¡()\'-_;\n\t'

def clean(text):
	for c in punctuation:
		text = text.replace(c, ' ')
	text = text.replace('ñ', 'n')
	text = text.replace('á', 'a')
	text = text.replace('é', 'e')
	text = text.replace('í', 'i')
	text = text.replace('ó', 'o')
	text = text.lower()
	text = text.strip()
	return ' '.join(text.split())

def tokenize(text):
	text = clean(text)

	if text == '':
		return []

	return text.split(' ')