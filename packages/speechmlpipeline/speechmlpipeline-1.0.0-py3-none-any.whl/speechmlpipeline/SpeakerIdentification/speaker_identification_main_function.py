import os
import pandas as pd
from speechbrain.pretrained import SpeakerRecognition
from pydub import AudioSegment

from speechmlpipeline.Helpers.helpers import map_notsure_to_false, map_string_to_bool

def run_speaker_identification_model_function(detection_file_input_path, detection_file_input_name,
                                     audio_speaker_file_input_path, audio_file_input_path,
                                     verification_model_path, speaker_change_col, verification_score_threshold,
                                     identification_output_path, temp_output_path):
    '''
    The main function to run Speechbrain verification model to identify a speaker for each segment in the input file by comparing
    similarities between that segment and the input verified audio file of each speaker

    :param detection_file_input_path: A path where the speaker change detection output in csv file is saved
    :type detection_file_input_path: str
    :param detection_file_input_name: A speaker change detection output csv file name ending with .csv
    :type detection_file_input_name: str
    :param audio_speaker_file_input_path:  A path which contains a verified audio file of each speaker
    :type audio_speaker_file_input_path: str
    :param audio_file_input_path: A path which contains an input audio file
    :type audio_file_input_path: str
    :param verification_model_path: A path where the speaker verification model files are saved, default to None
    :type verification_model_path: str
    :param speaker_change_col: A column name in the detection output csv file which specifies which speaker
    change detection model result is used for speaker identification
    :type speaker_change_col: str
    :param verification_score_threshold: A score threshold in which the speaker would be identified as "OTHERS"
    if the verification score is below this threshold，ranging from negative value to 1
    :type verification_score_threshold: str
    :param identification_output_path: A path to save the speaker identification output in csv file
    :type identification_output_path: str
    :param temp_output_path: A path to save the temporary cut audio file of each segment
    :type temp_output_path: str
    '''

    filename_noftype = detection_file_input_name.split('.')[0]

    # List speakers and their related sounds files
    sound_speaker_files = [filename for filename in sorted(os.listdir(audio_speaker_file_input_path)) if filename.endswith('WAV')]
    speakers = [filename.split('.')[0] for filename in sound_speaker_files]
    detection_csv = pd.read_csv(os.path.join(detection_file_input_path, detection_file_input_name))

    # Process Diarization Outputs
    if speaker_change_col in ['speaker_change_llama2', 'speaker_change_nlp']:
        # Fill Missing Values by FALSE: would ignore llama2 output if output is None
        # Convert string/object type to bool type; Could not directly use astype(bool): 'False' would become True
        detection_csv[speaker_change_col] = detection_csv[speaker_change_col].apply(map_notsure_to_false).apply(map_string_to_bool)

    # Would identify verification result only if the score is above threshold
    # Import speaker identification models
    if os.path.exists(verification_model_path):
        verification_model = SpeakerRecognition.from_hparams(source = verification_model_path)
    else:
        raise Exception('Please download the model first by following readme')

    # Import full_audio
    full_audio = AudioSegment.from_wav(os.path.join(audio_file_input_path, '{}.WAV'.format(filename_noftype)))

    # Speaker Identification for each audio segment
    speaker_identify_allsegments = []
    start_segment = detection_csv.iloc[0]['start']
    end_segment = detection_csv.iloc[0]['end']
    start_row_idx = 0
    end_row_idx = 0

    # Append pseudo last row with speaker change col TRUE to deal with the last row exception
    # If the real final row is FALSE, then merge all false speaker segments including the last row together
    # If the real final row is TRUE, then the last row itself is also the independent segment
    detection_csv.loc[len(detection_csv)] = detection_csv.iloc[-1]
    # New row is appended
    detection_csv.loc[len(detection_csv)-1, speaker_change_col] = True

    for current_row_idx, row in detection_csv.iterrows():
        if current_row_idx == 0: # No speaker changes information of the first row
            continue
        # Deal with the last row condition
        # If speaker_change = True, merge previous false speaker change segments together
        if row[speaker_change_col]:
            audio_segment = full_audio[start_segment * 1e3:end_segment * 1e3]
            audio_segment.export(os.path.join(temp_output_path, 'audio_segment_temp.wav'), format="wav")

            speaker_scores_segment = {}
            for idx, sound_speaker_file in enumerate(sound_speaker_files):
                score, _ = verification_model.verify_files(os.path.join(audio_speaker_file_input_path, sound_speaker_file),
                                                           os.path.join(temp_output_path, 'audio_segment_temp.wav'))
                speaker_scores_segment[speakers[idx]] = score.item()

            # Find the optimal speaker
            speaker_identify  = max(speaker_scores_segment, key = speaker_scores_segment.get)
            # print(speaker_scores_segment)
            # print(speaker_identify)
            # print(current_row_idx, row[speaker_change_col])
            # print(start_row_idx, end_row_idx)

            # Would identify speaker as OTHERS if the score is below the threshold such as 0
            if speaker_scores_segment[speaker_identify] < verification_score_threshold:
                speaker_identify = 'OTHERS'

            speaker_identify_allsegments.extend([speaker_identify]*(end_row_idx-start_row_idx+1))
            start_segment = row['start']
            end_segment = row['end']
            start_row_idx = current_row_idx
            end_row_idx = current_row_idx
        else:
            end_row_idx = current_row_idx
            end_segment = row['end']


    speaker_identify_allsegments.append('random_last_row')
    detection_csv['speakers_predict'] = speaker_identify_allsegments

    # Remove previous append last row and return identification results
    detection_csv_output = detection_csv.iloc[:-1]
    detection_csv_output.to_csv(os.path.join(identification_output_path, detection_file_input_name), index = False)
    return detection_csv_output