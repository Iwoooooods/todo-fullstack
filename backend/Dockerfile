#build image
# Use an official Python runtime as a parent image
FROM python:3.12.2
# Set the working directory in the container
WORKDIR /backend
# Copy the current directory contents into the container at /app
COPY ./requirements.txt /backend/requirements.txt
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# Copy the rest of the application
COPY ./app /backend/app
#Expose port on host
EXPOSE 10086
# Run the application
CMD ["fastapi", "run", "app/main.py", "--port", "10086", "--host", "0.0.0.0"]
