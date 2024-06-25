FROM python:3.8-alpine

LABEL maintainer="Umpa Lumpa <dik@duk.com>"

ENV USER=serviceuser
RUN adduser -D $USER
USER $USER

WORKDIR /app/
COPY /helloapp .
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["app.py"]
