FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DATABASE_PATH=/data/students.db
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home --uid 10001 appuser
COPY backend/ ./backend/
COPY frontend/ ./frontend/
RUN mkdir -p /data && chown -R appuser:appuser /app /data
USER appuser
WORKDIR /app/backend
EXPOSE 5000
CMD ["python", "app.py"]
