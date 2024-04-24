#from root of project run:
#python -m unittest tests.test_presentation_creator
#
#
import unittest
from unittest.mock import patch, MagicMock
from presentation.presentation_creator import PresentationCreator


class TestPresentationCreator(unittest.TestCase):
    def setUp(self):
        self.file_path = 'test_data.json'
        self.creator = PresentationCreator(self.file_path)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"slides": [{"title": "Test Title", "content": "Test Content"}]}')
    @patch('json.load')
    def test_load_content_from_json(self, mock_json_load, mock_open):
        mock_json_load.return_value = {'slides': [{'title': 'Test Title', 'content': 'Test Content'}]}
        result = self.creator.load_content_from_json()
        self.assertEqual(result, {'slides': [{'title': 'Test Title', 'content': 'Test Content'}]})

    def test_validate_content_data(self):
        content_data = {'slides': [{'title': 'Test', 'content': 'Test Content'}]}
        result = self.creator.validate_content_data(content_data)
        self.assertTrue(result)

    def test_validate_slide(self):
        slide = {'title': 'Test', 'content': 'Test Content'}
        result = self.creator.validate_slide(slide)
        self.assertTrue(result)

    
    @patch('presentation.presentation_creator.Presentation')
    @patch('os.path.exists', return_value=True)  # Assume the image file exists for this test
    def test_create_presentation(self, mock_exists, mock_presentation):
        # Setup the mock for the Presentation instance
        pres_instance = mock_presentation.return_value
        pres_instance.save.return_value = None
        
        # Create instance of PresentationCreator
        creator = PresentationCreator('dummy.json')
        
        # Mock data that simulates valid input
        content_data = {
            'slides': [{
                'title': 'Test',
                'content': 'Content',
                'images': [{
                    'path': 'path/to/image.jpg',
                    'caption': 'A caption'
                }],
                'imagelayout': [1, 1]
            }]
        }
        
        # Run the method to test
        creator.create_presentation(content_data, 'output.pptx')
        
        # Check that the save method was called
        pres_instance.save.assert_called_with('output.pptx')
    

    # Add additional tests for other methods if needed

if __name__ == '__main__':
    unittest.main()
