from pymongo import MongoClient
from dotenv import find_dotenv, dotenv_values
from datetime import datetime

config = dotenv_values(find_dotenv())
client = MongoClient(config.get("MONGODB_URI"))
db = client["hackathon_db"] 
conversation_history = db["user_history"] 

def simpan_interaksi(user_id, topic, prompt, response):
    """Menyimpan interaksi pengguna ke MongoDB."""
    existing_interaction = conversation_history.find_one({"user_id": user_id, "topic": topic})
    
    # Membuat data baru untuk disimpan
    new_interaction = {
        "prompt": prompt,
        "response": response,
        "timestamp": datetime.now(),
    }
    
    if existing_interaction:
        # Jika sudah ada interaksi, tambahkan prompt dan response baru ke array
        conversation_history.update_one(
            {"user_id": user_id, "topic": topic},
            {"$push": {"interactions": new_interaction}}
        )
    else:
        # Jika belum ada, buat entry baru dengan array interactions
        interaction = {
            "user_id": user_id,
            "topic": topic,
            "interactions": [new_interaction],  # Menyimpan prompt dan response dalam array
            "created_at": datetime.now(),
        }
        conversation_history.insert_one(interaction)

def get_previous_interactions(user_id, topic):
    """Mengambil riwayat interaksi untuk user dan topik tertentu."""
    try:
        document = conversation_history.find_one({"user_id": user_id, "topic": topic})
        if document:
            interactions = document.get('interactions', [])
            return interactions
        else:
            print("Dokumen tidak ditemukan")  # Debugging output
            return []
    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil riwayat interaksi: {e}")  # Debugging output
        return []

def hapus_semua_interaksi(user_id, topic):
    """Menghapus semua interaksi untuk topik tertentu dari riwayat percakapan pengguna."""
    conversation_history.update_many(
        {"user_id": user_id, "topic": topic},
        {"$set": {"interactions": []}}  # Mengosongkan array interactions
    )