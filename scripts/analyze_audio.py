#!/usr/bin/env python3
"""Measure audio file properties; does not identify or clone a speaker."""
import argparse
import soundfile as sf
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("audio_path")
args = parser.parse_args()
audio, sr = sf.read(args.audio_path, always_2d=True)
print(f"Duration: {len(audio)/sr:.2f}s")
print(f"Sample rate: {sr} Hz")
print(f"Channels: {audio.shape[1]}")
print(f"Peak: {float(np.max(np.abs(audio))):.4f}")
print(f"RMS: {float(np.sqrt(np.mean(np.square(audio)))):.4f}")
