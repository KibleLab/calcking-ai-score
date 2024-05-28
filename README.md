# Installation
```sh
conda create -n calc python=3.12 -y
conda activate calc
pip install -r requirements.txt
```

# How to start
```sh
uvicorn main:app --reload
```