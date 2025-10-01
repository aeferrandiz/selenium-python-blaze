# Dockerfile para el Framework de Automatización QA
FROM python:3.12-slim

# Metadatos del contenedor
LABEL maintainer="Equipo QA"
LABEL description="Framework de Automatización QA para DemoBlaze"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HEADLESS=true
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_PATH=/usr/bin/google-chrome

# Instalar dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    curl \
    unzip \
    xvfb \
    x11vnc \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome de forma segura
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar Mozilla Firefox
RUN apt-get update \
    && apt-get install -y firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias primero (para optimizar cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Crear usuario no-root antes de copiar el código fuente
RUN useradd --create-home --shell /bin/bash qa

# Copiar código fuente del proyecto
COPY --chown=qa:qa . .

# Crear directorios necesarios para reportes
RUN mkdir -p reports/screenshots reports/allure-results \
    && chown -R qa:qa /app

# Cambiar al usuario no-root para seguridad
USER qa

# Exponer puerto para servir reportes
EXPOSE 8080

# Verificación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import selenium; print('OK')" || exit 1

# Copiar y configurar script de entrada
COPY --chown=qa:qa docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Configurar punto de entrada y comando por defecto
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["test"]
