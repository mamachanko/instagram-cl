from arrow import Arrow

import json
import os
import re

from instagram_cl.instagram_cl import InstagramMedia


test_dir = os.path.dirname(os.path.abspath(__file__))
media_sample_file = os.path.join(test_dir, 'media_sample.json')
with open(media_sample_file, 'r') as f:
    media_sample = json.load(f)


class TestInstagramMedia:

    def test_stores_username(self):
        instagram_media = InstagramMedia(media_sample)
        assert instagram_media.username == media_sample['user']['username']

    def test_stores_date(self):
        instagram_media = InstagramMedia(media_sample)
        assert instagram_media.created_time == Arrow.utcfromtimestamp(media_sample['created_time'])

    def test_representation(self):
        instagram_media = InstagramMedia(media_sample)
        assert repr(instagram_media) == '<InstagramMedia by @sugardubz created %s>' % instagram_media.created_time.humanize()

