FROM python:latest
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD fastapi run src/main.py --forwarded-allow-ips="*"
