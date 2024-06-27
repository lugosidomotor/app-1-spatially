FROM --platform=linux/amd64 python:3.9-alpine

LABEL maintainer="Umpa Lumpa <dik@duk.com>"

ENV USER=serviceuser
RUN adduser -D $USER
USER $USER

WORKDIR /app/
COPY /helloapp .
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD ["app.py"]
