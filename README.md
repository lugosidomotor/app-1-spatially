# app-1-spatially

## Overview

This project is a Flask-based web application that reads data from a file, writes it to a PostgreSQL database, and displays it on a webpage. It also integrates with Kubernetes and Azure Key Vault for managing secrets.

graph TD;
    A[Start] --> B[Read data from data.txt]
    B --> C[Initialize Kubernetes client]
    C --> D[Get Key Vault address from Kubernetes secret]
    D --> E[Decode Key Vault address]
    E --> F[Initialize Azure Key Vault client]
    F --> G[Get PostgreSQL connection string from Key Vault]
    G --> H[Connect to PostgreSQL database]
    H --> I[Create table if not exists]
    I --> J[Write data to database]
    J --> K[Start Flask web server]
    K --> L[Display data on webpage]
