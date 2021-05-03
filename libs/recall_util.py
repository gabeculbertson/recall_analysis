from .tokenize import *

def get_words(text, stopwords=set()):
	text = clean(text)
	text = text.replace('\n', ' ').replace('\r', ' ')
	return [x for x in text.split(' ') if x and x not in stopwords]

def words_to_dict(words):
	word_dict = {}
	for word in words:
		word_dict[word] = True
	return word_dict

def get_subsequence(input_words, caption_words, start_index):
	longest_sequence = 0
	for i in range(0, len(caption_words)):
		j = 0
		# print(j, i, start_index, input_words)
		while j + start_index < len(input_words) and i + j < len(caption_words) and input_words[start_index + j] == caption_words[i + j]:
			j += 1
		if j > longest_sequence:
			longest_sequence = j
	return longest_sequence

def compare_input_text_to_caption_text(input_text, caption_text, stopwords=set()):
	invalid_displayed = False

	input_words = get_words(input_text, stopwords)
	input_word_dict = words_to_dict(input_words)

	caption_words = get_words(caption_text, stopwords)
	caption_word_dict = words_to_dict(caption_words)

	correct_count = 0
	for i, word in enumerate(input_words):
		if word in caption_word_dict:
			correct_count += 1
			seq = get_subsequence(input_words, caption_words, i)
			if seq > longest_sequence:
				longest_sequence = seq
		else:
			current_sequence = 0
			if not invalid_displayed:
				# print("\nTRUE: " + clean(caption_text).replace('\n', ' ').replace('\r', ' ') + "\nUSER: " + clean(input_text).replace('\n', ' ').replace('\r', ' '))
				invalid_displayed = True
			# print(">>>>" + word)
	return correct_count