# import FastApi
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sys, uvicorn

# import Env
from dotenv import load_dotenv
import os

# import Gemini Api
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

load_dotenv()

myApi = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=myApi)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "hello colab"}


@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    input_text = data.get("message", "")
    if input_text == "":
        return JSONResponse(content={"Response": "No Input Data"})
    response_prom = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a prompt engineer specialized in creating keyword-rich prompts for Stable Diffusion. Use English keywords only. Convert a simple image idea into a single, well-structured prompt made of concise, comma-separated visual keywords. Focus on realism, high detail, lighting, mood, and scene elements. Do not write full sentences, lists, or explanations. Only return one prompt per input."),
    contents=input_text
    )
    
    converted_prompt = response_prom.text

    response_img = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=converted_prompt,
        config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
        )
    )
    
    for part in response_img.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            img_base64 = base64.b64encode(part.inline_data.data).decode('utf-8')
    
    return JSONResponse({
        "prompt": converted_prompt,
        "image": img_base64
    })
