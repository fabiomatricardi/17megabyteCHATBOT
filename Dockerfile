FROM bitnami/minideb:latest

# Install build requirements
#RUN apt-get update &&   apt install --no-install-recommends -y build-essential gcc \
#   && rm -rf /var/lib/apt/lists/*
RUN apt update && apt install -y python3 python3-pip python3.11-venv

# Set the working directory
WORKDIR /app
# COPY requirements.txt /requirements.txt
COPY . .
RUN python3 -m venv venv 
RUN chmod +x *.sh && ./install.sh 
# Run the application
CMD ["./run_start.sh"]
