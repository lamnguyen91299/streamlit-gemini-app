import os
import google.generativeai as genai
import streamlit as st
from PIL import Image
import io


# Check if the app is running in Streamlit Cloud
if "gemini_api_key" in st.secrets:
    # Use Streamlit Secrets if running in Streamlit Cloud
    gemini_api_key = st.secrets["gemini_api_key"]
else:
    # Load environment variables if running locally
    from dotenv import load_dotenv
    import os
    load_dotenv()
    gemini_api_key = os.getenv("gemini_api_key")

genai.configure(api_key=gemini_api_key)


def handle_uploaded_image(uploaded_file):
  if uploaded_file is None:
    return None
  try:
    # Đọc nội dung tệp được tải lên và chuyển đổi thành chuỗi byte
    image_bytes = uploaded_file.read()
    img = Image.open(io.BytesIO(image_bytes))
    # Chuyển đổi chuỗi byte thành đối tượng PIL Image
    return img
  except Exception as e:
    print(f"Lỗi khi đọc tệp hình ảnh: {e}")
    return None

model = genai.GenerativeModel('gemini-pro-vision')

st.header("We're Not Really Stranger")

wnrs_level = st.radio(
    "Select your level: \n\n",
    ["Icebreaker ","Connection ", "Reflection "],
    key="wnrs_level",
    horizontal=True
)

picture = st.camera_input("Take a picture")
if picture:
    st.write("Take picture succesfull !")

img = handle_uploaded_image(picture)
prompt = f"""Based on the concept of the "We're Not Really Strangers" deck and the content of the photo that input . Please give me 1 main questions from level {wnrs_level} along with an additional sub question .
With these inputs, make sure to follow following guidelines and generate with proper headlines: 
  + main question :
    + sub question : 
"""
er_diag_img_description = st.button("Generate!", key="er_diag_img_description")
if er_diag_img_description and prompt:
    with st.spinner("Generating..."):
        response = model.generate_content([prompt, img])
        st.markdown(response.text)