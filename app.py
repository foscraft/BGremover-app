import streamlit as st
from rembg import remove
from PIL import Image
import io
import numpy as np

def main():
    st.subheader("Foscraft's Image Background Remover App")

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Remove Background"):
            with st.spinner("Removing background..."):
                # Remove background
                result = remove(np.array(image))
                # Convert numpy array with alpha channel to PIL Image
                result_image = Image.fromarray(result, mode="RGBA")

                st.image(result_image, caption="Background Removed", use_column_width=True)
                result_bytes_io = io.BytesIO()
                result_image.save(result_bytes_io, format="PNG")
                result_bytes_io.seek(0)

                # Download button to save the file
                st.download_button(label="Download Image", key="download_button", data=result_bytes_io, file_name="background_removed.png", mime="image/png")

if __name__ == "__main__":
    main()
