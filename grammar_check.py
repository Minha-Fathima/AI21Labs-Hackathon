import ai21
import os
import warnings

from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv(".env.local")

# Access the API key
api_key = os.getenv("API_KEY")

ai21.api_key = api_key


def grammarCheck(text):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            lines = text.split("\n")
            chunks = []
            current_chunk = ""
            for line in lines:
                if len(current_chunk) + len(line) + 1 > 500:
                    chunks.append(current_chunk)
                    current_chunk = line
                else:
                    current_chunk += "\n" + line
            if current_chunk:
                chunks.append(current_chunk)

            print("Total text length:", len(text))
            for i, chunk in enumerate(chunks, start=1):
                print(f"Chunk {i} length:", len(chunk))

            corrections = []
            for chunk in chunks:
                response = ai21.GEC.execute(text=chunk)
                corrections.extend(response.corrections)
        return corrections
    except Exception as e:
        print("Error occurred during grammar checking:", str(e))
        return []


def getLineNo(text, errors):
    lines = text.split("\n")
    errorLines = []

    for error in errors:
        size = 0
        for i, line in enumerate(lines):
            if error["startIndex"] < (size + len(line)):
                errorLines.append(i + 1)
                break
            size += len(line) + 1
    return errorLines
