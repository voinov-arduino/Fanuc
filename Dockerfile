FROM python:3.8

WORKDIR /lidar

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ./eip_driver

CMD ["python", "main.py"]

CMD ["bash"]