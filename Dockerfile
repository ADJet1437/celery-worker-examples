FROM python:3.8-slim-buster

RUN useradd --create-home celery
USER celery
ENV PATH="/home/celery/.local/bin:${PATH}"

WORKDIR /home/celery
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD app.py .

CMD ["celery", "-A", "app", "worker", "-B"]
