import torch
import json
from pathlib import Path
from safetensors.torch import load_file
from stable_audio_tools import create_model_from_config
from stable_audio_tools.inference.generation import generate_diffusion_cond
from stable_audio_tools import get_pretrained_model
from einops import rearrange
import torchaudio
from fastapi import FastAPI, Request
import gc
from torch.cuda.amp import autocast
import uuid
import numpy as np

# Generate stereo audio
from torch import amp

app = FastAPI()
MODEL_PATH = "C:/Users/Ku/FinalProject/Human-FinalProject-API"

device = "cuda" if torch.cuda.is_available() else "cpu"

# 경로 설정
model_dir = Path(MODEL_PATH)
ckpt_path = model_dir / "model.safetensors"
config_path = model_dir / "model_config.json"

# config.json 로드
with open(config_path, "r") as f:
    config = json.load(f)

# 모델 생성 및 가중치 로드
model = create_model_from_config(config)
state_dict = load_file(str(ckpt_path))  # safetensors 로드
model.load_state_dict(state_dict)

model = model.to(device).half()  # float16

sample_rate = config["sample_rate"]
sample_size = config["sample_size"]


@app.get("/")
def hello():
    return {"message": "Hello"}

@app.post("/generate_audio")
async def generateAudio(request: Request):
    data = await request.json()

    # Set up text and timing conditioning
    conditioning = [{
        "prompt": data['prompt'],
        "seconds_start": 0, 
        "seconds_total": 20
    }]


    with torch.no_grad():
        with amp.autocast('cuda', dtype=torch.float16):
            output = generate_diffusion_cond(
                model,
                seed=np.random.randint(0, 2**31 - 1),
                steps=70,
                cfg_scale=7,
                conditioning=conditioning,
                sample_size=sample_rate * 20,
                sigma_min=0.03,
                sigma_max=500,
                sampler_type="dpmpp-3m-sde",
                device=device
            )

    print(1)

    # Rearrange audio batch to a single sequence
    output = rearrange(output, "b d n -> d (b n)")

    uuidFile = f"{uuid.uuid4()}" + ".wav"
    
    filename = f"C:/Users/Ku/Server/ku9907/audio/{uuidFile}"
    print(2)

    # Peak normalize, clip, convert to int16, and save to file
    output = output.to(torch.float32).div(torch.max(torch.abs(output))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()

    print(3)
    torchaudio.save(filename, output, sample_rate)

    print(4)
    del output
    torch.cuda.empty_cache()
    gc.collect()

    return {"message": "Generate Success", "file_name": uuidFile, "save_path" : filename}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)