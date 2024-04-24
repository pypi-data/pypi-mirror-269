#from root of project run:
#python -m unittest tests.test_presentation_processor
#
import unittest
from unittest.mock import patch, mock_open
import json
from presentation.presentation_processor import PresentationProcessor  # Adjust the import according to your file structure

class TestPresentationProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PresentationProcessor()
        self.sample_text = "**Slide Title**:\n- Content line 1\n- Content line 2\n- Image: path/to/image.jpg\n- Caption: Description of the image"
        self.expected_json = json.dumps({
            "slides": [
                {
                    "title": "Slide Title",
                    "content": "Content line 1\nContent line 2\n",
                    "images": [
                        {
                            "path": "path/to/image.jpg",
                            "caption": "Description of the image"
                        }
                    ]
                }
            ]
        }, indent=4)
        self.expected_text = "1. **Slide Title**:\n   - Content line 1\n   - Content line 2\n   - Image: path/to/image.jpg\n   - Caption: Description of the image"

    def test_text_to_json(self):
        result = self.processor.text_to_json(self.sample_text)
        self.assertEqual(json.loads(result), json.loads(self.expected_json))

    def test_json_to_text(self):
        result = self.processor.json_to_text(self.expected_json)
        self.assertEqual(result.strip(), self.expected_text.strip())

    @patch('builtins.open', new_callable=mock_open, read_data="data")
    @patch('os.path.exists')
    def test_read_from_file(self, mock_exists, mocked_open):  # Changed `mock_open` to `mocked_open` to reflect the patched object
        mock_exists.return_value = True
        result = self.processor.read_text_from_file("dummy_path")
        self.assertEqual(result, "data")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_save_to_file(self, mock_exists, mocked_open):
        processor = PresentationProcessor()
        success = processor.save_to_file("data", "testfile.txt")
        self.assertTrue(success)  # This asserts that `success` should be True
        mocked_open.assert_called_with("testfile.txt", 'w')  # Use the mock object passed to the method



if __name__ == '__main__':
    unittest.main()
