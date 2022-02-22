import os
import io
import onnxruntime
import torch
import numpy as np
import time
import json
from TTS.utils.synthesizer import Synthesizer
from TTS.tts.utils.synthesis import synthesis, trim_silence

# if env not set
if "TTS_MODEL_FILE" not in os.environ:
    DIR = "C:/YainTTS/models"
    try:
        models = next(os.walk(DIR))[1][0]
    except:
        print("모델이 설치가 되어있지 않아 실행할 수 없습니다.")
        exit(1)

    os.environ['TTS_MODEL_FILE']="/".join([DIR,models,'glowtts-v2/best_model.pth.tar'])
    os.environ['TTS_MODEL_CONFIG']="/".join([DIR,models,'glowtts-v2/config.json'])
    os.environ['VOCODER_MODEL_FILE']="/".join([DIR,models,'hifigan-v2/best_model.pth.tar'])
    os.environ['VOCODER_MODEL_CONFIG']="/".join([DIR,models,'hifigan-v2/config.json'])

synthesizer = Synthesizer(
    os.environ['TTS_MODEL_FILE'],
    os.environ['TTS_MODEL_CONFIG'],
    None,
    os.environ['VOCODER_MODEL_FILE'],
    os.environ['VOCODER_MODEL_CONFIG'],
    None,
    None,
    False,
)

def synthesize(text):
    synthesizer = Synthesizer(
    os.environ['TTS_MODEL_FILE'],
    os.environ['TTS_MODEL_CONFIG'],
    None,
    os.environ['VOCODER_MODEL_FILE'],
    os.environ['VOCODER_MODEL_CONFIG'],
    None,
    None,
    )
    wavs = synthesizer.tts(text, None, None)
    out = io.BytesIO()
    synthesizer.save_wav(wavs, out)
    return out