FROM python3.11

COPY . /app

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

CMD ["python3". "src/main.py"]