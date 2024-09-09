# Usar la imagen oficial de Python
FROM python:3.8

# Instalar las bibliotecas necesarias
RUN apt-get update && apt-get install -y \
    gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 \
    libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation \
    libappindicator1 libnss3 lsb-release xdg-utils \
    libvulkan1 mesa-vulkan-drivers

# Instalar Firefox
RUN apt-get install -y firefox-esr

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