FROM python:3.8.10-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# RUN apt-get update && apt-get install -y ffmpeg

EXPOSE 8501

CMD ["streamlit", "run", "main.py","–server.port=8501", "–server.address=0.0.0.0"]