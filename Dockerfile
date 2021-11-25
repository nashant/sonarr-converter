FROM python:3.10-slim

EXPOSE 8080/tcp

ADD ./src /src
WORKDIR /src

RUN apt-get update -y \
 && apt-get install -yq --no-install-recommends ffmpeg \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -r /var/cache/apt

ENTRYPOINT ["python3", "converter.py"]