FROM python:3.10-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src
COPY api ./src

COPY requirements.txt ./src

# https://stackoverflow.com/questions/58018300/using-a-pip-cache-directory-in-docker-builds
# RUN pip3 install --no-cache-dir -r ./src/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r ./src/requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
