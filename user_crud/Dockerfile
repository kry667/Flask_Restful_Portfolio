# Use a specific Python version
FROM python:3.11

WORKDIR /user_crud

# Copy requirements file first and install dependencies inside a virtual environment
COPY ./requirements.txt requirements.txt
RUN /bin/bash -c "pip install --no-cache-dir --upgrade -r requirements.txt"

# Copy the rest of the application code
COPY . .

# Expose port (if needed)
EXPOSE 5001

# Set environment variable
ENV VARIABLE_NAME=user_var
ENV MYSQL_HOST=db
ENV MYSQL_USER=my-user
ENV MYSQL_PASSWORD=my-password
ENV MYSQL_DB=my-database

# Command to run your user_crud script
CMD ["/bin/bash", "-c", "python user_crud.py"]
