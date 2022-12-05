FROM python:3

COPY . /flask-demo/

RUN pip install -r /flask-demo/requirements.txt

WORKDIR /flask-demo

EXPOSE 8881

CMD ["gunicorn", "app:app", "-c", "./gunicorn/gunicorn.cfg.py"]

