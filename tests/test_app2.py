import streamlit as st
from rembg import remove
from PIL import Image
import io
import numpy as np
import tempfile
import pytest

def test_main():
    # Test file upload
    with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
        temp_file.write(b"dummy image data")
        temp_file.seek(0)
        st.file_uploader = lambda label, type: temp_file.name
        main()

    # Test button click
    st.button = lambda label: True
    main()

    # Test image processing
    st.spinner = lambda label: None
    st.image = lambda image, caption, use_column_width: None
    st.markdown = lambda text: None
    main()

def test_remove_background():
    # Test remove background function
    image_array = np.zeros((100, 100, 4), dtype=np.uint8)
    result = remove(image_array)
    assert result.shape == (100, 100, 4)

def test_save_result_image():
    # Test save result image function
    result_image = Image.fromarray(np.zeros((100, 100, 4), dtype=np.uint8), mode="RGBA")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        save_result_image(temp_file.name, result_image)
        assert os.path.exists(temp_file.name)

if __name__ == "__main__":
    pytest.main()
