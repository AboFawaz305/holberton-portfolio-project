FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD fastapi run src/main.py --forwarded-allow-ips="*"
