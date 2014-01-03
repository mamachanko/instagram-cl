import json
import os

test_dir = os.path.dirname(os.path.abspath(__file__))
media_sample_file = os.path.join(test_dir, 'media_sample.json')
with open(media_sample_file, 'r') as f:
    media_sample = json.load(f)
