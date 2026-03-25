import os
import urllib.request

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
urls = {
    'starry_night.t7': 'https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/starry_night.t7',
    'composition_vii.t7': 'https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/composition_vii.t7',
    'la_muse.t7': 'https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/la_muse.t7',
    'candy.t7': 'https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/candy.t7'
}

def download():
    os.makedirs(MODELS_DIR, exist_ok=True)
    for name, url in urls.items():
        path = os.path.join(MODELS_DIR, name)
        if not os.path.exists(path):
            print(f"Downloading {name} from {url}...")
            try:
                urllib.request.urlretrieve(url, path)
                print(f"Saved to {path}")
            except Exception as e:
                print(f"Failed to download {name}: {e}")
        else:
            print(f"{name} already exists.")

if __name__ == '__main__':
    download()
