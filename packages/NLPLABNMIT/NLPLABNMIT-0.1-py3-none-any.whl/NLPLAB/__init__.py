def p1():
    return '''import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
import string
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text.lower())
    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens
def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmas
def stem(tokens):
    stemmer = PorterStemmer()
    stems = [stemmer.stem(token) for token in tokens]
    return stems
def main():
    # Sample text
    text = "Tokenization is the process of breaking down text into words and phrases. Stemming and Lemmatization are techniques used to reduce words to their base form."
    # Preprocess text
    tokens = preprocess_text(text)
    # Lemmatization
    lemmas = lemmatize(tokens)
    print("Lemmatization:")
    print(lemmas)
    # Stemming
    stems = stem(tokens)
    print("\nStemming:")
    print(stems)
if __name__ == "main": 
    main()'''


def p2():
    return '''import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv("financial_dataset.csv")

# Assuming "filename" is not defined, I'm removing it from the code.

X = data['text']  # Fixed typo in variable name
y = data['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=47)  # Fixed typos

vectorizer = CountVectorizer(ngram_range=(1, 2))  # Fixed typo
X_train_vectorized = vectorizer.fit_transform(X_train)  # Fixed typo
X_test_vectorized = vectorizer.transform(X_test)  # Fixed typo

classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

y_pred = classifier.predict(X_test_vectorized)

accuracy = accuracy_score(y_test, y_pred)  # Fixed typo
print("Accuracy:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred))'''


def p4():
    return '''import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer

# Sample text data
documents = [
    "baseball soccer basketball",
    "soccer basketball tennis",
    "tennis cricket",
    "cricket soccer"
]

# Create a CountVectorizer to convert text data into a matrix of token counts
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

# Apply Latent Semantic Analysis (LSA)
lsa = TruncatedSVD(n_components=2)  # You can adjust the number of components/topics
lsa.fit(X)

# Extract the components/topics
terms = vectorizer.get_feature_names()
topic_matrix = np.array([lsa.components_[i] / np.linalg.norm(lsa.components_[i]) for i in range(lsa.components_.shape[0])])

# Print the topics
print("Top terms for each topic:")
for i, topic in enumerate(topic_matrix):
    top_indices = topic.argsort()[-5:][::-1]  # Get the top 5 terms for each topic
    top_terms = [terms[index] for index in top_indices]
    print(f"Topic {i + 1}: {' '.join(top_terms)}")'''


def p3():
    return '''import pandas as pd
from sklearn.preprocessing import OneHotEncoder
# Example categorical data
categories = ['teacher', 'nurse', 'police', 'doctor']
# Convert categorical data into a DataFrame
data = pd.DataFrame({'Category': categories})
# Initialize the OneHotEncoder
encoder = OneHotEncoder(sparse_output=False, dtype=int)
# Fit and transform the categorical data
encoded_data = encoder.fit_transform(data)
# Convert the encoded data to a DataFrame
encoded_df = pd.DataFrame(encoded_data, columns=categories)
# Print the encoded DataFrame
encoded_df.head()

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

documents = ["This is the first document.",
"This document is the second document.",
"And this is the third one.",
"Is this the first document?"]
# Convert text data into a DataFrame
data = pd.DataFrame({'Text': documents})
# Initialize the CountVectorizer
vectorizer = CountVectorizer()
# Fit and transform the text data
bow_vectors = vectorizer.fit_transform(data['Text'])
# Convert the BOW vectors to a DataFrame
bow_df = pd.DataFrame(bow_vectors.toarray(), columns=vectorizer.get_feature_names_out())
# Print the BOW DataFrame
bow_df.head()

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
# Example text data
documents = ["This is the first document.",
"This document is the second document.",
"And this is the third one.",
"Is this the first document?"]
# Convert text data into a DataFrame
data = pd.DataFrame({'Text': documents})
# Initialize the CountVectorizer with desired n-gram range
ngram_vectorizer = CountVectorizer(ngram_range=(2,3))

ngram_vectors = ngram_vectorizer.fit_transform(data['Text'])
# Convert the N-gram vectors to a DataFrame
ngram_df = pd.DataFrame(ngram_vectors.toarray(), columns=ngram_vectorizer.get_feature_names_out())
# Print the N-gram DataFrame
ngram_df.head()

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

documents = ["This is the first document.",
"This document is the second document.",
"And this is the third one.",
"Is this the first document?"]
# Convert text data into a DataFrame
data = pd.DataFrame({'Text': documents})
# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
# Fit and transform the text data
tfidf_vectors = vectorizer.fit_transform(data['Text'])
# Convert the TF-IDF vectors to a DataFrame
tfidf_df = pd.DataFrame(tfidf_vectors.toarray(), columns=vectorizer.get_feature_names_out())

tfidf_df.head()


import numpy as np

# Define a function to calculate the length of each document
def tlen(doc):
    return len(doc)

# Your text data
a = [
    "This is the first document",
    "This document is the second document the third one.",
    "And this is 'Is this the first document?'"
]


# Calculate the custom features
custom_features = np.array([tlen(doc) for doc in a])

# Print the custom features
print("Custom features:", custom_features)
import pandas as pd
from gensim.models import FastText

sentences = [["I", "like", "apples"],
["I", "enjoy", "eating", "fruits"]]
# Training the FastText model
model_fasttext = FastText(sentences, min_count=1, window=5, vector_size=100)
# Accessing word vectors
word_vectors = model_fasttext.wv
# Creating a DataFrame for word vectors
word_vectors_df = pd.DataFrame(word_vectors.vectors, index=word_vectors.index_to_key)
# Displaying the word vectors DataFrame
word_vectors_df.head(10)


'''