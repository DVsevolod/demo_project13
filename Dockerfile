FROM python:3.11-slim

WORKDIR /demo_project13

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run_game.py"]