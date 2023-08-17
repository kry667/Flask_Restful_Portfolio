# Use a specific Python version
FROM python:3.11

WORKDIR /app

# Copy requirements file first and install dependencies inside a virtual environment
COPY ./requirements.txt requirements.txt
RUN /bin/bash -c "pip install --no-cache-dir --upgrade -r requirements.txt"

# Copy the rest of the application code
COPY . .

# Expose port and start application
EXPOSE 5000
CMD ["/bin/bash", "-c", "python app.py"]
