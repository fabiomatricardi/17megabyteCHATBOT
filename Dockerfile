FROM bitnami/minideb:latest as builder

# Install build requirements
#RUN apt-get update &&   apt install --no-install-recommends -y build-essential gcc \
#   && rm -rf /var/lib/apt/lists/*
RUN install_packages python3 python3-pip python3.11-venv

# Set the working directory
WORKDIR /app
RUN python3 -m venv venv 
COPY requirements.txt ./requirements.txt
COPY install.sh /app/install.sh
RUN chmod +x *.sh && ./install.sh 

FROM bitnami/minideb:latest
RUN install_packages python3
WORKDIR /app
COPY --from=builder /app/venv /app/venv
COPY . .
RUN chmod +x *.sh
# Run the application
CMD ["./run_start.sh"]
