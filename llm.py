import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Please set GOOGLE_API_KEY in your environment.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

def complete(prompt: str) -> str:
    return llm.invoke(prompt).content.strip()