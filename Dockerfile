FROM python:3.9-slim

COPY . /flask-demo/

RUN pip install -r /flask-demo/requirements.txt

WORKDIR /flask-demo

EXPOSE 8881

CMD ["gunicorn", "main:app", "-c", "./gunicorn/gunicorn.cfg.py"]

