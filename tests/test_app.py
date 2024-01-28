import io
import tempfile
import unittest
from unittest.mock import patch

import streamlit as st
from PIL import Image
from rembg import remove

from app import main

class TestApp(unittest.TestCase):

    def test_main(self):
        # Test when no image is uploaded
        with patch.object(st, 'file_uploader', return_value=None):
            with patch.object(st, 'button', return_value=False):
                with patch.object(st, 'image') as mock_image:
                    main()
                    mock_image.assert_not_called()

        # Test when an image is uploaded and background removal is not requested
        with patch.object(st, 'file_uploader', return_value='test_image.png'):
            with patch.object(st, 'button', return_value=False):
                with patch.object(st, 'image') as mock_image:
                    main()
                    mock_image.assert_called_once()

        # Test when an image is uploaded and background removal is requested
        with patch.object(st, 'file_uploader', return_value='test_image.png'):
            with patch.object(st, 'button', return_value=True):
                with patch.object(st, 'image') as mock_image:
                    with patch.object(st, 'spinner') as mock_spinner:
                        with patch.object(Image, 'open') as mock_open:
                            with patch.object(remove, '__call__') as mock_remove:
                                with patch.object(Image, 'open') as mock_open_result:
                                    with patch.object(tempfile, 'NamedTemporaryFile') as mock_temp_file:
                                        with patch.object(st, 'markdown') as mock_markdown:
                                            main()
                                            mock_image.assert_called_once()
                                            mock_spinner.assert_called_once()
                                            mock_open.assert_called_once_with('test_image.png')
                                            mock_remove.assert_called_once()
                                            mock_open_result.assert_called_once_with(io.BytesIO(mock_remove.return_value))
                                            mock_temp_file.assert_called_once()
                                            mock_markdown.assert_called_once()

if __name__ == '__main__':
    unittest.main()
