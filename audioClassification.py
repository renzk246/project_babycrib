import argparse
import time

from tflite_support.task import audio
from tflite_support.task import core
from tflite_support.task import processor

# Global Variable
global classifier, audio_record, tensor_audio
global interval_between_inference, pause_time, last_inference_time

def audio_initialize(model: str, max_results: int, score_threshold: float,
        overlapping_factor: float, num_threads: int, enable_edgetpu: bool):

    global classifier, audio_record, tensor_audio
    global interval_between_inference, pause_time, last_inference_time

    """Continuously run inference on audio data acquired from the device.

      Args:
        model: Name of the TFLite audio classification model.
        max_results: Maximum number of classification results to display.
        score_threshold: The score threshold of classification results.
        overlapping_factor: Target overlapping between adjacent inferences.
        num_threads: Number of CPU threads to run the model.
        enable_edgetpu: Whether to run the model on EdgeTPU.
    """

    if (overlapping_factor <= 0) or (overlapping_factor >= 1.0):
        raise ValueError('Overlapping factor must be between 0 and 1.')

    if (score_threshold < 0) or (score_threshold > 1.0):
        raise ValueError('Score threshold must be between (inclusive) 0 and 1.')

    # Initialize the audio classification model.
    base_options = core.BaseOptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    classification_options = processor.ClassificationOptions(
        max_results=max_results, score_threshold=score_threshold)
    options = audio.AudioClassifierOptions(
        base_options=base_options, classification_options=classification_options)
    classifier = audio.AudioClassifier.create_from_options(options)

    # Initialize the audio recorder and a tensor to store the audio input.
    audio_record = classifier.create_audio_record()
    tensor_audio = classifier.create_input_tensor_audio()

    # We'll try to run inference every interval_between_inference seconds.
    # This is usually half of the model's input length to create an overlapping
    # between incoming audio segments to improve classification accuracy.
    input_length_in_second = float(len(
        tensor_audio.buffer)) / tensor_audio.format.sample_rate
    interval_between_inference = input_length_in_second * (1 - overlapping_factor)
    pause_time = interval_between_inference * 0.1
    last_inference_time = time.time()

    # Start audio recording in the background.
    audio_record.start_recording()

    return

def audio_run(max_results):
    global classifier, audio_record, tensor_audio
    global interval_between_inference, pause_time, last_inference_time

    now = time.time()
    diff = now - last_inference_time
    if diff < interval_between_inference:
        time.sleep(pause_time)
    last_inference_time = now

    # Load the input audio and run classify.
    tensor_audio.load_from_audio_record(audio_record)
    result = classifier.classify(tensor_audio)

    # Return Results as List
    indexes = []
    category_results = []
    score_results = []
    for i in range(max_results):
        indexes.append(result.classifications[0].categories[i].index)
        category_results.append(result.classifications[0].categories[i].category_name)
        score_results.append(result.classifications[0].categories[i].score)

    return indexes, category_results, score_results