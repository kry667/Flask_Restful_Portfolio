FROM python:3.11-slim-bookworm

WORKDIR /user_crud

COPY ./requirements.txt requirements.txt
RUN /bin/bash -c "pip install --no-cache-dir --upgrade -r requirements.txt"

COPY . .

EXPOSE 5001

CMD ["/bin/bash", "-c", "python user_crud.py"]