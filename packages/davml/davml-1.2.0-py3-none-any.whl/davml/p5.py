import re

def clean_text(text):
    # Remove punctuation and numbers using regular expressions
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = re.sub(r'\d+', '', cleaned_text)
    return cleaned_text

# Read the text file
with open('Modi_2019.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Clean the text
cleaned_text = clean_text(text)
import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize, sent_tokenize

# Tokenize at sentence level
sent_tokens = sent_tokenize(cleaned_text)

# Tokenize at word level
word_tokens = word_tokenize(cleaned_text)
!pip install nltk
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger')

# POS Tagging
pos_tags = pos_tag(word_tokens)
from nltk.corpus import stopwords
nltk.download('stopwords')

# Get English stopwords
stop_words = set(stopwords.words('english'))

# Remove stopwords
filtered_tokens = [word for word in word_tokens if word.lower() not in stop_words]
from nltk.stem import PorterStemmer

# Initialize Porter Stemmer
porter_stemmer = PorterStemmer()

# Stemming
stemmed_words = [porter_stemmer.stem(word) for word in filtered_tokens]

import matplotlib.pyplot as plt

# Visualize original text vs cleaned text length
plt.figure(figsize=(10, 6))
plt.bar(['Original Text', 'Cleaned Text'], [len(text), len(cleaned_text)], color=['blue', 'green'])
plt.title('Length of Original Text vs. Cleaned Text')
plt.ylabel('Number of Characters')
plt.show()
from nltk.probability import FreqDist

# Frequency Distribution of Word Tokens
word_freq = FreqDist(word_tokens)
plt.figure(figsize=(10, 6))
word_freq.plot(30, title='Top 30 Most Common Words')
plt.show()

