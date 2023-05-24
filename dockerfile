FROM python:3.9
ENV PYTHONBUFFERED=1
ENV REDIS_HOST "redis"

# Set the working directory
WORKDIR /django

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN apt-get update && apt-get install libgl1 ffmpeg libsm6 libxext6 zbar-tools  -y && pip install "setuptools<58.0.0" && pip install --no-cache-dir -r requirements.txt

# export DJANGO_SETTINGS_MODULE=mysite.settings
# Copy the source code to the container
COPY . .
ENV PATH="py/bin:$PATH"
EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["sh","-c", "python manage.py makemigrations && python manage.py migrate && python3 manage.py initadmin && python manage.py runserver 0.0.0.0:8000"]
