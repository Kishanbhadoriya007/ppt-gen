# Dockerfile
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Create necessary directories that might be written to by the app
# and ensure the app user can write to them if running as non-root.
# GENERATED_PPTS_DIR will be /app/app/generated_ppts inside the container.
RUN mkdir -p /app/app/server_templates /app/app/generated_ppts/uploads \
    && chown -R 1000:1000 /app \
    && chmod -R 755 /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Tells uvicorn where to find the app, can also be set in CMD
# ENV MODULE_NAME="app.main"
# ENV VARIABLE_NAME="app"

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
# --no-cache-dir reduces image size
# --upgrade pip ensures pip is up to date
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code into the container
# This assumes your 'app' directory (with main.py, etc.) is in the same directory as the Dockerfile
COPY ./app /app/app

# Expose the port the app runs on (FastAPI default with Uvicorn)
EXPOSE 8000

# Optional: Switch to a non-root user for better security
# USER 1000

# Command to run the Uvicorn server
# This will run the FastAPI app instance named 'app' from the 'app/main.py' file.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]