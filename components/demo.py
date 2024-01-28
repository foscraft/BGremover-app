import streamlit as st
from rembg import remove
from PIL import Image
import io
import numpy as np
import tempfile

def main():
    st.subheader("Foscraft's Background Remover App")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Remove Background"):
            with st.spinner("Removing background..."):
                # Convert PIL image to RGBA format
                image_rgba = image.convert("RGBA")

                # Convert RGBA image to numpy array
                image_array = np.array(image_rgba)

                # Remove background
                result = remove(image_array)

                # Convert numpy array with alpha channel to PIL Image
                result_image = Image.fromarray(result, mode="RGBA")

                # Display result image
                st.image(result_image, caption="Background Removed", use_column_width=True)

                # Save result image to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    result_image.save(temp_file.name)

                # Provide download link for the result image
                result_bytes = result_image.tobytes()
                st.download_button(label="Download Image", key="download_button", data=result_bytes, mime="image/png")

if __name__ == "__main__":
    main()
