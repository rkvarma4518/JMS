# Use a base image that has Python already installed
FROM python:3.8

# Install system dependencies
RUN apt-get update && apt-get install -y git

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install torch separately
RUN pip install --no-cache-dir torch torchvision

# Clone detectron2 from GitHub
RUN pip install --no-cache-dir git+https://github.com/facebookresearch/detectron2.git@dd2db71b0f8d855b71cac655186cbddca1bfda93

# Copy your application code
COPY . .

# Specify the command to run on container start
CMD ["python", "app.py"]
