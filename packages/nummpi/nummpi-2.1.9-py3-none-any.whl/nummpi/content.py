#Content Analysis

import nltk
import pandas as pd
import matplotlib.pylab as plt
import gensim
from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Read data from CSV file
df = pd.read_csv('/content/drive/MyDrive/SMA_datasets_prac_exam/social_media_data.csv')

# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')

# Tokenization, stopword removal, and lemmatization
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return filtered_tokens

df['tokens'] = df['text'].apply(preprocess_text)

# Create dictionary and document-term matrix
dictionary = corpora.Dictionary(df['tokens'])
corpus = [dictionary.doc2bow(tokens) for tokens in df['tokens']]

# Topic modeling using LDA
num_topics = 5  # Adjust the number of topics as needed
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20)

# Print topics
print("Topics:")
for topic_id in range(num_topics):
    print(f"Topic {topic_id + 1}: {lda_model.print_topic(topic_id)}")

# Keyword extraction
all_tokens = [token for tokens in df['tokens'] for token in tokens]
keyword_counter = Counter(all_tokens)

# Print most common keywords
num_keywords = 10  # Adjust the number of keywords as needed
print("\nTop Keywords:")
for keyword, count in keyword_counter.most_common(num_keywords):
    print(f"{keyword}: {count}")

# Display topics in a structured format
print("Identified Topics from LDA:")
for idx in range(num_topics):
    topic_info = lda_model.print_topic(idx, topn=10)  # Get the top 10 terms per topic
    topic_number = idx + 1
    words_and_weights = topic_info.split(" + ")
    print(f"\nTopic {topic_number}:")
    for item in words_and_weights:
        weight, word = item.split("*")
        print(f"  - {word.strip()} (Weight: {weight.strip()})")

# visualization
for idx, topic in enumerate(lda_model.show_topics(num_topics, formatted=False)):
    topic_terms = [term[0] for term in topic[1]]
    term_weights = [term[1] for term in topic[1]]

    plt.figure()
    plt.bar(topic_terms, term_weights, color='skyblue')
    plt.title(f"Topic {idx + 1}")
    plt.xlabel("Terms")
    plt.ylabel("Weights")
    plt.show()