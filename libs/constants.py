import csv

from .tokenize import *

FILE_NAME = 'data/base_raw_data.csv'
FIRST_DATA_ROW = 3
RECALL_INTERVAL = 5
RECALL_COUNT = 5
TRANSLATION_COUNT = 18
FIRST_MULTIPLE_CHOICE_COLUMN = 141
MULTIPLE_CHOICE_COUNT = 18
LAST_MULTIPLE_CHOICE_COLUMN = 158
SONA_ID_COLUMN = 161

csv_data = None
with open(FILE_NAME, 'r', encoding="utf-8") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
	csv_data = list(csv_reader)

def init_question_index(name):
	for i in range(0, len(csv_data[0])):
		if csv_data[0][i] == name:
			return i
	print("Could not find column: ", name)
	return -1
IS_NATIVE_SPEAKER_OFFSET = 23
ENGLISH_NATIVE_SPEAKER_COLUMN = init_question_index('Q1')
SPANISH_LEVEL = init_question_index("Q11")
FIRST_ES_RECALL_COLUMN = init_question_index("1_Q22")
FIRST_EN_RECALL_COLUMN = init_question_index("1_Q13")
FIRST_TRANSLATION_COLUMN = init_question_index("1_Q30_1")
DID_TRANSLATE = init_question_index("Q45")

es_recall_references = {
	'1_Q22': "Es un programa que lo tiene todo. Es un programa de los fines de semana. Es un programa de revista que lo tiene todo.",
	'2_Q22': "Pero no me lo van a creer, pero no he podido encontrar al ingeniero. Y ahora que venga, tengo que esperar a que se digne a atenderme",
	'3_Q22': "Oye, pero, a ver, ¿qué te dijo Alma? Que no, que ella no le va a hablar a mi papá, que le hable yo y que tengo que dar la cara.",
	'4_Q22': "Chalino, esto no esta muy lento? Si, es que hace una semana que vienen poquitos trabajadores. En serio?",
	'5_Q22': "¿entonces, qué? ¿quién es esa mujer de anoche? ¿no sabes cómo se llama? ¿es de aquí? ¿es turista? Yo no sé.",
	'6_Q22': "Necesito dos. No, ya no quedan. Entonces, para el Domingo?",
	'7_Q22': "Buenas tardes, señorita. Todavía hay entradas para el programa del sábado?",
	'8_Q22': "Para cuando? Para el viernes por la noche, sobre las nueve. Somos cuatro adultas y dos niños.",
	'9_Q22': "Un momento por favor, que tomo notas. Que día podría venir a su casa? El jueves o el viernes por la mañana.",
	'10_Q22': "Dado que la mayor parte de mi familia vino, decidimos ir a cenar al restaurante Español de siempre.",
}

column_index_to_es_recall_reference = {}
column_index_to_tokenized_es_recall_reference = {}
for key in es_recall_references:
	index = init_question_index(key)
	column_index_to_es_recall_reference[index] = es_recall_references[key]
	column_index_to_tokenized_es_recall_reference[index] = tokenize(es_recall_references[key])

en_recall_references = {
	'1_Q13': "Yeah, I could tell, since you didn't call or write the entire time it was happening. No, I know, I was just",
	'2_Q13': "the dedicated detectives who investigate these vicious felonies are members of an elite squad known as the special victims unit.",
	'3_Q13': "That addict and her pimp were down in the basement asking about the morgue. You didn’t let them stay there? Of course not. I made them return with me to the ground floor.",
	'4_Q13': "There's a really cool coffee place, Jitters, at the Steamtown Mall. You ever been there? No.",
	'5_Q13': "And you're worried about the imbalance in our currency, our foreign debt — all of it. You already have the president’s ear.",
}

column_index_to_en_recall_reference = {}
column_index_to_tokenized_en_recall_reference = {}
for key in en_recall_references:
	index = init_question_index(key)
	column_index_to_en_recall_reference[index] = en_recall_references[key]
	column_index_to_tokenized_en_recall_reference[index] = tokenize(en_recall_references[key])

MULTIPLE_CHOICE_ANSWERS = []
with open('data/answer-key.txt', 'r', encoding='utf-8') as answer_file:
	text = answer_file.read().split('\n')
	for line in text:
		MULTIPLE_CHOICE_ANSWERS.append(int(line))