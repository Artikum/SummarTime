from rutermextract import TermExtractor
import pymorphy2 
from summa import keywords 
from langdetect import detect 


from rake_nltk import Rake
import yake
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from heapq import nlargest

from nltk.stem import WordNetLemmatizer

# Загрузка стоп-слов для английского языка
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

import requests
from bs4 import BeautifulSoup


from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
# CORS(app, supports_credentials=True, origin='*')

def lemmatize_text(text, language='english'):
    if language == 'russian':
        morph = pymorphy2.MorphAnalyzer()
        lemmatized_words = [morph.parse(word)[0].normal_form for word in text.split()]
        return ' '.join(lemmatized_words)
    elif language == 'english':
        tokens = word_tokenize(text)
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(lemmatized_words)
    else:
        er = "Unsupported language. Only 'english' and 'russian' are supported. You tryed it in " + language 
        raise ValueError(er)

def clean_text(text):
    # Токенизация текста
    tokens = word_tokenize(text)
    # Загрузка списка стоп-слов для английского языка
    english_stop_words = set(stopwords.words('english'))
    # Удаление стоп-слов и знаков пунктуации
    filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in english_stop_words]
    # Объединение токенов обратно в текст
    clean_text = ' '.join(filtered_tokens)
    return clean_text

def process_text(text):
    # Здесь вы можете реализовать свою функцию обработки текста
    return text.lower()  # Пример: возвращаем текст в верхнем регистре

@app.route('/preprocess', methods=['POST'])
def preprocess_text():
    language='english'
    data = request.get_json()
    text = data.get('text')
    # Лемматизация текста
    lemmatized_text = lemmatize_text(text, language)
    # Очистка текста от стоп-слов и знаков пунктуации
    cleaned_text = clean_text(lemmatized_text)
    #clean_text = process_text(cleaned_text)
    return jsonify({'text': process_text(cleaned_text)})

    # text1 = data.get('text1')
    # text2 = data.get('text2')

    # if not text1 or not text2:
    #     return jsonify({"error": "Both text1 and text2 are required"}), 400

    # result = text1 in text2
    # return jsonify({'text': result})

# @app.route('/titlegen', methods=['POST'])
# def generate_title():
#     # Определяем язык текста
#     data = request.get_json()
#     input_text = data.get('text')#data['text']
#     language = detect(input_text)

#     if language == 'ru':
#         # Извлечение ключевых слов из текста на русском языке
#         term_extractor = TermExtractor()
#         terms = term_extractor(input_text)
#         extracted_keywords = [term.lemmatize for term in terms][:5]  # Берем первые 5 ключевых слов
#     else:
#         # Извлечение ключевых слов из текста на английском языке
#         extracted_keywords = keywords.keywords(input_text, language='english', words=5).split('\n')

#     # Создание заголовка на основе извлеченных ключевых слов
#     title = ' '.join(extracted_keywords)
#     return jsonify({'text': extracted_keywords})





@app.route('/titlegen', methods=['POST'])
def summarize():
    num_sentences=3
    data = request.get_json()
    input_text = data.get('text')#data['text']
    text = process_text(input_text)
    
    # Разбиение текста на предложения
    sentences = sent_tokenize(text)

    # Разбиение текста на слова
    words = word_tokenize(text.lower())

    # Удаление стоп-слов и пунктуации
    stop_words = set(stopwords.words('russian') + list(punctuation))

    # Подсчёт частоты встречаемости каждого слова, исключая стоп-слова
    word_freq = {}
    for word in words:
        if word not in stop_words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1

    # Нормализация частоты встречаемости
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    # Оценка важности предложений на основе частоты встречаемости слов
    sent_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if len(sent.split(' ')) < 15:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word]
                    else:
                        sent_scores[sent] += word_freq[word]

    # Выбор наиболее важных предложений
    summary_sentences = nlargest(num_sentences, sent_scores, key=sent_scores.get)
    summary = ' '.join(summary_sentences)
    #return summary
    return jsonify({'text': summary})


@app.route('/summertime', methods=['POST'])
def summarizeSummerTime():
    num_sentences=3
    data = request.get_json()
    input_text = data.get('text')#data['text']
    text = process_text(input_text)
    
    # Разбиение текста на предложения
    sentences = sent_tokenize(text)

    # Разбиение текста на слова
    words = word_tokenize(text.lower())

    # Удаление стоп-слов и пунктуации
    stop_words = set(stopwords.words('russian') + list(punctuation))

    # Подсчёт частоты встречаемости каждого слова, исключая стоп-слова
    word_freq = {}
    for word in words:
        if word not in stop_words:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1

    # Нормализация частоты встречаемости
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    # Оценка важности предложений на основе частоты встречаемости слов
    sent_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word]
                    else:
                        sent_scores[sent] += word_freq[word]

    # Выбор наиболее важных предложений
    summary_sentences = nlargest(num_sentences, sent_scores, key=sent_scores.get)
    summary = ' '.join(summary_sentences)
    #return summary
    return jsonify({'text': summary})


# @app.route('/titlegen', methods=['POST'])
# def generate_title():
#     # Определяем язык текста
#     data = request.get_json()
#     input_text = data.get('text')
#     language = detect(input_text)

#     if language == 'ru':
#         # Извлечение ключевых слов из текста на русском языке
#         rake = Rake(language='russian')
#         rake.extract_keywords_from_text(input_text)
#         extracted_keywords = rake.get_ranked_phrases()[:5]  # Берем первые 5 ключевых слов
#     else:
#         # Извлечение ключевых слов из текста на английском языке
#         kw_extractor = yake.KeywordExtractor(lan=language, n=1, top=5)
#         keywords_list = kw_extractor.extract_keywords(input_text)
#         extracted_keywords = [kw[0] for kw in keywords_list]

#     # Создание заголовка на основе извлеченных ключевых слов
#     title = ' '.join(extracted_keywords)
#     return jsonify({'text': extracted_keywords})

@app.route('/textcollector', methods=['POST'])
def search_and_save_links():
    data = request.get_json()
    query = data.get('text')#
    limit = data.get('int')
    myInt = int(limit)
    # Задаем URL для поиска, например, Google
    url = f"https://www.google.com/search?q={query}"
    
    # Отправляем запрос
    response = requests.get(url)
    
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим все ссылки на странице результатов поиска
        links = soup.find_all('a')
        
        # Счетчик для ограничения количества сохраняемых ссылок
        count = 0
        
        # Список для сохранения проверенных и подходящих ссылок
        saved_links = []
        
        # Проходимся по найденным ссылкам
        for link in links:
            href = link.get('href')
            
            # Проверяем, что ссылка не является ссылкой на результаты поиска, картой или изображением
            if href.startswith('/url?q=http') and not any(ext in href for ext in ['.google.', '/maps/', '/search?q=related:', '/imgres?']):
                # Извлекаем саму ссылку
                clean_link = href.split('/url?q=')[1].split('&')[0]
                
                # Проверяем, что ссылка не на Википедию на любом языке
                if "wikipedia.org" in clean_link:
                    continue
                
                # Проверяем, что ссылка не находится в списке игнорируемых сайтов
                # if ignored_sites and any(site in clean_link for site in ignored_sites):
                #     continue
                
                # # Проверяем содержимое веб-страницы на наличие запрещенных слов
                # if forbidden_words:
                #     page_response = requests.get(clean_link)
                #     if page_response.status_code == 200:
                #         page_content = page_response.text.lower()
                #         if any(word in page_content for word in forbidden_words):
                #             continue
                
                # Добавляем ссылку в список сохраненных ссылок
                saved_links.append(clean_link)
                
                # Увеличиваем счетчик сохраненных ссылок
                count += 1
                
                # Если количество сохраненных ссылок достигло лимита, прерываем цикл
                if count == myInt:
                    break
        
        # Возвращаем список сохраненных ссылок
        return jsonify({'text': saved_links})
    else:
        # Если запрос не удался, выводим сообщение об ошибке
        #print("Ошибка при отправке запроса")
        return jsonify({'text': "Ошибка при отправке запроса"})
# def detect_language():
#     data = request.get_json()
#     input_text = data.get('text')#data['text']
#     try:
#         language = detect(input_text)
#         if language == "en":
#             language = "english"
#         elif language == "ru":
#             language = "russian"
#         return jsonify({'text': language})
#     except:
#         return jsonify({'text': "unknown"})


if __name__ == '__main__':
    app.run(debug=True)