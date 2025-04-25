import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import textstat

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(stopwords.words('english'))


def clean_text(text):
    '''
    text: unformatted text
    return: cleaned text
    '''
    
    text = re.sub(r"[^a-zA-Z\s]", "", text) # remove punctuation
    text = text.lower()
    tokens = nltk.word_tokenize(text) # tokenize text
    tokens = [word for word in tokens if word not in stopwords] # remove stop words
    
    return tokens

def word_count(text):
    '''
    text: unformatted text
    return: word count
    '''
    tokens = clean_text(text)
    return len(tokens)

def get_top_ngrams(text, n = 3, top_n = 1):
    '''
    Note: n-grams are used to find the most common phrases in the text.
    An n-gram is a sequence of n-tokens or words from the text that are frequenly used together.
    
    text: unformatted text
    n: n-gram size
    top_n: number of top n-grams to return
    return: list of top_n n-grams
    '''
    text = clean_text(text)
    grams = nltk.ngrams(text, n) # create n-grams
    ngram_freq = nltk.FreqDist(grams) # count n-grams
    top_ngrams = ngram_freq.most_common(top_n) # get top n-grams
    
    return top_ngrams
    
    
def get_top_words(text, top_n = 10):
    '''
    text: unformatted text
    top_n: number of top words to return
    return: list of top_n words
    '''
    tokens = clean_text(text)
    word_freq = nltk.FreqDist(tokens)
    top_words = word_freq.most_common(top_n) # get top words
    
    return top_words

def remove_stopwords(tokens):
    '''
    tokens: tokenized text from clean_text function
    stopwords: set of nltk stopwords
    return: text without stop words
    '''
    stopwords = set(stopwords.words('english'))
    return [word for word in tokens in word not in stopwords]


def readability_score(text):
    '''
    text: unformatted text
    return: readability score
    '''
    
    return textstat.flesch_reading_ease(text) # return readability score

def title_features(title):
    tokens = nltk.word_tokenize(title)
    
    return{
        'title_length': len(tokens),
        'avg_word_length': len(title) / len(tokens),
        'poses_question': '?' in title,
        'colon': ":" in title
    }
    
def lemmatize(tokens):
    '''
    tokens: tokenized text from abstract
    returns: a text blob with lemmatized infinitives. eg: studied -> study
    '''
    pass
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(t) for t in tokens])

# def make_cols(df, functions):
#     '''
#     df: dataframe
#     functions: list of functions to apply to the dataframe
#     return: dataframe with new columns
#     '''
    
#     if functions is None:
#         return df
#     else:
#         for function in functions:
#             # only apply funndtions on the abstract since we do not have the full article text
#             # and we do not want to download the full article text
#             if function.__name__ == 'title_features':
#                 title_features_dict = df['title'].apply(function)
#                 features_df = pd.DataFrame(title_features_dict.tolist())
#                 df = pd.concat([df,features_df], axis = 1)
#             df[function.__name__] = df['abstract'].apply(function)
#         return df