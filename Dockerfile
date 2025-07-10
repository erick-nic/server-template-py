FROM python:3.13.3-slim

WORKDIR /server
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./server /server

COPY ./server/requirements.txt /server/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


