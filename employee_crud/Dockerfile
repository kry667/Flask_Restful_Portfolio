FROM python:3.11-slim-bookworm

WORKDIR /employee_crud

COPY ./requirements.txt requirements.txt
RUN /bin/bash -c "pip install --no-cache-dir --upgrade -r requirements.txt"

COPY . .

EXPOSE 5002

CMD ["/bin/bash", "-c", "python employee_crud.py"]