from pymongo import MongoClient
from dotenv import find_dotenv, dotenv_values
from datetime import datetime

config = dotenv_values(find_dotenv())
client = MongoClient(config.get("MONGODB_URI"))
db = client["hackathon_db"] 
conversation_history = db["user_history"] 

def save_interaction(user_id, topic, interaction):
    """Menyimpan interaksi pengguna ke MongoDB."""
    timestamp = datetime.utcnow()  # Mendapatkan waktu sekarang dalam UTC
    try:
        # Mencari dokumen yang sesuai dengan user_id dan topic
        document = conversation_history.find_one({"user_id": user_id, "topic": topic})
        if document:
            # Jika dokumen ditemukan, tambahkan interaksi baru
            conversation_history.update_one(
                {"user_id": user_id, "topic": topic},
                {"$push": {"interactions": {"role": interaction["role"], "content": interaction["content"]}}}
            )
        else:
            # Jika dokumen tidak ditemukan, buat dokumen baru dengan interaksi
            conversation_history.insert_one({
                "user_id": user_id,
                "topic": topic,
                "interactions": [{
                    "role": interaction["role"],
                    "content": interaction["content"],
                }],
                "timestamp": timestamp
            })
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan interaksi: {e}")  # Debugging output

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

def delete_all_interactions(user_id, topic):
    """Menghapus semua interaksi untuk topik tertentu dari riwayat percakapan pengguna."""
    conversation_history.update_many(
        {"user_id": user_id, "topic": topic},
        {"$set": {"interactions": []}}  # Mengosongkan array interactions
    )