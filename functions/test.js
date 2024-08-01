const nltk = require('nltk');
const { sent_tokenize, word_tokenize } = nltk;
const { stopwords } = nltk.corpus;
const { punctuation } = require('string');
const { nlargest } = require('heapq');

function summarize(text, numSentences = 3) {
    // Разбиение текста на предложения
    let sentences = sent_tokenize(text);

    // Разбиение текста на слова
    let words = word_tokenize(text.toLowerCase());

    // Удаление стоп-слов и пунктуации
    let stopWords = new Set(stopwords.words('english').concat(punctuation));

    // Подсчёт частоты встречаемости каждого слова, исключая стоп-слова
    let wordFreq = {};
    for (let word of words) {
        if (!stopWords.has(word)) {
            if (!wordFreq[word]) {
                wordFreq[word] = 1;
            } else {
                wordFreq[word]++;
            }
        }
    }

    // Нормализация частоты встречаемости
    let maxFreq = Math.max(...Object.values(wordFreq));
    for (let word in wordFreq) {
        wordFreq[word] /= maxFreq;
    }

    // Оценка важности предложений на основе частоты встречаемости слов
    let sentScores = {};
    for (let sent of sentences) {
        let sentWords = word_tokenize(sent.toLowerCase());
        for (let word of sentWords) {
            if (wordFreq[word]) {
                if (sent.split(' ').length < 30) {
                    sentScores[sent] = sentScores[sent] || 0;
                    sentScores[sent] += wordFreq[word];
                }
            }
        }
    }

    // Выбор наиболее важных предложений
    let summarySentences = nlargest(numSentences, Object.keys(sentScores), (a, b) => sentScores[a] - sentScores[b]);
    let summary = summarySentences.join(' ');
    return summary;
}

// Пример использования
let text = "This is an example text that we want to summarize. There can be multiple sentences in the text. Summarization will help us get a brief overview of the text.";
let summarizedText = summarize(text, 2); // Суммаризуем текст до 2 предложений
console.log(summarizedText);


