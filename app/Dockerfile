FROM python:3.13.5-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get -y upgrade && \
    pip install -r requirements.txt
EXPOSE 8501
COPY . /app
ENV PATH=“${PATH}:/root/.local/bin”
CMD ["streamlit", "run", "main.py"]
