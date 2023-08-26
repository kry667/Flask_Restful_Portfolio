FROM python:3.11

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN /bin/bash -c "pip install --no-cache-dir --upgrade -r requirements.txt"

COPY . .

EXPOSE 5000
CMD ["/bin/bash", "-c", "python app.py"]