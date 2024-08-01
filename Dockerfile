FROM python:3

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    musl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /car_parking

COPY requirements.txt /car_parking/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /car_parking

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
