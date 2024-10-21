# MLOps-course
MLOps Specialize: Udemy Bootcamp 2022 


## Section 13: Putting models into production
There are different alternatives to deploy a model in a production environment:
 1. Through API 
 2. Through applications (mobile/web)

## Section 14: MLOps phase 3: Model serving through APIs
Several Python API package for quickstart:
- [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/)
- [Django](https://www.django-rest-framework.org/tutorial/quickstart/)

In this Section we focus on serving model via APIs using FastAPI framework

### 1. Run first simple FastAPI app
1. Create new conda env
```bash
conda create --name phase3-mlops python=3.9
# or
# conda create --prefix D:/Users/st_cong/conda/phase3-mlops python=3.9
# mklink /J "C:\Users\st_cong\AppData\Local\miniconda3\envs\phase3-mlops" "D:\Users\st_cong\conda\phase3-mlops" 
conda activate phase3-mlops
```
2. Install packages
```bash
(phase3-mlops) pip install -r requirements.txt
```
3. Run App
```bash
(phase3-mlops) python "1.FastAPI Fundamentals.py"

INFO:     Started server process [8372]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
> You can open direct http://127.0.0.1:8000 to send request to API or make request via [PostMan](https://www.postman.com/)

