from google.cloud import firestore

def save_message(session_id: str, sender: str, message: str):
    db = firestore.Client()
    doc_ref = db.collection("conversations").document(session_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update({"messages": firestore.ArrayUnion([{"role": sender, "message": message}] )})
    else:
        doc_ref.set({"messages": [{"role": sender, "message": message}]})

def get_history(session_id: str):
    db = firestore.Client()
    doc_ref = db.collection("conversations").document(session_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get("messages", [])
    return []