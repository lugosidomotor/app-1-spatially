FROM --platform=linux/amd64 python:3.8-alpine

LABEL maintainer="Umpa Lumpa <dik@duk.com>"

ENV USER=serviceuser
RUN adduser -D $USER
USER $USER

WORKDIR /app/
COPY /helloapp .
COPY requirements.txt requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir Flask && \
    pip install --no-cache-dir kubernetes && \
    pip install --no-cache-dir psycopg2-binary && \
    pip install --no-cache-dir requests && \
    pip install --no-cache-dir azure-identity && \
    pip install --no-cache-dir azure-keyvault-secrets

ENTRYPOINT [ "python3" ]
CMD ["app.py"]
