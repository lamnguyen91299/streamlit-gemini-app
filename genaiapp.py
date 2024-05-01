import os
import numpy as np
import cv2
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

# define a convert upload file to variable
@st.cache_data
def handle_uploaded_image(uploaded_file):
  """
  Chuyển đổi tệp hình ảnh được tải lên Streamlit thành đối tượng PIL Image.

  Args:
      uploaded_file: Đối tượng tệp được tải lên lấy từ st.file_uploader trong Streamlit

  Returns:
      Nếu chuyển đổi thành công, trả về đối tượng PIL Image, nếu thất bại, trả về None.
  """
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
@st.cache_data
def process_image(image_data):
    """Processes the image data for display."""
    if image_data is not None:
        img = Image.open(image_data)
        return img
    else:
        return None
# session state
if 'img' not in st.session_state:
    st.session_state['img'] = None
if 'upload_button' not in st.session_state:
    st.session_state.upload_button = False
# First header
st.header("Gemini Vertex AI Project")
tab1, tab2 = st.tabs(
    ["Marketing campaign", "Image analyst"]
)
# Marketing campaign tab 
with tab1:
    st.subheader("Generate your marketing campaign")

    product_name = st.text_input(
        "What is the name of the product? \n\n", key="product_name", value="Tetchies Data Edu"
    )
    product_category = st.radio(
        "Select your product category: \n\n",
        ["Education","Clothing", "Electronics", "Food", "Health & Beauty"],
        key="product_category",
        horizontal=True
    )
    st.write("Select your target audience: ")
    target_audience_age = st.radio(
        "Target age: \n\n",
        ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        key="target_audience_age",
        horizontal=True
    )
    # target_audience_gender = st.radio("Target gender: \n\n",["male","female","trans","non-binary","others"],key="target_audience_gender",horizontal=True)
    target_audience_location = st.radio(
        "Target location: \n\n",
        ["Urban", "Suburban", "Rural"],
        key="target_audience_location",
        horizontal=True
    )
    st.write("Select your marketing campaign goal: ")
    campaign_goal = st.multiselect(
        "Select your marketing campaign goal: \n\n",
        [
            "Increase brand awareness",
            "Generate leads",
            "Drive sales",
            "Improve brand sentiment",
        ],
        key="campaign_goal",
        default=["Increase brand awareness", "Generate leads"],
    )
    if campaign_goal is None:
        campaign_goal = ["Increase brand awareness", "Generate leads"]
    brand_voice = st.radio(
        "Select your brand voice: \n\n",
        ["Formal", "Informal", "Serious", "Humorous"],
        key="brand_voice",
        horizontal=True,
    )
    estimated_budget = st.radio(
        "Select your estimated budget ($): \n\n",
        ["1,000-5,000", "5,000-10,000", "10,000-20,000", "20,000+"],
        key="estimated_budget",
        horizontal=True,
    )
    prompt = f"""Generate a marketing campaign for {product_name}, a {product_category} designed for the age group: {target_audience_age}.
    The target location is this: {target_audience_location}.
    Aim to primarily achieve {campaign_goal}.
    Emphasize the product's unique selling proposition while using a {brand_voice} tone of voice.
    Allocate the total budget of {estimated_budget}.
    With these inputs, make sure to follow following guidelines and generate the marketing campaign with proper headlines: \n
    - Briefly describe company, its values, mission, and target audience.
    - Highlight any relevant brand guidelines or messaging frameworks.
    - Provide a concise overview of the campaign's objectives and goals.
    - Briefly explain the product or service being promoted.
    - Define your ideal customer with clear demographics, psychographics, and behavioral insights.
    - Understand their needs, wants, motivations, and pain points.
    - Clearly articulate the desired outcomes for the campaign.
    - Use SMART goals (Specific, Measurable, Achievable, Relevant, and Time-bound) for clarity.
    - Define key performance indicators (KPIs) to track progress and success.
    - Specify the primary and secondary goals of the campaign.
    - Examples include brand awareness, lead generation, sales growth, or website traffic.
    - Clearly define what differentiates your product or service from competitors.
    - Emphasize the value proposition and unique benefits offered to the target audience.
    - Define the desired tone and personality of the campaign messaging.
    - Identify the specific channels you will use to reach your target audience.
    - Clearly state the desired action you want the audience to take.
    - Make it specific, compelling, and easy to understand.
    - Identify and analyze your key competitors in the market.
    - Understand their strengths and weaknesses, target audience, and marketing strategies.
    - Develop a differentiation strategy to stand out from the competition.
    - Define how you will track the success of the campaign.
   -  Utilize relevant KPIs to measure performance and return on investment (ROI).
   Give proper bullet points and headlines for the marketing campaign. Do not produce any empty lines.
   Be very succinct and to the point.
    """
    config = {
        "temperature": 0.8,
        "max_output_tokens": 2048,
    }
    model = genai.GenerativeModel('gemini-pro')
    generate_t2t = st.button("Generate my campaign", key="generate_campaign")
    if generate_t2t and prompt:
        second_tab1, second_tab2 = st.tabs(["Campaign", "Prompt"])
        with st.spinner("Generating your marketing campaign..."):
            with second_tab1:
                response = model.generate_content(prompt)
                if response:
                    st.write("Your marketing campaign:")
                    st.write(response.text)
            with second_tab2:
                st.text(prompt)  

# Image analyst tab
with tab2:
    model = genai.GenerativeModel('gemini-pro-vision')
    st.write("Using Gemini 1.0 Pro Vision - Multimodal model")
    screens_undst, diagrams_undst = st.tabs(
        [
            "Image, Art",
            "ER diagrams",
        ]
    )
    # screens_undst tab
    
    with screens_undst:
        uploaded_art_file = st.file_uploader("Upload your picture", type=["jpg","png"])
        img = handle_uploaded_image(uploaded_art_file)
        st.session_state['img'] = img
        # Display image
        if img:
            st.image(img)
        else:
            st.warning("Please upload your picture !")
        prompt = """Is an expert in art paintings. Please list the information of the following photo including the following information : 
        Author, Historical background, year of release, Meaning of the painting. 
In addition, if the painting is not a famous painting, please state the basic information of the photo, including the composition and artistic genre of the photo, information such as author, context, Year of release need not be stated."""
        tab1, tab2 = st.tabs(["Response", "Prompt"])
        img_description = st.button("Generate!", key="img_description")
        #Response tab
        with tab1:
            if img_description and prompt:
                with st.spinner("Generating..."):
                    response = model.generate_content([prompt, img])
                    st.markdown(response.text)
        #Prompt tab
        with tab2:
            st.write("Prompt used:")
            st.text(prompt + "\n" + "input_image") 

    # diagrams_undst
    with diagrams_undst:
        uploaded_uml_file = st.file_uploader("Upload your UML", type=["jpg","png"])
        uml_img = handle_uploaded_image(uploaded_uml_file)
        if uml_img:
            st.image(uml_img)
        else:
            st.warning("Please upload your UML !")
        prompt = """Document the entities and relationships in this ER diagram"""
        tab1, tab2 = st.tabs(["Response", "Prompt"])
        er_diag_img_description = st.button("Generate!", key="er_diag_img_description")
        #Response tab
        with tab1:
            if er_diag_img_description and prompt:
                with st.spinner("Generating..."):
                    response = model.generate_content([prompt, uml_img])
                    st.markdown(response.text)
        #Prompt tab
        with tab2:
            st.write("Prompt used:")
            st.text(prompt + "\n" + "input_image")                             