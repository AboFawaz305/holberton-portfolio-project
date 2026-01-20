FROM python:latest
COPY defaults/RR.gif /static/uploads/organizations/RR.gif
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD fastapi run src/main.py --forwarded-allow-ips="*"
