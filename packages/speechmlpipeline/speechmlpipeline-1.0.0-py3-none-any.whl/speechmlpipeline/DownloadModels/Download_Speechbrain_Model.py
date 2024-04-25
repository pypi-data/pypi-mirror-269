import os

from speechbrain.pretrained import SpeakerRecognition

download_model_path = '/Users/jf3375/Dropbox (Princeton)/speechmlmodels'
model_folder = 'Speechbrain'

def download_speechbrain_model(download_model_path, model_folder= 'speechbrain'):
    verification_model = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                                     savedir = os.path.join(download_model_path, model_folder))


