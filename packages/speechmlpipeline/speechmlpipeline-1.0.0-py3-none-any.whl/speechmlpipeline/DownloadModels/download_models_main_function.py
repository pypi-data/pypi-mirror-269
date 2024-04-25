from .Download_Whisper_Model import download_whisper_model
from .Download_Llama_Model import download_llama_model
from .Download_Speechbrain_Model import download_speechbrain_model

def download_models_main_function(download_model_path, models_list, hf_access_token):
    '''
    The main function to download models and save them on the local path

    :param download_model_path: A path to save all the downloaded models files
    :type download_model_path: str
    :param models_list: A list of the names of the models to be downloaded
    :type models_list: str
    :param hf_access_token: Access token to HuggingFace
    :type hf_access_token: str
    :return: None
    :rtype: None
    '''
    if 'whisper' in models_list:
        download_whisper_model(download_model_path, model_folder='whisper')
    if 'speechbrain' in models_list:
        download_speechbrain_model(download_model_path, model_folder = 'speechbrain')
    if 'llama2-13b' in models_list:
        download_llama_model(download_model_path, hf_access_token, model_folder = 'llama',
                         llama_model_repo_id='meta-llama/Llama-2-13b-chat-hf')
    if 'llama2-70b' in models_list:
        download_llama_model(download_model_path, hf_access_token, model_folder = 'llama',
                         llama_model_repo_id='meta-llama/Llama-2-70b-chat-hf')
