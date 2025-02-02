import os
import unittest
from dotenv import load_dotenv

from hugging_py_face.audio_processing import AudioProcessing

load_dotenv()


class TestAudioProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ap = AudioProcessing(os.environ.get("API_KEY"))
        cls.inputs = os.path.join(os.path.dirname(__file__), '..', 'resources', 'amused.wav')

    def test_speech_recognition(self):
        self.assertEqual(
            self.ap.speech_recognition(self.inputs),
            {
                'text': 'I AM PLAYING A SINGLE HAND IN IT LOOKS LIKE A LOSING GAME'
            },
        )

    def test_audio_classification(self):
        self.assertEqual(
            self.ap.audio_classification(self.inputs),
            [
                {'label': 'hap', 'score': 0.996896505355835},
                {'label': 'sad', 'score': 0.002958094235509634},
                {'label': 'neu', 'score': 9.905487240757793e-05},
                {'label': 'ang', 'score': 4.624627763405442e-05}
            ],
        )