import streamlit as st
import openai
from io import BytesIO
import requests
from PIL import Image

# Set up your OpenAI API key
openai.api_key = "YOUR_KEY"
if st.button("화면이 너무 지저분 하다면 눌러주세요"):
    st.session_state.clear()
    st.experimental_rerun()
# Create a Streamlit web app
st.title("나만의 작은 그림 일기장")

# Define a function to generate a response using GPT-3.5 Turbo
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turbo engine
        prompt=prompt,
        max_tokens=300,  # Set the maximum number of tokens in the response
        n=1,  # Generate a single response
        stop=None,  # Specify an optional stop sequence to end the response
        temperature=0.2,  # Control the randomness of the generated response
        top_p=1.0,  # Control the diversity of the generated response
    )
    return response.choices[0].text.strip()

# Create a text input for the user to enter their message
user_input = st.text_area("일기를 적어보세요 ( 특수 문자나 기호 사용 ❌)", height=200)

# Create a session_state variable to store the response3 value
if 'response3' not in st.session_state:
    st.session_state.response3 = ""
    

# Generate a response when the user submits their message
if st.button("제출"):
    response1 = generate_response(user_input + " 내가 적은것을 한줄로 다른 말 넣지말고 딱 요약한 것만 보여줘")
    st.success(response1)

    # Store the value of response1 in session_state
    st.session_state.response1 = response1

# Check if response1 is available in session_state
if 'response1' in st.session_state:
    response2 = generate_response(st.session_state.response1 + " 이 글이 행복, 슬픔, 화남 중 어떤 것 같아 키워드만 말해줘")

    # Store the value of response2 in session_state
    st.session_state.response2 = response2

# Check if response2 is available in session_state
if 'response2' in st.session_state:
    if st.session_state.response2 == "행복":
        st.success('😀')
    elif st.session_state.response2 == "슬픔":
        st.success('😭')
    elif st.session_state.response2 == "화남":
        st.success('🤬')

    response3 = generate_response(st.session_state.response1 + " 영어로 번역해서 다른 말 넣지말고 보여줘")

    # Store the value of response3 in session_state
    st.session_state.response3 = response3
    
    option = st.selectbox(
    '당신이 좋아하는 그림 스타일은?',
    ('digital art', 'oil', 'pencil', 'crayon')
    )
    st.session_state.option = option
    if st.button("이미지 만들기"):
        response = openai.Image.create(
            prompt=st.session_state.option+" drawing of " + st.session_state.response3,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.text("이미지가 마음에 드시지 않으면 다시 버튼을 눌려주세요")
        
