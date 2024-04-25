import os
import pandas as pd

from pyannote.core import Annotation, Timeline, Segment

labelled_data_path = '/Users/jf3375/Desktop/evaluation_data/VoxConverse/test_csv'
csv_filename = 'rmvsh.csv'
labelled_df = pd.read_csv(os.path.join(labelled_data_path, csv_filename))

num_of_speakers = len(labelled_df['speaker'].unique())
speaking_file_len = labelled_df['duration'].sum()


# Parse Inputs to Data Structures in Metrics Module
labelled_df['end'] = labelled_df['bgn'] + labelled_df['duration']
labels_segments = Timeline()
labels_annotation = Annotation()

# Append pseudo last row with speaker  col Tto deal with the last row exception
# If the real last row speaker change is FALSE, then merge all false speaker segments including the real last row together
# If the real last row speaker change is TRUE, then the real last row itself is also the independent segment
labelled_df.loc[len(labelled_df)] = labelled_df.iloc[-1]
labelled_df.loc[len(labelled_df)-1, 'speaker'] = 'random' #pseudo random speaker to ensure the last row get processed

num_speaker_changes = 0
first_row = labelled_df.iloc[0]
prev_speaker = first_row['speaker']
start_segment = first_row['bgn']
end_segment = first_row['end']

for idx, row in labelled_df[['bgn', 'end', 'speaker']].iloc[1:].iterrows():
    speaker = row['speaker']
    if speaker != prev_speaker:
        num_speaker_changes +=1
        time_segment = Segment(start_segment, end_segment)
        labels_segments.add(time_segment)
        labels_annotation[time_segment] = prev_speaker

        #Update all information after the segment is recorded in annotation
        start_segment = row['bgn']
        end_segment = row['end']
        prev_speaker = speaker
    else:
        end_segment = row['end']

proportion_no_speaker_changes = 1 - (num_speaker_changes-1)/(labelled_df.shape[0]-2) #Exclude pseudo row and first row
print(num_of_speakers, speaking_file_len, proportion_no_speaker_changes)
