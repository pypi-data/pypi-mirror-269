import os
import ssl
import whisper

download_model_path = '/Users/jf3375/Dropbox (Princeton)/speechmlmodels'
model_folder = 'Whisper'
def download_whisper_model(download_model_path, model_folder='whisper'):
    ssl._create_default_https_context = ssl._create_unverified_context
    whisper.load_model("large-v2", download_root=os.path.join(download_model_path, model_folder))