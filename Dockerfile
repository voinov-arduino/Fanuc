FROM python:3.10

WORKDIR /lidar

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ./eip_driver

CMD ["python", "main.py"]