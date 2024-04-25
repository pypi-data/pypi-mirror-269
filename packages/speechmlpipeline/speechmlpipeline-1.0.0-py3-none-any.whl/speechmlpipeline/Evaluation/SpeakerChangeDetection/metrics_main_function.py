'''
Calculate precision, recall, precisionrecallfscore,
coverage, purity, and coveragepurityfscore using Pyannote
Drop missing values before calculating the evaluation metric
'''

import os
import pandas as pd
from numpy import NaN

from pyannote.core import Annotation, Timeline, Segment
from pyannote.metrics.segmentation import SegmentationPrecision, SegmentationRecall, \
    SegmentationCoverage, SegmentationPurity

def map_notsure_to_true(x):
    if x == 'NotSure':
        return True
    else:
        return x

def map_string_to_bool(x):
    if type(x) == str: # Check if x is string
        if x.lower() == 'true':
            return True
        elif x.lower() == 'false':
            return False
    else:
        return x

def calculate_detection_metrics(prediction_output_path, labelled_data_path, csv_filename, tolerance=0.5):
    '''
    The function calculates metrics to evaluate the performance of speaker change detection models. The calculated metrics
    are segment precision, segment recall, segment precision recall f1 score,
    segment coverage, segment purity, and segment purity f1 score.

    The function uses the csv files of speaker change detection predictions and true labels to calculate the metrics.
    The speaker change detection predictions csv file should contain start, end, and speaker_change column to indicate
    if speaker change is True or False from the start to the end of every segment.

    The speaker change detection labels csv file should contain bgn, duration, and speaker column (corresponding to the
    standardized rttm format) to indicate each speaker from the bgn of every segment with the duration.

    :param prediction_output_path: A path where the csv file of speaker change detection predictions is saved
    :type prediction_output_path: str
    :param labelled_data_path: A path where the csv file of speaker change detection true labels is saved
    :type labelled_data_path: str
    :param csv_filename: A name of the csv files of speaker change detection predictions and true labels
    :type csv_filename: str
    :param tolerance: The maximum distance between two boundaries of time segments for them to be matched.
    :type tolerance: float
    :return: None
    :rtype: None
    '''
    # Read Prediction and Labelled DF
    prediction_df = pd.read_csv(os.path.join(prediction_output_path, csv_filename))
    labelled_df = pd.read_csv(os.path.join(labelled_data_path, csv_filename))

    # Process Llama2 and NLP Predictions, filling not sure predictions as speaker change as true
    prediction_df['speaker_change_nlp'] = prediction_df['speaker_change_nlp'].apply(map_notsure_to_true).apply(map_string_to_bool)
    prediction_df['speaker_change_llama2'] = prediction_df['speaker_change_llama2'].apply(map_notsure_to_true).apply(map_string_to_bool)

    # Fill the empty silence parts into previous speaker ending as the pyannotate metircs module requires the continous segment
    # Parse Inputs to Data Structures in Metrics Module
    labelled_end_times = list(labelled_df['bgn'])[1:]
    labelled_end_times.append(labelled_df.iloc[-1]['bgn']+labelled_df.iloc[-1]['duration'])
    labelled_df['end'] = labelled_end_times


    prediction_end_times = list(prediction_df['start'])[1:]
    prediction_end_times.append(prediction_df.iloc[-1]['end'])
    prediction_df['end'] = prediction_end_times

    # Initialize Metrics Class
    coverage_score = SegmentationCoverage(tolerance=tolerance)
    purity_score = SegmentationPurity(tolerance=tolerance)
    precision_score = SegmentationPrecision(tolerance=tolerance)
    recall_score = SegmentationRecall(tolerance=tolerance)

    # Initialize Evaluation DataFrame
    evaluation_df = pd.DataFrame()

    # List Six Metrics for Calculation
    metrics_names_list = ['precision', 'recall', 'precision_recall_f1', 'coverage', 'purity', 'coverage_purity_f1']
    evaluation_df['metric_name'] = metrics_names_list


    labels_segments = Timeline()
    labels_annotation = Annotation()

    # Append pseudo last row with speaker col to deal with the last row exception
    # If the real last row speaker change is FALSE, then merge all false speaker segments including the real last row together
    # If the real last row speaker change is TRUE, then the real last row itself is also the independent segment
    labelled_df.loc[len(labelled_df)] = labelled_df.iloc[-1]
    labelled_df.loc[len(labelled_df)-1, 'speaker'] = 'random'  # pseudo random speaker to ensure the last row get processed

    num_speaker_changes = 0
    first_row = labelled_df.iloc[0]
    prev_speaker = first_row['speaker']
    start_segment = first_row['bgn']
    end_segment = first_row['end']

    for idx, row in labelled_df[['bgn', 'end', 'speaker']].iloc[1:].iterrows():
        speaker = row['speaker']
        if speaker != prev_speaker:
            num_speaker_changes += 1
            time_segment = Segment(start_segment, end_segment)
            labels_segments.add(time_segment)
            labels_annotation[time_segment] = prev_speaker

            # Update all information after the segment is recorded in annotation
            start_segment = row['bgn']
            end_segment = row['end']
            prev_speaker = speaker
        else:
            end_segment = row['end']

    #Extract files charactersitics
    npossiblechanges = labelled_df.shape[0]-2 # Exclude pseudo row and first row
    if npossiblechanges == 0: # Labelled df only has one row and one pseudo row, no speaker change at all
        proportion_speaker_changes = 0
    else:
        proportion_speaker_changes = (num_speaker_changes - 1)/(npossiblechanges)
    num_of_speakers = len(labelled_df['speaker'].unique())-1 #Drop random speaker in the end

    # Put file characteristics in a df
    metrics_num = len(metrics_names_list)
    evaluation_df['audio_file_name'] = [csv_filename.split('.')[0]] * metrics_num
    evaluation_df['speaking_len_file'] =[labelled_end_times[-1]] * metrics_num
    evaluation_df['num_of_speakers'] = [num_of_speakers] * metrics_num
    evaluation_df['num_speaker_changes'] = [num_speaker_changes - 1] * metrics_num
    evaluation_df['proportion_speaker_changes'] = [proportion_speaker_changes] * metrics_num

    # Append pseudo last row with speaker change col TRUE to deal with the last row exception
    # If the real last row is FALSE, then merge all false speaker segments including the real last row together
    # If the real last row is TRUE, then the real last row itself is also the independent segment
    prediction_df.loc[len(prediction_df)] = prediction_df.iloc[-1]

    # Calculate Evaluation Metrics for All Models
    speaker_change_models_cols = [col for col in prediction_df.columns if 'speaker_change' in col and 'true' not in col]
    for speaker_change_col in speaker_change_models_cols:
        # Update the speaker change column of the model in last row as true
        prediction_df.loc[len(prediction_df) - 1, speaker_change_col] = True

        # Parse Inputs into Data Structures on Metrics Module
        prediction_segments = Timeline()
        start_segment = prediction_df.iloc[0]['start']
        end_segment = prediction_df.iloc[0]['end']

        for current_row_idx, row in prediction_df.iterrows():
            if current_row_idx == 0:  # No speaker changes information of the first row
                continue
            # If speaker_change = True, merge previous false speaker change segments together
            if row[speaker_change_col]:
                prediction_segments.add(Segment(start_segment, end_segment))
                start_segment = row['start']
                end_segment = row['end']
            else:
                end_segment = row['end']
        # Fix the bug of PyAnnote which calculates the prediction as 1 when there is zero speaker change prediction
        if sum(prediction_df[speaker_change_col]) == 2: #The first and last rows have two pseudo true speaker changes; zero indeed speaker change prediction
            precision = NaN
        else:
            precision = precision_score(labels_segments, prediction_segments)
        # Fix the bug of PyAnnote which calculates recall when zero speaker change happens
        if num_speaker_changes == 1: #only has one pseudo speaker change, zero real speaker change
            recall = NaN
        else:
            recall = recall_score(labels_segments, prediction_segments)
        if (precision+recall != 0):
            precision_recall_f1 = 2 * precision * recall / (precision + recall)
        else:
            precision_recall_f1 = NaN
        coverage = coverage_score(labels_annotation, prediction_segments)
        purity = purity_score(labels_annotation, prediction_segments)
        if (coverage+purity != 0):
            coverage_purity_f1 = 2 * coverage * purity / (coverage + purity)
        else:
            coverage_purity_f1 = NaN
        evaluation_df[speaker_change_col] = [precision, recall, precision_recall_f1, coverage, purity,
                                             coverage_purity_f1]
    return evaluation_df

# Test Codes
# prediction_output_path = '/Users/jf3375/Downloads'
# labelled_data_path = '/Users/jf3375/Desktop/evaluation_data/VoxConverse/test_csv'
# csv_filename = 'rmvsh.csv'
# tolerance = 0
# evaluation_df, prediction_df, labelled_df, labels_annotation, prediction_segments = calculate_detection_metrics(prediction_output_path, labelled_data_path, csv_filename, tolerance=0.5)
#
# coverage_score = SegmentationCoverage(tolerance=tolerance)
# purity_score = SegmentationPurity(tolerance=tolerance)
# precision_score = SegmentationPrecision(tolerance=tolerance)
# recall_score = SegmentationRecall(tolerance=tolerance)
#
# print(precision_score(labels_annotation, prediction_segments))
# print(recall_score(labels_annotation, prediction_segments))
# print(coverage_score(labels_annotation, prediction_segments))
# print(purity_score(labels_annotation, prediction_segments))