FROM python:3
#install dependency
RUN pip install python-binance
RUN pip install numpy
COPY . /app
CMD ["python", "-u" ,"/app/main.py"]

