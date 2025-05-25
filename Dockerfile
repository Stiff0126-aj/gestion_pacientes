FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["gunicorn", "gestion_pacientes_ms.wsgi:application", "--bind", "0.0.0.0:8080"]
