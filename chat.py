import json
import random  

from sentence_transformers import SentenceTransformer, util 


model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model = SentenceTransformer(model_name)

with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

bot_name = "SRH"

def get_response(msg):
    if not msg.strip():  # Check if the input message is empty or contains only whitespace
        return "சரியான கேள்வியை வழங்கவும்."

    # Encode the user message
    user_embedding = model.encode(msg, convert_to_tensor=True)

    # Loop through intents and find the most similar response
    max_score = -1
    best_response = ""
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            
            pattern_embedding = model.encode(pattern, convert_to_tensor=True)

           
            score = util.pytorch_cos_sim(user_embedding, pattern_embedding).item()

            
            if score > max_score:
                max_score = score
                best_response = random.choice(intent['responses'])  # Use random.choice here

    # If the similarity score doesn't meet a certain threshold, provide a default response
    if max_score < 0.4:
        return "எனக்கு புரியவில்லை. மீண்டும் சொல்ல முடியுமா?"

    # Return the best response
    return best_response

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)