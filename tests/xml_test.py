import os
import unittest
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from utils.xml_parser import extract_alignments, align_sentences
class TestExtractAlignments(unittest.TestCase):

    def test_extract_alignments(self):
        path_to_file = 'data/test.xml'
        eng_first = True
        alignment_dict = extract_alignments(path_to_file, eng_first)

        expected_output = {0: 1, 0: 1, 2: 4, 3: 5}
        
        self.assertEqual(alignment_dict, expected_output)


class TestAccumulateSentences(unittest.TestCase):

    def setUp(self):
        self.accumulator_dict = {
            0: {"eng": "Hello", "lug": "Jeebale"},
            4: {"eng": "My Lord !", "lug": "Mukama Wange !"},
        }
        self.eng_sentences_dict = {
            0: "Hello",
            1: "How are you?",
            2: "What is your name?"
        }
        self.other_sentences_dict = {
            10: "Habari",
            11: "Habari yako?",
            12: "Jina lako nani?"
        }
        self.alignment_dict = {
            0: 10,
            1: 11,
            2: 12
        }
        self.other_language = "swa"
        self.minimum_length = 3


    def test_align_sentences(self):
        # Define input values
        
        # Call the function
        result = align_sentences(
            self.accumulator_dict, self.eng_sentences_dict, self.other_sentences_dict, self.alignment_dict, self.other_language, self.minimum_length)

        # Define expected output
        expected_output = {
            0: {"eng": "Hello", "swa": "Habari", "lug": "Jeebale"},
            1: {"eng": "How are you?", "swa": "Habari yako?"},
            2: {"eng": "What is your name?", "swa": "Jina lako nani?"},
            4: {"eng": "My Lord !", "lug": "Mukama Wange !"},

        }

        # Check the output is as expected
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
