FROM python:3.10-slim

RUN apt-get update && apt-get install libgl1-mesa-glx libglib2.0-0 -y

WORKDIR /app

COPY requirements.txt	.

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999"]