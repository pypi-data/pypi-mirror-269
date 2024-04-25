from typing import Union
import pandas as pd
import torch
import os
import spacy

from audiotextspeakerchangedetect.SpeakerChangeDetection.speaker_change_detection_main_function import run_speaker_change_detection_models

def run_speaker_change_detection_models_function(audio_file_input_path, audio_file_input_name, min_speakers, max_speakers,
                                   whisper_output_path, whisper_output_file_name, detection_models,
                                   detection_output_path, hf_access_token,
                                   llama2_model_path, pyannote_model_path=None,
                                   device: Union[str, torch.device]=None,
                                   detection_llama2_output_path=None, temp_output_path=None):
    '''
    The main function to choose and run models to identify speaker change detections of an input
    audio file from each of models

    :param audio_file_input_path: A path which contains an input audio file
    :type audio_file_input_path: str
    :param audio_file_input_name: A audio file name containing the file type
    :type audio_file_input_name: str
    :param min_speakers: The minimal number of speakers in the input audio file
    :type: min_speakers: int
    :param max_speakers: The maximal number of speakers in the input audio file
    :type: max_speakers: int
    :param whisper_output_path: A path where a Whisper transcription output csv file is saved
    :type whisper_output_path: str
    :param whisper_output_file_name: A Whisper transcription output csv file name ending with .csv
    :type: whisper_output_file_name: str
    :param detection_models: A list of names of speaker change detection models to be run
    :type detection_models: list
    :param detection_output_path: A path to save the speaker change detection output in csv file
    :type detection_output_path: str
    :param hf_access_token: Access token to HuggingFace
    :type hf_access_token: str
    :param llama2_model_path: A path where the Llama2 model files are saved
    :type llama2_model_path: str
    :param pyannote_model_path: A path where the Pyannote model files are saved, default to None
    :type pyannote_model_path: str, optional
    :param device:Device type to run the model, defaults to None so GPU would be automatically
    used if it is available
    :type: str or torch.device, optional
    :param detection_llama2_output_path: A path where the pre-run Llama2 speaker change detection output in csv file
    is saved if exists, default to None
    :type detection_llama2_output_path: str, optional
    :param temp_output_path: A path to save the current run of Llama2 speaker change detection output
    to avoid future rerunning, default to None
    :type temp_output_path: str, optional
    :return: None
    :rtype: None
    '''

    whisper_df = run_speaker_change_detection_models(audio_file_input_path, audio_file_input_name, min_speakers, max_speakers,
                                   whisper_output_path, whisper_output_file_name, detection_models,
                                   detection_output_path, hf_access_token,
                                   llama2_model_path, pyannote_model_path,
                                   device,
                                   detection_llama2_output_path, temp_output_path)
    return whisper_df
