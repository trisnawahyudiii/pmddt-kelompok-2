import time
import pickle
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Constants
NB_CLASSIFIER_MODEL_PATH = 'ml_model/nb_classifier_service.pkl'
TFIDF_MODEL_PATH = 'ml_model/tfidf_service_model.pkl'

# Inisialisasi objek stopword remover
stopword_factory = StopWordRemoverFactory()
stopwords = stopword_factory.get_stop_words()


def load_model(file_path):
    with open(file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model


def predict_review_service(data):
    tfidf_vectorizer = load_model(TFIDF_MODEL_PATH)
    nb_service = load_model(NB_CLASSIFIER_MODEL_PATH)

    tfidf_matrix = tfidf_vectorizer.transform(data['review'])

    start_time = time.time()
    prediction = nb_service.predict(tfidf_matrix)
    end_time = time.time()

    print(f"Aspek service prediction time: {end_time - start_time} seconds")

    data['label'] = prediction
    return data
