import re
import pickle
import os
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
from services.training_data import TRAINING_DATA

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

STOP_WORDS = list(stopwords.words('english'))
MODEL_PATH = "services/email_classifier_model.pkl"


def clean_text(text: str) -> str:
    """
    Preprocess text: lowercase, remove URLs, special chars, extra spaces.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)    # remove URLs
    text = re.sub(r'[^a-z\s]', ' ', text)          # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()        # clean whitespace
    return text


def train_model():
    """
    Train Naive Bayes classifier using TF-IDF vectorization.
    Saves model to disk for reuse.
    """
    # Prepare training data
    texts  = [clean_text(text) for text, label in TRAINING_DATA]
    labels = [label for text, label in TRAINING_DATA]

    # Split into train/test sets (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # Build pipeline: TF-IDF + Naive Bayes
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            stop_words=STOP_WORDS,
            ngram_range=(1, 2),    # unigrams and bigrams
            max_features=5000
        )),
        ('clf', MultinomialNB(alpha=0.1))
    ])

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(f"✅ Model trained! Accuracy: {accuracy * 100:.1f}%")
    print(metrics.classification_report(y_test, y_pred))

    # Save model to disk
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    print(f"✅ Model saved to {MODEL_PATH}")
    return model


def load_model():
    """
    Load saved model from disk. Train if not exists.
    """
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    else:
        print("No saved model found. Training new model...")
        return train_model()


# Load model once when module is imported
model = load_model()


def classify_email(subject: str, body: str, sender: str = "") -> str:
    """
    Classify a single email using the trained ML model.
    """
    combined = clean_text(f"{subject} {body} {sender}")
    if not combined:
        return "general"
    prediction = model.predict([combined])
    return prediction[0]


def classify_bulk(emails: list) -> list:
    """
    Classify multiple emails at once.
    """
    results = []
    for email in emails:
        category = classify_email(
            subject=email.get("subject", ""),
            body=email.get("body", ""),
            sender=email.get("sender", "")
        )
        results.append({
            "gmail_id": email.get("gmail_id", ""),
            "subject":  email.get("subject", ""),
            "category": category
        })
    return results


def get_model_info() -> dict:
    """
    Return model information for supervisor demo.
    """
    texts  = [clean_text(text) for text, label in TRAINING_DATA]
    labels = [label for text, label in TRAINING_DATA]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )
    y_pred = model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)

    return {
        "model":           "Naive Bayes with TF-IDF Vectorization",
        "training_samples": len(TRAINING_DATA),
        "categories":      ["urgent", "spam", "newsletter", "social", "important", "general"],
        "accuracy":        f"{accuracy * 100:.1f}%",
        "features":        "TF-IDF with unigrams and bigrams, max 5000 features"
    }