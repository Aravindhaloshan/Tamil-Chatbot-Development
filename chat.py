
import json
import random  

from sentence_transformers import SentenceTransformer, util 


model_name = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
model = SentenceTransformer(model_name)


with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

encoded_patterns = []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        pattern_embedding = model.encode(pattern, convert_to_tensor=True)
        encoded_patterns.append((pattern_embedding, intent['responses']))
bot_name = "SRH"

def get_response(msg):
    if not msg.strip():  
        return "சரியான கேள்வியை வழங்கவும்."


    user_embedding = model.encode(msg, convert_to_tensor=True)

  
    max_score = -1
    best_response = ""
    for pattern_embedding, responses in encoded_patterns:
        score = util.pytorch_cos_sim(user_embedding, pattern_embedding).item()
        if score > max_score:
            max_score = score
            best_response = random.choice(responses)

    if max_score < 0.4:
        return "எனக்கு புரியவில்லை. மீண்டும் சொல்ல முடியுமா?"

    return best_response

if __name__ == "__main__":
    print("Chat செய்வோம்! (வெளியேற 'வெளியேறு' என தட்டச்சு செய்யவும்)")
    while True:
        sentence = input("உங்கள் கேள்வி: ")
        if sentence == "வெளியேறு":
            break

        resp = get_response(sentence)
        print(resp)
		
