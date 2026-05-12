import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys

# Add src to path
sys.path.append(os.path.abspath("src"))

from publish_to_zenodo import publish

class TestZenodoPublish(unittest.TestCase):
    @patch('requests.post')
    @patch('requests.put')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists')
    def test_publish_injects_metadata(self, mock_exists, mock_open, mock_put, mock_post):
        # Setup mocks
        mock_exists.side_effect = lambda x: x == "ro-crate-metadata.json" or x == "dummy.md"

        # Mocking json.load for ro-crate-metadata.json
        ro_crate_content = {"@type": "Dataset", "name": "Test Corpus"}

        # We need to handle the multiple calls to open
        mock_file_ro = MagicMock()
        mock_file_ro.__enter__.return_value.read.return_value = json.dumps(ro_crate_content).encode()

        mock_file_main = MagicMock()
        mock_file_main.__enter__.return_value.read.return_value = b"test content"

        # This is a bit tricky with builtins.open and json.load
        # Let's simplify and just check if requests.post was called with expected description

        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            'id': 123,
            'links': {'bucket': 'http://bucket'}
        }

        mock_put.return_value.status_code = 201

        # Run publish
        with patch('os.environ.get', return_value="fake_token"):
            with patch('json.load', return_value=ro_crate_content):
                publish("dummy.md", "Test Title", "en")

        # Verify
        call_args = mock_post.call_args_list[0]
        sent_data = json.loads(call_args.kwargs['data'])
        description = sent_data['metadata']['description']

        self.assertIn("AI Identity & Metadata (RO-Crate)", description)
        self.assertEqual(sent_data['metadata']['creators'][0]['orcid'], '0000-0002-8401-8018')

if __name__ == "__main__":
    unittest.main()
