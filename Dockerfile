FROM python:3.12-alpine

ADD requirements.txt /autumn/requirements.txt
RUN pip3 install -r /autumn/requirements.txt

WORKDIR /autumn
CMD ["python3", "-u", "main.py"]
