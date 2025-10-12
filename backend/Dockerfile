# Stage 1: Test runner
FROM python:3.11-slim AS test

WORKDIR /app

# Install dependencies, including test dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run tests
CMD ["pytest"]

# Stage 2: Production build
FROM python:3.11-slim AS production

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
