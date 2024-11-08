FROM python:3.11
WORKDIR /docker_fast
COPY ./requirements.txt /docker_fast/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /docker_fast/requirements.txt

COPY . /docker_fast

CMD ["uvicorn", "/docker_fast/api:app", "--host", "0.0.0.0", "--port", "8000"]
