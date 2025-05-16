# Use the official Python base image
FROM python:3.9-slim

RUN mkdir /project

# Set the working directory inside the container
WORKDIR /project

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Específicamente copia el archivo de credenciales por separado también
COPY ./app/firebase/deathnote.json ./app/firebase/deathnote.json


# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]