FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 8000 for the API
EXPOSE 8000

# Run the FastAPI server using uvicorn
CMD ["uvicorn", "assistant:app", "--host", "0.0.0.0", "--port", "8000"]