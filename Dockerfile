FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-cache


COPY . .

RUN mkdir -p /app/data

ENTRYPOINT ["python", "main.py"]