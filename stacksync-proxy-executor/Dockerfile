#Saarthak Mudigere Girsh
#saarthakmudigere@gmail.com
#6823923698

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py ./main.py

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

