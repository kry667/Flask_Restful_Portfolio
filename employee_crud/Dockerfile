# Use a specific Python version
FROM python:3.11

WORKDIR /employee_crud

# Copy requirements file first and install dependencies inside a virtual environment
COPY ./requirements.txt requirements.txt
RUN /bin/bash -c "pip install --no-cache-dir --upgrade -r requirements.txt"

# Copy the rest of the application code
COPY . .

# Expose port (if needed)
# EXPOSE 5000

# Set environment variables
ENV MYSQL_HOST=db
ENV MYSQL_USER=my-user
ENV MYSQL_PASSWORD=my-password
ENV MYSQL_DB=my-database
ENV VARIABLE_NAME=employee_var

# Command to run your user_crud script
CMD ["/bin/bash", "-c", "python employee_crud.py"]