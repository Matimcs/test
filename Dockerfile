# Usar la imagen oficial de Python
FROM python:3.8

# Instalar las bibliotecas necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    geckodriver \
    libdbus-glib-1-2 \
    libgtk-3-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copiar el código local a la imagen
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Ejecutar la aplicación con Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
