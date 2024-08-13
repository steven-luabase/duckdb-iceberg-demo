FROM python:3.11-slim

WORKDIR /project

COPY . .

RUN pip install -r requirements.txt

# Exposing the flask app port from container to host
EXPOSE 5000

# Starting application
CMD ["python", "main.py"]
