FROM python:3.11-slim

WORKDIR /winter

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app/winter.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["python", "app/winter.py"]