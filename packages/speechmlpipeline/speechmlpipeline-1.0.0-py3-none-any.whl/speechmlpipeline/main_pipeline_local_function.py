from typing import TypedDict, Union, Optional
import torch

from speechmlpipeline.DownloadModels.download_models_main_function import download_models_main_function
from speechmlpipeline.AudioToTextTranscription.Whispertimestamped import whisper_transcription
from speechmlpipeline.SpeakerChangeDetection.speaker_change_detection_main_function import run_speaker_change_detection_models_function
from speechmlpipeline.EnsembleSpeakerChangeDetection.ensemble_detection import ensemble_detection_function
from speechmlpipeline.SpeakerIdentification.speaker_identification_main_function import run_speaker_identification_model_function

# Create new class types to run the whole pipeline
class DownloadModelsInputs(TypedDict):
    '''
    A class to specify inputs to download_models_main_function

    :param download_model_path: The path to save all the downloaded models files
    :type download_model_path: str
    :param models_list: The list of the names of the models to be downloaded
    :type models_list: str
    :param hf_access_token: Access token to HuggingFace
    :type hf_access_token: str
    '''
    download_model_path: str
    models_list: list
    hf_access_token: str

class TranscriptionInputs(TypedDict):
    '''
    A class to specify inputs to whisper_transcription function

    :param audio_file_input_path: A path which contains the audio file
    :type audio_file_input_path: str
    :param audio_file_input_name: A audio file name containing the file type
    :type audio_file_input_name: str
    :param whisper_model_path: A path where the Whisper model files are saved
    :type whisper_model_path: str
    :param whisper_output_path: A path to save the csv file of transcription outputs
    :type whisper_output_path: str
    :param device: Device type to run the model; If the type is None, GPU would be automatically used if it is available
    :type: str or torch.device or None
    :param only_run_in_english: True or False to Indicate if Whisper would only be run when
    the identified langauge in the audio file is English
    :type: bool
    '''
    audio_file_input_path: str
    audio_file_input_name: str
    whisper_model_path: str
    whisper_output_path: str
    device: Union[str, torch.device, None]
    only_run_in_english: bool

class SpeakerChangeDetectionInputs(TypedDict):
    '''
    A class to specify inputs to speaker_change_detection_main_function function

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
    :param pyannote_model_path: A path where the Pyannote model files are saved
    :type pyannote_model_path: str or None
    :param device: Device type to run the model
    used if it is available
    :type: str or torch.device or None
    :param detection_llama2_output_path: A path where the pre-run Llama2 speaker change detection output in csv file
    is saved if exists
    :type detection_llama2_output_path: str or None
    :param temp_output_path: A path to save the current run of Llama2 speaker change detection output
    to avoid future rerunning
    :type temp_output_path: str or None
    :return: None
    :rtype: None
    '''
    audio_file_input_path: str
    audio_file_input_name: str
    min_speakers: int
    max_speakers: int
    whisper_output_path: str
    whisper_output_file_name: str
    detection_models: list
    detection_output_path: str
    hf_access_token: str
    llama2_model_path: str
    pyannote_model_path: Union[str, None]
    device: Union[str, torch.device, None]
    detection_llama2_output_path: Union[str, None]
    temp_output_path: Union[str, None]

class EnsembleDetectionInputs(TypedDict):
    '''
    A class to specify inputs to ensemble_detection function

    :param detection_file_input_path: A path where the speaker change detection output in csv file is saved
    :type detection_file_input_path: str
    :param detection_file_input_name: A speaker change detection output csv file name ending with .csv
    :type detection_file_input_name: str
    :param ensemble_output_path: A path to save the ensemble detection output in csv file
    :type ensemble_output_path: str
    :param ensemble_voting: A list of voting methods to be used to build the final ensemble model
    :type ensemble_voting: list
    '''
    detection_file_input_path: str
    detection_file_input_name: str
    ensemble_output_path: str
    ensemble_voting: list

class SpeakerIdentificationInputs(TypedDict):
    '''
    A class to specify inputs to run_speaker_identification_model function

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
    detection_file_input_path: str
    detection_file_input_name: str
    audio_speaker_file_input_path: str
    audio_file_input_path: str
    verification_model_path: str
    speaker_change_col: str
    verification_score_threshold: float
    identification_output_path: str
    temp_output_path: str
def run_speech_ml_pipeline(download: Optional[DownloadModelsInputs] = None,
                           transcription: Optional[TranscriptionInputs] = None,
                           speakerchangedetection: Optional[SpeakerChangeDetectionInputs] = None,
                           ensembledetection: Optional[EnsembleDetectionInputs] = None,
                           speakeridentification: Optional[SpeakerIdentificationInputs] = None):
    """The main function to run the whole speech machine learning pipeline to get the transcription outputs with speaker labels
    or run any individual step or steps of the pipeline

    For the function usage exmples, please refer to run_main_pipeline_local_function.py
    For the inputs classes documentation, please refer to their doc strings at the top of this file

    :param download: DownloadModelsInputs Class to specify inputs to download all models to use them offline
    :type download: Optional[DownloadModelsInputs]
    :param transcription: TranscriptionInputs Class to specify inputs to run OpenAI Whisper for Audio-to-Text Transcription with Timestamps Adjustment
    :type transcription: Optional[TranscriptionInputs]
    :param speakerchangedetection: SpeakerChangeDetectionInputs Class to specify inputs to run various models including
    PyAnnote Model, Spectral Clustering, Llama2, and NLP Rule-Based Analysis for Speaker Change Detection
    :type speakerchangedetection: Optional[SpeakerChangeDetectionInputs]
    :param ensembledetection: EnsembleDetectionInputs Class to specify inputs to build an Ensemble Model of Speaker
    Change Detection by considering both audio and textual features
    :type ensembledetection: Optional[EnsembleDetectionInputs]
    :param speakeridentification: SpeakerIdentificationInputs Class to specify inputs to run Speechbrain Verification Model for Speaker Identification
    :type speakeridentification: Optional[SpeakerIdentificationInputs]
    """
    # Download Model
    if download:
        download_models_main_function(download["download_model_path"],
                                      download["models_list"],
                                      download["hf_access_token"])
        print('Finish Download Model')

    # Run Whisper Transcription with TimeStamps Correction
    if transcription:
        whisper_transcription(transcription['audio_file_input_path'],
                              transcription['audio_file_input_name'],
                              transcription['whisper_model_path'],
                              transcription['whisper_output_path'],
                              transcription['device'])
        print('Finish Transcription')

    # Run Speaker Change Detection
    if speakerchangedetection:
        run_speaker_change_detection_models_function(
            speakerchangedetection['audio_file_input_path'],
            speakerchangedetection['audio_file_input_name'],
            speakerchangedetection['min_speakers'],
            speakerchangedetection['max_speakers'],
            speakerchangedetection['whisper_output_path'],
            speakerchangedetection['whisper_output_file_name'],
            speakerchangedetection['detection_models'],
            speakerchangedetection['detection_output_path'],
            speakerchangedetection['hf_access_token'],
            speakerchangedetection['llama2_model_path'],
            speakerchangedetection['pyannote_model_path'],
            speakerchangedetection['device'],
            speakerchangedetection['detection_llama2_output_path'],
            speakerchangedetection['temp_output_path'])
        print('Finish Detection')

    # Ensemble Detection
    if ensembledetection:
        ensemble_detection_function(ensembledetection['detection_file_input_path'],
                           ensembledetection['detection_file_input_name'],
                           ensembledetection['ensemble_output_path'],
                           ensembledetection['ensemble_voting'])
        print('Finish Ensemble Detection')

    # Run Speaker Identification
    if speakeridentification:
        run_speaker_identification_model_function(
            speakeridentification['detection_file_input_path'],
            speakeridentification['detection_file_input_name'],
            speakeridentification['audio_speaker_file_input_path'],
            speakeridentification['audio_file_input_path'],
            speakeridentification['verification_model_path'],
            speakeridentification['speaker_change_col'],
            speakeridentification['verification_score_threshold'],
            speakeridentification['identification_output_path'],
            speakeridentification['temp_output_path'])
        print('Finish Identification')

