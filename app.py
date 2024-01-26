import google.generativeai as genai
import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

import PyPDF2 as pdf

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_response(input):
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content(input)
   return response.text

def extract_text(resume):
   reader = pdf.PdfReader(resume)
   number_of_pages = len(reader.pages)
   text = ''
   for i in range(number_of_pages):
      page = reader.pages[i]
      text += str(page.extract_text())
   return text

#Prompt Template
input_prompt1 = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on job descripion
resume:{text}
job description:{job_desc}

I want the response in one single string having the below structure with areas of improvement
"JD Match":"%"
"""

input_prompt2 = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Find the missing keywords in the resume comparing with job description with highest accuracy
resume:{text}
job description:{job_desc}

I want the response in one single string having the structure mentioning all the missing keywords and skills
"MissingKeywords:[]"
"""

# Set page title and header
st.set_page_config(page_title='TrackTalent', layout='wide')

# st.title('TrackTalent')
st.markdown("<h1 style='text-align: left; color: teal;'>TrackTalent</h1>", unsafe_allow_html=True)
job_desc = st.text_area('Paste your Job Description here:', height=200)
resume = st.file_uploader('Upload your Resume file (PDF only)', type=['pdf'])

submit1 = st.button("Percentage match")
submit2 = st.button("Missing Keywords")

if submit1:
    if resume is not None:
        text=extract_text(resume)
        response=get_response(input_prompt1)
        st.subheader(response)

if submit2:
    if resume is not None:
        text=extract_text(resume)
        response=get_response(input_prompt2)
        st.subheader(response)