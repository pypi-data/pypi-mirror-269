'''
Functions to Apply Whisper with Improved TimeStamped Accuracy for Audio-Text Transcription and Output Results in CSV to Create Training Data
'''

#!/usr/bin/env python
# coding: utf-8
import os
import whisper_timestamped as whisper
import pandas as pd
import torch
from typing import Union

def whisper_transcription(audio_file_input_path, audio_file_input_name, whisper_model_path, whisper_output_path,
                          device: Union[str, torch.device]=None,
                          only_run_in_english = True):
    '''
    The main function to run OpenAI Whisper to get transcription texts with timestamp adjustments
    :param audio_file_input_path: A path which contains an input audio file
    :type audio_file_input_path: str
    :param audio_file_input_name: A audio file name containing the file type
    :type audio_file_input_name: str
    :param whisper_model_path: A path where the Whisper model files are saved
    :type whisper_model_path: str
    :param whisper_output_path: A path to save the transcription output in csv file
    :type whisper_output_path: str
    :param device: Device type to run the model, defaults to None so GPU would be automatically used if it is available
    :type: str or torch.device, optional
    :param only_run_in_english: True or False to Indicate if Whisper would only be run when
    the identified langauge in the audio file is English, defaults to True
    :type: bool, optional
    :return: None
    :rtype: None
    '''
    audio_file_input_name_noftype = audio_file_input_name.split('.')[0]

    if not device:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    audio = whisper.load_audio(os.path.join(audio_file_input_path, audio_file_input_name))
    whisper_model = whisper.load_model(whisper_model_path, device=device) # Could not use predownloaded Whisper model for accurate timestamp

    # detect the spoken language
    mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio)).to(device)
    _, probs = whisper_model.detect_language(mel)
    detected_language = max(probs, key=probs.get)

    if detected_language != 'en' and only_run_in_english:
        print('Langauge is not English. No further processing. Return Dataframe with only Detected Language as Output')
        transcribe_df = pd.DataFrame()
        transcribe_df['language'] = [detected_language]
        transcribe_df.to_csv(os.path.join(whisper_output_path, '{}.csv'.format(audio_file_input_name_noftype)),
                             index=False)
        return
    # Translate text into Whisper
    result = whisper.transcribe(whisper_model, audio, beam_size=5, best_of=5,
                                temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
                                vad = 'auditok', language= detected_language)
    segment_len = len(result['segments'])
    transcribe_df = pd.DataFrame()
    start_list = []
    end_list = []
    text_list = []

    # Process Whisper Outputs
    # Should concat duplicated continuous text columns together
    first_segment = result['segments'][0]
    start_idx, end_idx, prev_text = first_segment['start'], first_segment['end'], first_segment['text']

    for idx, segment in enumerate(result['segments'][1:]):
        if prev_text != segment['text']:
            # output previous same rows into df
            start_list.append(start_idx)
            end_list.append(end_idx)
            text_list.append(prev_text)
            start_idx, end_idx, prev_text = segment['start'], segment['end'], segment['text']
        else:
            end_idx = segment['end']

    # Append last segment to df
    start_list.append(start_idx)
    end_list.append(end_idx)
    text_list.append(prev_text)

    transcribe_df['start'], transcribe_df['end'], transcribe_df['text'] = start_list, end_list, text_list
    transcribe_df['file_name'] = audio_file_input_name_noftype
    transcribe_df['speaker'] = ''
    # Remove leading and trailing whitespaces from whisper outputs
    transcribe_df['text'] = transcribe_df['text'].apply(lambda x: x.strip())
    # Create unique id of whisper segment for later merge
    transcribe_df['segmentid'] = list(range(transcribe_df.shape[0]))
    transcribe_df['language'] = detected_language

    transcribe_df.to_csv(os.path.join(whisper_output_path, '{}.csv'.format(audio_file_input_name_noftype)), index=False)
    return transcribe_df

