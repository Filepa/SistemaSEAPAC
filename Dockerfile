FROM python:3.12-slim

WORKDIR /app

# Instala netcat (nc)
RUN apt-get update && apt-get install -y netcat-traditional && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]