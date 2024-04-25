'''
Sample File to Run the Whole SpeechMLPipeline Without Existing Llama2 output
'''

from main_pipeline_local_function import TranscriptionInputs, SpeakerChangeDetectionInputs, \
    EnsembleDetectionInputs, SpeakerIdentificationInputs, run_speech_ml_pipeline

# Shared Inputs
hf_access_token = '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'
device = None  # if set device = None, by default would use gpu if cuda is available, otherwise use gpu
audio_file_input_path = '/scratch/gpfs/jf3375/modern_family/audio/sample_data'
audio_file_input_name =  'sample_data.WAV'
csv_file_input_name = audio_file_input_name.split('.')[0] + '.csv'
whisper_output_path = '/scratch/gpfs/jf3375/test/output'
detection_output_path = '/scratch/gpfs/jf3375/test/output'

# Transcription Specific Inputs
whisper_model_path = '/scratch/gpfs/jf3375/models/whisper/large-v2.pt'

# Detection Specific Inputs
detection_models =  ['pyannote', 'clustering', 'nlp', 'llama2-70b']
min_speakers = 2
max_speakers = 10
llama2_model_path = '/scratch/gpfs/jf3375/models/llama'
pyannote_model_path = '/scratch/gpfs/jf3375/models/pyannote3.1/Diarization'
detection_llama2_output_path =  None
temp_output_path = '/scratch/gpfs/jf3375/test/temp'

# Ensemble Specific Inputs
ensemble_voting = ['majority', 'unanimity']
ensemble_output_path = '/scratch/gpfs/jf3375/test/output'

# Identification Specific Inputs
audio_speaker_file_input_path = '/scratch/gpfs/jf3375/modern_family/characters_sounds'
verification_model_path = '/scratch/gpfs/jf3375/models/speechbrain'
speaker_change_col = 'speaker_change_ensemble_unanimity'
verification_score_threshold = 0
identification_output_path =  '/scratch/gpfs/jf3375/test/output'

# Pass Inputs into Each Pipeline Class
transcription_inputs = TranscriptionInputs(audio_file_input_path=audio_file_input_path, audio_file_input_name=audio_file_input_name,
                                    whisper_model_path=whisper_model_path, whisper_output_path=whisper_output_path,
                                    device = device)

detection_inputs = SpeakerChangeDetectionInputs(audio_file_input_path=audio_file_input_path, audio_file_input_name=audio_file_input_name,
                                    min_speakers=min_speakers, max_speakers=max_speakers,
                                    whisper_output_path=whisper_output_path, whisper_output_file_name= csv_file_input_name,
                                    detection_models=detection_models,
                                    detection_output_path=detection_output_path,
                                    hf_access_token=hf_access_token,
                                    llama2_model_path=llama2_model_path, pyannote_model_path = pyannote_model_path,
                                    device = device,
                                    detection_llama2_output_path=None,
                                    temp_output_path=temp_output_path)

ensemble_detection_inputs = EnsembleDetectionInputs(detection_file_input_path=detection_output_path,
                                                    detection_file_input_name=csv_file_input_name,
                                                    ensemble_output_path=ensemble_output_path,
                                                    ensemble_voting=ensemble_voting
                                                    )

speaker_identification_inputs = SpeakerIdentificationInputs(detection_file_input_path=detection_output_path,
                                                            detection_file_input_name=csv_file_input_name,
                                                            audio_speaker_file_input_path=audio_speaker_file_input_path,
                                                            audio_file_input_path=audio_file_input_path,
                                                            verification_model_path=verification_model_path,
                                                            speaker_change_col=speaker_change_col,
                                                            verification_score_threshold=verification_score_threshold,
                                                            identification_output_path=identification_output_path,
                                                            temp_output_path=temp_output_path)
# Run SpeechMLPipeline
# Run Whole Pipeline except for Downloading Models
run_speech_ml_pipeline(transcription = transcription_inputs,
                       speakerchangedetection=detection_inputs, ensembledetection=ensemble_detection_inputs,
                       speakeridentification=speaker_identification_inputs)

# Only run one step of pipeline
# run_speech_ml_pipeline(ensembledetection=ensemble_detection_inputs)

# Run two steps of pipeline
# run_speech_ml_pipeline(transcription = transcription_inputs,
#                        speakerchangedetection=detection_inputs)