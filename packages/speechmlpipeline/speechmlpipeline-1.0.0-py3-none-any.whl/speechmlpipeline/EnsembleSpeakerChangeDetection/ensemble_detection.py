import os
import pandas as pd

from audiotextspeakerchangedetect.EnsembleSpeakerChangeDetection.ensemble_detection import ensemble_detection

def ensemble_detection_function(detection_file_input_path, detection_file_input_name, ensemble_output_path,
                       ensemble_voting = ['majority', 'unanimity']):
    '''
    The main function to build an ensemble model of speaker change detection by using both audio and textual features.
    Specifically, the ensemble model is built by aggregating predictions from various detection models
    (except for the NLP rule-based model) using the input ensemble voting method.
    Then, the final prediction of the ensemble model is corrected by using results from the NLP rule-based model.

    :param detection_file_input_path: A path where the speaker change detection output in csv file is saved
    :type detection_file_input_path: str
    :param detection_file_input_name: A speaker change detection output csv file name ending with .csv
    :type detection_file_input_name: str
    :param ensemble_output_path: A path to save the ensemble detection output in csv file
    :type ensemble_output_path: str
    :param ensemble_voting: A list of voting methods to be used to build the final ensemble model
    :type ensemble_voting: list
    :return: None
    :rtype: None
    '''
    detection_csv = ensemble_detection(detection_file_input_path, detection_file_input_name, ensemble_output_path, ensemble_voting)
    return detection_csv

