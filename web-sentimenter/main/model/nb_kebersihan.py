import time
import pickle
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Constants
NB_CLASSIFIER_MODEL_PATH = "ml_model/nb_classifier_kebersihan.pkl"
TFIDF_MODEL_PATH = "ml_model/tfidf_kebersihan_model.pkl"

# Inisialisasi objek stopword remover
stopword_factory = StopWordRemoverFactory()
stopwords = stopword_factory.get_stop_words()


def load_model(file_path):
    with open(file_path, "rb") as model_file:
        model = pickle.load(model_file)
    return model


tfidf_vectorizer = load_model(TFIDF_MODEL_PATH)
nb_kebersihan = load_model(NB_CLASSIFIER_MODEL_PATH)


def predict_review_kebersihan(data):
    tfidf_matrix = tfidf_vectorizer.transform(data["review"])

    start_time = time.time()
    prediction = nb_kebersihan.predict(tfidf_matrix)
    end_time = time.time()

    print(f"Aspek kebersihan prediction time: {end_time - start_time} seconds")

    data["label"] = prediction
    return data


def single_predict_review_kebersihan(review):
    tfidf_matrix = tfidf_vectorizer.transform([review])
    prediction = nb_kebersihan.predict(tfidf_matrix)

    return prediction
