FROM python:3.10-buster

WORKDIR /src
COPY app ./src

COPY requirements.txt ./src

# Python library
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r ./src/requirements.txt

ENTRYPOINT ["streamlit", "run", "main.py"]
