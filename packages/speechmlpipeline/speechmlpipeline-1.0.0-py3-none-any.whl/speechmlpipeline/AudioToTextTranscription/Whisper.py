'''
Functions to Apply Whisper for Audio-Text Transcription and Output Results in CSV to Create Training Data
'''

#!/usr/bin/env python
# coding: utf-8
import os
import whisper
import pandas as pd
import torch
from typing import Union

def whisper_transcription(audio_file_input_path, audio_file_input_name,
                          whisper_model_path, whisper_output_path, device: Union[str, torch.device]=None):

    audio_file_input_name_noftype = audio_file_input_name.split('.')[0]
    whisper_model = whisper.load_model(name = whisper_model_path, device=device)

    # Translate text into Whisper
    result = whisper_model.transcribe(os.path.join(audio_file_input_path, audio_file_input_name))
    segment_len = len(result['segments'])
    transcribe_df = pd.DataFrame()
    start_list = [0] * segment_len
    end_list = [0] * segment_len
    text_list = [0] * segment_len

    for idx, segment in enumerate(result['segments']):
        start_list[idx], end_list[idx], text_list[idx] = segment['start'], segment['end'], segment['text']

    transcribe_df['start'], transcribe_df['end'], transcribe_df['text'] = start_list, end_list, text_list
    transcribe_df['file_name'] = audio_file_input_name_noftype
    transcribe_df['speaker'] = ''

    # Remove leading and trailing whitespaces from whisper outputs
    transcribe_df['text'] = transcribe_df['text'].apply(lambda x: x.strip())

    transcribe_df.to_csv(os.path.join(whisper_output_path, '{}.csv'.format(audio_file_input_name_noftype)), index=False)
    return transcribe_df

