# Use the slim Debian variant to cut 800MB of bloat
FROM python:3.12.3-slim

# Prevent Python from writing .pyc files to disk and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install the system dependencies required for psycopg2 to compile
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application logic
COPY . .

# Expose the port documentation (does not actually publish the port)
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]