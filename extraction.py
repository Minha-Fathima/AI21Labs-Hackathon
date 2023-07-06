import ai21
import os

from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv(".env.local")

# Access the API key
api_key = os.getenv("API_KEY")

ai21.api_key = api_key


def Job_Title_Extraction(text):
    response = ai21.Experimental.answer(
        context=text, question="What job is this person applying for?"
    )
    return response.answer


def Skills_Extraction(text):
    response = ai21.Experimental.answer(
        context=text, question="What skill sets does this person have?"
    )
    return response.answer
