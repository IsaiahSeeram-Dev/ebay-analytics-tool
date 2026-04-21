# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything into container
COPY . /app

# Install dependencies 
RUN pip install flask gunicorn

# Expose port
EXPOSE 5000

# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
