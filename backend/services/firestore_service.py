from google.cloud import firestore

db = firestore.Client()

def save_conversation(user_id, messages):
    conversation_ref = db.collection('conversations').document(user_id)
    conversation_ref.set({
        'messages': messages
    })

def get_conversation(user_id):
    conversation_ref = db.collection('conversations').document(user_id)
    conversation = conversation_ref.get()
    if conversation.exists:
        return conversation.to_dict().get('messages', [])
    return []