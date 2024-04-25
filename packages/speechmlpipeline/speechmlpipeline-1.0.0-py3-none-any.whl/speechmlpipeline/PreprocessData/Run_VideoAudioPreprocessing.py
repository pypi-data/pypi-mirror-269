'''
Codes to Run Video/Audio for ML Models Inputs
python xx.py
'''

#!/usr/bin/env python
# coding: utf-8
import os
import shutil
from joblib import Parallel, delayed
from VideoAudioPreprocessing import remove_noise, output_silence_timestamps, cut_video_and_audio_based_on_silence
from moviepy.editor import audio_fileClip

def preprocess_video_audio(input_filename, input_path,
                            output_videoprocessed_path, output_silencets_path,
                            output_cut_path, temp_audio_path,
                            video_filetype = 'mp4', audio_filetype = 'wav',
                            threshold = -60, duration = 1):

        if not input_filename.endswith(video_filetype):
            raise Exception('The input file {} does not have the correct file type'.format(input_filename))

        # Remove Background Noise
        remove_noise(input_filename, input_path, output_videoprocessed_path)

        # Find Silence Parts of Audio and Video
        input_path = output_videoprocessed_path
        output_silence_timestamps(input_filename, input_path, output_silencets_path, threshold, duration)

        # Cut video and audio based on silence timestamps
        input_filename_noft = input_filename.split(".")[0]
        input_silence_filename = "{}.txt".format(input_filename_noft)

        input_processed_video_path = output_videoprocessed_path
        input_silencets_path = output_silencets_path

        cut_video_and_audio_based_on_silence(input_filename_noft, video_filetype, audio_filetype,
                                             input_silence_filename,
                                             input_processed_video_path, input_silencets_path,
                                             output_cut_path, temp_audio_path)
def main():
    input_path = "/Users/jf3375/Desktop/DDSS/Projects/NJFS/audio_speech/data/njfs/input"
    os.chdir(input_path)

    output_videoprocessed_path = "/Users/jf3375/Desktop/DDSS/Projects/NJFS/audio_speech/data/njfs/output_processed"
    output_silencets_path = "/Users/jf3375/Desktop/DDSS/Projects/NJFS/audio_speech/data/njfs/silence_timestamps"
    output_cut_path = '/Users/jf3375/Desktop/DDSS/Projects/NJFS/audio_speech/data/njfs/output_cut'
    temp_audio_path = '/Users/jf3375/Desktop/DDSS/Projects/NJFS/audio_speech/data/njfs/temp'

    video_filetype = 'mp4'
    audio_filetype = 'wav'

    for input_filename in os.listdir(input_path):
        input_filename_noft = input_filename.split('.')[0]
        try:
            preprocess_video_audio(input_filename, input_path,
                                                output_videoprocessed_path, output_silencets_path,
                                                output_cut_path, temp_audio_path,
                                                video_filetype = 'mp4', audio_filetype = 'wav',
                                                threshold = -60, duration = 1)
        except:
            # corrupted file or built-in moviepy bug: copy original files directly
            input_file = "{}/{}.{}".format(input_path, input_filename_noft, video_filetype)
            output_audio_file = "{}/audio/{}.{}".format(output_cut_path, input_filename_noft, audio_filetype)
            output_video_file = "{}/video/{}.{}".format(output_cut_path, input_filename_noft, video_filetype)
            audio = audio_fileClip(input_file)
            # If the file not corrupted, output audio file
            audio.write_audio_file(output_audio_file)
            # If the file not corrupted, copy video file
            print('file not corrupted')
            shutil.copyfile(input_file, output_video_file)

if __name__ == '__main__':
    main()