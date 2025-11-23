import subprocess
import struct
import json

SAMPLING_RATE = 10

# Extract audio data
ffmpeg_cmd = [
    'ffmpeg', '-y', '-i', '../public/hsk5aworkbook01-1.mp3',
    '-ac', '1',
    '-filter:a', f'aresample={SAMPLING_RATE}',
    '-map', '0:a',
    '-c:a', 'pcm_s16le',
    '-f', 's16le',
    '-'
]

result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)

# Convert binary data to list of integers
audio_data = [x[0] for x in struct.iter_unpack('<h', result.stdout)]

print(f"Samples: {len(audio_data)}")
print(f"Duration: {len(audio_data)/SAMPLING_RATE:.2f} seconds")

# Save as JSON
with open('waveform.json', 'w') as f:
    json.dump({
        'samples': audio_data,
        'sample_rate': SAMPLING_RATE,
        'length': len(audio_data)
    }, f)

print("Saved to waveform.json")

# Or just work with audio_data list directly
# print(audio_data[:10])  # First 10 samples
