memory_store = {}

def save_memory(user_id, history):

    memory_store[user_id] = history

def load_memory(user_id):

    return memory_store.get(user_id, [])
