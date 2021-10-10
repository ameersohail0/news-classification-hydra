FROM python:3.8-slim
LABEL team="Hydra"

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99
ENV FLASK_APP app.py

SHELL ["/bin/bash", "-c"]

# Install apt dependencies
RUN apt update

# Install dependencies
RUN pip3 install flask

# Application code
COPY app.py /app/app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]