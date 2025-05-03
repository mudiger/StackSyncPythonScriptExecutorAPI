#Saarthak Mudigere Girsh
#saarthakmudigere@gmail.com
#6823923698

FROM python:3.11-slim

# Install dependencies for nsjail
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libcap2-bin \
    libprotobuf-dev \
    protobuf-compiler \
    pkg-config \
    ca-certificates \
    flex \
    bison \
    libnl-3-dev \
    libnl-route-3-dev

# Clone and build nsjail
RUN git clone https://github.com/google/nsjail.git /opt/nsjail && \
    cd /opt/nsjail && \
    make && \
    cp nsjail /usr/local/bin/nsjail && \
    chmod +x /usr/local/bin/nsjail

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up the app
WORKDIR /app
COPY app/ ./app/
COPY nsjail.cfg .

EXPOSE 8080
CMD ["python", "app/main.py"]
