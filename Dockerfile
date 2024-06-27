FROM --platform=linux/amd64 python:3.8-alpine

LABEL maintainer="Umpa Lumpa <dik@duk.com>"

ENV USER=serviceuser
RUN adduser -D $USER
USER $USER

WORKDIR /app/
COPY /helloapp .
COPY requirements.txt requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install Flask
RUN pip install --no-cache-dir Flask

# Install kubernetes
RUN pip install --no-cache-dir kubernetes

# Install psycopg2-binary
RUN pip install --no-cache-dir psycopg2-binary

# Install requests
RUN pip install --no-cache-dir requests

# Install azure-identity
RUN pip install --no-cache-dir azure-identity

# Install azure-keyvault-secrets
RUN pip install --no-cache-dir azure-keyvault-secrets

ENTRYPOINT [ "python3" ]
CMD ["app.py"]
