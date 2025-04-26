import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from textstat import flesch_reading_ease

nltk.download('punkt')
nltk.download('punkt_tab')

def word_count(text):
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text)
    return len(tokens)

def word_diversity(text):
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    unique_tokens = set(tokens)
    return len(unique_tokens) / max(len(tokens), 1)

def avg_word_length(text):
    tokens = re.findall(r'\b[a-zA-Z]{2,}\b', text)
    return sum(len(word) for word in tokens) / max(len(tokens), 1)

def avg_sentence_length(text):
    sentences = sent_tokenize(text)
    if not sentences:
        return 0
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    return total_words / len(sentences)

def readability_score(text):
    try:
        score = flesch_reading_ease(text)
    except:
        score = 0
    return score

# Sentiment Analysis (Simple placeholder for extension)
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def sentiment_class(text):
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.6:
        return "Optimistic"
    elif 0.2 <= compound < 0.6:
        return "Positive"
    elif -0.2 < compound < 0.2:
        return "Neutral"
    elif -0.6 < compound <= -0.2:
        return "Cautious"
    else:
        return "Negative"

def get_title_features(title):
    return {
    "title_word_count": word_count(title),
    "title_word_diversity": word_diversity(title),
    "title_avg_word_len": avg_word_length(title),
    "title_avg_sent_len": avg_sentence_length(title),
    "title_sentiment": sentiment_class(title)
    }

def get_abstract_features(abstract):
    return {
    "abstract_word_count": word_count(abstract),
    "abstract_word_diversity": word_diversity(abstract),
    "abstract_avg_word_len": avg_word_length(abstract),
    "abstract_avg_sent_len": avg_sentence_length(abstract),
    "abstract_readability": readability_score(abstract),
    "abstract_sentiment": sentiment_class(abstract)
    }

def get_all_text_features(row):
    return {
    **get_title_features(row.get("title", "")),
    **get_abstract_features(row.get("abstract", ""))
    }

