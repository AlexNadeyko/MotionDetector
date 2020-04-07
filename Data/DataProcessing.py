import  pickle

def load_encodings():
    with open(r'./Data/known_encodings.dat', 'rb') as f:
        encodings = pickle.load(f)
    return encodings


def save_encoding(encoding):
    old_encodings = load_encodings()
    old_encodings.update(encoding)

    with open(r'./Data/known_encodings.dat', 'wb') as f:
        pickle.dump(old_encodings, f)