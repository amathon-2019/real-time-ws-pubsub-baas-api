FROM python:3.7

COPY requirements.txt /opt/api/requirements.txt
WORKDIR "/opt/api"
RUN python3.7 -m pip install -r /opt/api/requirements.txt

COPY . /opt/api

EXPOSE 8000

CMD ["python", "main.py"]
