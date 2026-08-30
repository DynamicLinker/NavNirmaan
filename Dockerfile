FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    blender \
    openscad \
    && rm -rf /var/lib/apt/lists/*


RUN ln -s /usr/bin/blender /usr/bin/blender-5.2

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt


COPY Backend/ ./Backend/
COPY Frontend/ ./Frontend/
COPY start.sh /app/start.sh

# Expose the ports for Backend (8000) and Frontend (8080)
EXPOSE 8000
EXPOSE 8080


CMD ["/app/start.sh"]
