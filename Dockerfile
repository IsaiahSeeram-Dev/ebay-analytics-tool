# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy everything into container
COPY . . 

# Install dependencies 
RUN pip install flask requests

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
