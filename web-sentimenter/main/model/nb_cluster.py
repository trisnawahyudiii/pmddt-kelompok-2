import pickle
import pandas as pd
from .preprocessing import data_preprocessor, process_review
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import time


# Constants
NB_CLUSTER_MODEL_PATH = 'ml_model/nb_cluster.pkl'
TFIDF_MODEL_PATH = 'ml_model/tfidf_cluster_model.pkl'

# Inisialisasi objek stopword remover
stopword_factory = StopWordRemoverFactory()
stopwords = stopword_factory.get_stop_words()


def load_model(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model


def cluster_review(data):
    df = pd.DataFrame(data)

    start_time = time.time()
    clean_data = data_preprocessor(df)
    end_time = time.time()

    print(f"\nCleaning time: {end_time - start_time} seconds")

    tfidf_vectorizer = load_model(TFIDF_MODEL_PATH)
    nb_cluster = load_model(NB_CLUSTER_MODEL_PATH)

    tfidf_matrix = tfidf_vectorizer.transform(clean_data['review'])

    start_time = time.time()
    prediction = nb_cluster.predict(tfidf_matrix)
    end_time = time.time()
    print(f"\nClustering time: {end_time - start_time} seconds")

    df['aspek'] = prediction

    # Create three separate DataFrames based on predicted labels
    df_kebersihan = df[df['aspek'] == 'kebersihan']
    df_linen = df[df['aspek'] == 'linen']
    df_service = df[df['aspek'] == 'service']

    return df_kebersihan, df_linen, df_service
