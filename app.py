import streamlit as st
from dotenv import load_dotenv

load_dotenv() ## load all the nevironment variables
import os
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points. 
Please provide the summary of the text given as following format: 

- Topic  Title(Bold)Large size
- Detailed summary of each topics """

# To extract Videoid from youtube url
def extract_video_id(url):
    # Parse the URL
    parsed_url = urlparse(url)
    # Extract query part from the URL
    query_string = parsed_url.query
    # Parse query string to get video ID
    video_id = parse_qs(query_string).get("v", [None])[0]
    return video_id

## to get the transcript data from youtube video
def extract_transcript_details(video_url):
    try:
        video_id=extract_video_id(video_url)
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## To get the summary based on Prompt from Google Gemini Pro
def generate_Lecture(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("Lecture Loom")
yt_url = st.text_input("Enter YouTube Video Link:")

if yt_url:
    video_id = extract_video_id(yt_url)
    print(video_id)
    st.image(f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg", use_column_width=True)
    


if st.button("Get Lecture Notes"):
    transcript_text=extract_transcript_details(yt_url)

    if transcript_text:
        summary=generate_Lecture(transcript_text,prompt)
        st.markdown("Here is your Lecture Notes:")
        st.write(summary)



