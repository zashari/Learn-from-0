import json
from pymongo import MongoClient
from dotenv import find_dotenv, dotenv_values
from datetime import datetime

config = dotenv_values(find_dotenv())
client = MongoClient(config.get("MONGODB_URI"))
db = client["hackathon_db"]
conversation_history = db["user_history"]

def simpan_interaksi(user_id, topic, message):
    existing_interaction = conversation_history.find_one({"user_id": user_id, "topic": topic})

    new_interaction = {
        "role": message['role'],
        "content": message['content'],
        "timestamp": datetime.now(),
    }

    if existing_interaction:
        conversation_history.update_one(
            {"user_id": user_id, "topic": topic},
            {"$push": {"interactions": new_interaction}}
        )
    else:
        interaction = {
            "user_id": user_id,
            "topic": topic,
            "interactions": [new_interaction],
            "created_at": datetime.now(),
        }
        conversation_history.insert_one(interaction)

def get_previous_interactions(user_id, topic):
    try:
        document = conversation_history.find_one({"user_id": user_id, "topic": topic})
        if document:
            interactions = document.get('interactions', [])
            return interactions
        else:
            return []
    except Exception as e:
        print(f"Error retrieving interactions: {e}")
        return []

def hapus_semua_interaksi(user_id, topic):
    conversation_history.update_many(
        {"user_id": user_id, "topic": topic},
        {"$set": {"interactions": []}}  
    )