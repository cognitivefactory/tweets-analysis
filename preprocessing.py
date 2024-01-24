import re
import string

import emoji

import spacy

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

EMOJI_PATTERN = re.compile('['
                            '\U0001F1E0-\U0001F1FF'  # flags (iOS)
                            '\U0001F300-\U0001F5FF'  # symbols & pictographs
                            '\U0001F600-\U0001F64F'  # emoticons
                            '\U0001F680-\U0001F6FF'  # transport & map symbols
                            '\U0001F700-\U0001F77F'  # alchemical symbols
                            '\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
                            '\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
                            '\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
                            '\U0001FA00-\U0001FA6F'  # Chess Symbols
                            '\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
                            '\U00002702-\U000027B0'  # Dingbats
                            '\U000024C2-\U0001F251'
                            ']+')

PUNCTUATION_PATTERN = re.compile('[%s]' % re.escape(string.punctuation))

HASHTAG_PATTERN = re.compile(r'#\w+')

USER_TAG_PATTERN = re.compile(r'@\w+')

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

stopwords_fr = stopwords.words('french')
""" stopwords_eng = stopwords.words('english')
stopwords_eng.remove('not')
stopwords_eng.remove('no') """

#nlp = spacy.load('fr_core_news_sm', disable=['parser', 'ner'])
#nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

def remove_stopwords(text, rem_unk=False):
    text = ' '.join([word for word in word_tokenize(text) if word not in stopwords_fr])
    """ if rem_unk:
       text = ' '.join([word for word in word_tokenize(text) if word in nlp.vocab.strings]) """
    return text

def normalize(text):
    """ text = text.replace('œ', 'oe').replace('æ', 'ae').replace('«', '').replace('»', '').replace('-',' ').replace('   ',' ')
    text = text.replace('é','e').replace('è','e').replace('ê','e').replace('à','a').replace('â','a').replace('ô','o').replace('î','i')
    text = text.replace('ï','i').replace('û','u').replace('ù','u').replace('ç','c').replace('ë','e').replace('ü','u').replace('ÿ','y')
    text = text.replace('ñ','n').replace('(','').replace(')','').replace('…', '...').replace('\'', ' ').replace('°', '') """
    text = re.sub(USER_TAG_PATTERN, '', text)
    text = re.sub(HASHTAG_PATTERN, '', text)
    text = re.sub(EMOJI_PATTERN, '', text)
    text = re.sub(URL_PATTERN, '', text)
    #text = re.sub(PUNCTUATION_PATTERN, '', text)
    text = text.replace('\n', ' ').replace('/', '')
    text = text.replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
    return text

def stemming_text(text):
    stemmer = nltk.stem.SnowballStemmer('french')
    return ' '.join([stemmer.stem(word) for word in word_tokenize(text)])

def lemmatize_text(text):
    # return ' '.join([token.lemma_ for token in nlp(text)])
    lemmatizer = nltk.stem.WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)])

def preprocess_text(text: str, stem_lemm: str, rem_unk=False):
    text = normalize(text)
    text = text.lower()
    #text = remove_stopwords(text, rem_unk)
    match stem_lemm:
      case 'stem':
        text = stemming_text(text)
      case 'lemm':
        text = lemmatize_text(text)
      case 'none':
        pass
      case _:
        pass
    return text

def preprocess_texts(texts,stem_lemm, rem_unk=False):
    return [preprocess_text(text, stem_lemm) for text in texts]