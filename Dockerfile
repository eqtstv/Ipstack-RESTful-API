# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Secret environment variables (added only for testing convenience) 
ENV IPSTACK_API_KEY="19d069d348570854675a5a2124ed8473"
ENV JWT_SECRET_KEY="1234"
ENV DATABASE_HOST="ec2-54-228-9-90.eu-west-1.compute.amazonaws.com"
ENV DATABASE_USER="hngkhrhthjjyxa"
ENV DATABASE_PASSWORD="80a554f0070d11d7cff5e18b1abd0d4a4b00a4acbb66eabe738170c17fda2941"
ENV DATABASE_DATABASE="dee49njhpmq673"

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app


CMD ["python", "run.py", "production"]