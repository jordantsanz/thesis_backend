FROM python:2.7
WORKDIR /app
COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8080
CMD ["gunicorn", "app:app", "-b", ":8080", "--timeout", "300"]

