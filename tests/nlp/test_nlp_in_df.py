import os
import unittest
import pandas as pd
from dotenv import load_dotenv
from pandas.testing import assert_frame_equal

from hugging_py_face.nlp import NLP

load_dotenv()


class TestNLPInDF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nlp = NLP(os.environ.get("API_KEY"))

    def test_fill_mask_in_df(self):
        texts = ["The answer to the universe is [MASK]."]
        df = pd.DataFrame(texts, columns=['texts'])

        assert_frame_equal(
            self.nlp.fill_mask_in_df(df, 'texts'),
            pd.DataFrame(
                {
                    "texts": texts,
                    "predictions": ["the answer to the universe is no."],
                }
            ),
        )

    def test_summarize_in_df(self):
        texts = ["The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."]
        df = pd.DataFrame(texts, columns=['texts'])

        assert_frame_equal(
            self.nlp.summarization_in_df(df, 'texts'),
            pd.DataFrame(
                {
                    "texts": texts,
                    "predictions": ["The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world."],
                }
            ),
        )

    def test_question_answering_in_df(self):
        questions = ["What's my name?"]
        contexts = ["My name is Clara and I live in Berkeley"]
        df = pd.DataFrame({
            "questions": questions,
            "contexts": contexts
        })

        assert_frame_equal(
            self.nlp.question_answering_in_df(df, 'questions', 'contexts'),
            pd.DataFrame(
                {
                    "questions": questions,
                    "contexts": contexts,
                    "predictions": ["Clara"],
                }
            ),
        )

    def test_sentence_similarity_in_df(self):
        source_sentences = ["That is a happy person"]
        sentences = ["That is a happy dog"]

        df = pd.DataFrame({
            "source_sentences": source_sentences,
            "sentences": sentences
        })

        assert_frame_equal(
            self.nlp.sentence_similarity_in_df(df, 'source_sentences', 'sentences'),
            pd.DataFrame(
                {
                    "source_sentences": source_sentences,
                    "sentences": sentences,
                    "predictions": [0.6945773363113403],
                }
            ),
        )

    def test_text_classification_in_df(self):
        texts = ["I like you. I love you", "I don't like you. I hate you"]
        df = pd.DataFrame(texts, columns=['texts'])

        assert_frame_equal(
            self.nlp.text_classification_in_df(df, 'texts'),
            pd.DataFrame(
                {
                    "texts": texts,
                    "predictions": ["POSITIVE", "NEGATIVE"],
                }
            ),
        )

    def test_text_generation_in_df(self):
        texts = ["The answer to the universe is"]
        df = pd.DataFrame(texts, columns=['texts'])

        assert_frame_equal(
            self.nlp.text_generation_in_df(df, 'texts'),
            pd.DataFrame(
                {
                    "texts": texts,
                    "predictions": ["The answer to the universe is that we find the Universe, a very large, unchanging, infinitely intricate, incredibly complex place that could not have been created by God in the first place. We'll explore this in more detail at the end of this"],
                }
            ),
        )

    def test_zero_shot_classification_in_df(self):
        texts = ["Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!"]
        df = pd.DataFrame(texts, columns=['texts'])

        candidate_labels = ["refund", "legal", "faq"]

        assert_frame_equal(
            self.nlp.zero_shot_classification_in_df(df, 'texts', candidate_labels),
            pd.DataFrame(
                {
                    "texts": texts,
                    "predictions": ["refund"],
                }
            ),
        )
