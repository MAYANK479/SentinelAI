FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install the missing ones
RUN pip install --no-cache-dir imbalanced-learn xgboost

COPY . .

EXPOSE 8000
# Ensure Python outputs everything immediately
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
