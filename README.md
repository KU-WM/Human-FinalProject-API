# Final Project
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Anaconda](https://img.shields.io/badge/anaconda-44A833?style=for-the-badge&logo=anaconda&logoColor=white)
![Fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![pytorch](https://img.shields.io/badge/pytorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![nVIDIA](https://img.shields.io/badge/cuda-000000.svg?style=for-the-badge&logo=nVIDIA&logoColor=green)
![huggingface](https://img.shields.io/badge/huggingface-FFD21E.svg?style=for-the-badge&logo=huggingface&logoColor=green)
![Nginx](https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

## 📌 목차
- [📝 소개](#-소개)
- [📘 사용법](#-사용법)
- [🎯 제작 목적](#-제작-목적)
- [🛠 개발 과정](#-개발-과정)
- [📁 전체 프로젝트 구성 트리](#-전체-프로젝트-구성-트리)
- [🧰 사용 기술 스택](#-사용-기술-스택)
- [📚 Reference](#-reference)
- [📄 License](#-license)
 
## 📝 소개
<img src="https://github.com/user-attachments/assets/85cc6a6d-3c04-41d2-b8ea-1ad42b39f49a" width="775px" />

Gemini API와 Stable-Audio 1.0 모델을 활용하여 **사용자가 간단한 텍스트 입력만으로 원하는 이미지와 간단한 효과음을 생성할 수 있는 사이트**를 풀스택으로 개발하고 서비스 하였습니다. 이 레포지토리는 해당 서비스의 ApiServer (Audio) 코드 입니다.<br>
[https://lnpra.com](https://lnpra.com) 에 접속하시면 해당 서비스를 사용하실 수 있습니다.<br>

프로젝트의 유지보수를 위하여 개인 프로젝트를 아래 3개의 레포지토리로 분리하여 저장하였습니다.<br>

[FrontEnd](https://github.com/KU-WM/Human-FinalProject-Front)<br>
[BackEnd](https://github.com/KU-WM/Human-FinalProject-Back.git)<br>
[Api Server](https://github.com/KU-WM/Human-FinalProject-API.git) - 현재 페이지<br>

## 📘 사용법

1) 모델 다운로드
https://huggingface.co/stabilityai/stable-audio-open-1.0 에 접속 후 모델 승인 받기 / 파일 전부 다운로드

2) git clone
```bash
git clone https://github.com/KU-WM/Human-FinalProject-API
```

3) 변수 설정
아래 표에 해당하는 변수를 반드시 본인 설정에 맞게 변경

|변수명|기능|
|---|---|
|MODEL_PATH|1에서 다운받은 폴더의 절대경로|
|filename|파일이 저장될 경로|
|__name__의 port|fastApi가 실행될 포트 번호|

4) 가상환경 구축

```bash
conda create -n [이름] python=3.10.16
conda activate [이름]
pip install -r requirements.txt
```
(pip install -r requirements.txt 이 코드의 경우 cd로 2번의 git clone 디렉토리로 이동하거나
requirements.txt 파일의 경로까지 전부 적어주어야 함)

5) 추가 파라미터 조정
모델의 효과음 생성 파라미터 조정 (generate_diffusion_cond 함수 내부)

|파라미터|기능|
|---|---|
|seed|매 실행마다 무작위로 생성 / 같은 입력에 대한 실행마다 동일한 값 원하면 상수|
|steps|오디오 생성시 전체 단계 수 / 크기에 따라 생성시간과 품질 상승|
|cfg_scale|DB의 정보를 받아오기 위한 데이터 형식 정의|
|sample_size|샘플링을 할 크기 (samepl_rate가 보통 1초)|
|sigma_min|끝의 노이즈 크기|
|sigma_max|시작시의 노이즈 크기|
|sampler_type|데이터를 샘플링 할 방식|

|기타 파라미터|기능|
|---|---|
|device|모델이 동작할 장치 cuda/cpu|
|conditioning|DB의 정보를 제어하는 기능 / 프롬프트, 사운드 길이(단 sample_size가 우선)|

7) 실행
```bash
python test.py
```
단 test.py의 경로로 cd를 통해 이동하거나 test.py의 경로를 모두 포함하여 사용해야 함

## 🎯 제작 목적
 기존 ai 이미지 생성시 유료 서비스 이거나, 모델 / LoRA / 파라미터 / 프롬프트 등 복잡한 입력이 필요 한 경우가 많습니다. 효과음 생성의 경우는 찾는것 부터가 힘든 경우도 있습니다.<br>
이 기능들을 쉽게 접근 가능하고 불편함 없이 간단한 설명만으로 원하는 이미지와 그에 어울리는 효과음을 생성할 수 있는 서비스를 제공하기 위해 제작하였습니다.

## 🛠 개발 과정
- 2025.05.26 ~ 2025.06.26 (약 5주) 의 기간동안 진행하였습니다.
- 오전/오후의 스크럼 회의를 통해 진행사항을 점검하고, 애자일 방법론을 통하여 유연한 개발을 진행하였습니다.

## 📁 전체 프로젝트 구성 트리
```
📦Human-FinalProject-API
 ┣ 📂projection_model
 ┣ 📂scheduler
 ┣ 📂text_encoder
 ┣ 📂tokenizer
 ┣ 📂transformer
 ┣ 📂vae
 ┣ 📂__pycache__
 ┣ 📜.gitignore
 ┣ 📜fma_dataset_attribution2.csv
 ┣ 📜freesound_dataset_attribution2.csv
 ┣ 📜LICENSE.md
 ┣ 📜model.ckpt
 ┣ 📜model.safetensors
 ┣ 📜model_config.json
 ┣ 📜model_index.json
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┣ 📜stable_audio_light.png
 ┗ 📜test.py
```
huggyface의 stable-audio 1.0을 받은 뒤 git과 같은 경로로 합친 경우의 트리입니다.

## 📚 Reference
- https://github.com/Stability-AI/stable-audio-tools.git
    - Stable-Audio 전용 라이브러리 stable-audio-tools의 깃허브.
- https://stableaudio.com/user-guide/prompt-structure
    - Stable-Audio 공식 문서 / 프롬프트 예시

## 📄 License
본 프로젝트의 코드는 비상업적 용도로 자유롭게 사용하실 수 있습니다.
상업적 이용이나 수정, 재배포 시에는 사전 연락을 부탁드립니다.
