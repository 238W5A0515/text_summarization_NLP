import nltk
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')

def summarize_text(text, num_sentences=3):

    # Split text into sentences
    sentences = nltk.sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    # Convert sentences to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Create similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Build graph
    graph = nx.from_numpy_array(similarity_matrix)

    # Rank sentences using PageRank
    scores = nx.pagerank(graph)

    # Rank sentences
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)),
        reverse=True
    )

    # Select top sentences
    summary = " ".join([ranked_sentences[i][1] for i in range(num_sentences)])

    return summary