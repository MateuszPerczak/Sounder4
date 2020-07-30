FROM python:latest
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /home/sounder4
WORKDIR /home/sounder4
CMD ["python", "Sounder4.py"]