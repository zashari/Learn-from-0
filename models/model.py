from pymongo import MongoClient
from dotenv import find_dotenv, dotenv_values
from datetime import datetime

config = dotenv_values(find_dotenv())
client = MongoClient(config.get("MONGODB_URI"))
db = client["nama_database_anda"] 
conversation_history = db["conversation_history"] 

def simpan_interaksi(user_id, topic, prompt, response):
    """Menyimpan interaksi pengguna ke MongoDB."""
    interaction = {
        "user_id": user_id,
        "topic": topic,
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.now(),
    }
    conversation_history.insert_one(interaction)

def get_previous_interactions(user_id, topic):
    """Mengambil riwayat interaksi untuk user dan topik tertentu."""
    return list(conversation_history.find({"user_id": user_id, "topic": topic}, {'_id': 0}))

def hapus_riwayat_topik(user_id, topic):
    """Menghapus riwayat percakapan untuk user dan topik tertentu."""
    conversation_history.delete_many({"user_id": user_id, "topic": topic})