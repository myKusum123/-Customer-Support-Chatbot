# chatbot_app/utils.py

import spacy
from transformers import pipeline

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def generate_response_based_on_entities(entities):
    for entity, label in entities:
        if label == "GPE":  # Geopolitical Entity
            return f"You're asking about {entity}. How can I help you with that location?"
        elif label == "PERSON":
            return f"Tell me more about {entity}."
    return "I'm sorry, I didn't understand that. Can you please clarify?"

# Load the sentiment-analysis pipeline
sentiment_analysis = pipeline('sentiment-analysis')

def analyze_sentiment(text):
    result = sentiment_analysis(text)[0]
    return f"Sentiment: {result['label']}, Score: {result['score']}"
