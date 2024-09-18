import random
import nltk
from pymongo import MongoClient
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import json

# Download nltk dataset for tokenization
nltk.download('punkt')

# Load chatbot intents file (you'll need a json file containing responses)
with open('intents.json') as file:
    intents = json.load(file)

# MongoDB client setup (ensure MongoDB is running)
client = MongoClient('mongodb://localhost:27017/')
db = client['education_db']  # Your MongoDB database
institutions_collection = db['institutions']  # Collection for institutions

# Loading a pre-trained model (example of a neural network model for the chatbot)
model = load_model('chatbot_model.h5')

# Function to preprocess input text
def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())
    return ' '.join(tokens)

# Function to predict the intent of the user's message
def predict_intent(text):
    # Preprocess the user input
    input_text = preprocess_text(text)
    
    # Vectorize and predict using the neural network
    input_data = np.array([input_text])  # Placeholder; vectorization should happen here
    prediction = model.predict(input_data)
    
    # Choose the most likely intent
    intent_idx = np.argmax(prediction)
    return intents['intents'][intent_idx]['tag']

# Chatbot response based on predicted intent
def get_response(intent):
    for intent_data in intents['intents']:
        if intent_data['tag'] == intent:
            return random.choice(intent_data['responses'])

# Example chatbot logic (main function)
def chatbot():
    print("Hello! I am your educational institution search assistant.")
    while True:
        message = input("You: ")
        if message.lower() == "quit":
            break
        
        # Predict intent and generate response
        intent = predict_intent(message)
        response = get_response(intent)
        
        # Special handling for institution search
        if intent == "search_institutions":
            search_institutions()

        print(f"Bot: {response}")

# Function to search institutions from MongoDB
def search_institutions():
    # Example search criteria; you can customize based on user input
    location = input("Enter preferred location: ")
    field = input("Enter field of study: ")
    
    # Query MongoDB for institutions matching the criteria
    query = {"location": location, "field": field}
    results = institutions_collection.find(query)
    
    if results.count() > 0:
        print("Here are some institutions based on your criteria:")
        for result in results:
            print(f"- {result['name']}, {result['location']} (Field: {result['field']})")
    else:
        print("No institutions found based on your criteria.")

if __name__ == "__main__":
    chatbot()
