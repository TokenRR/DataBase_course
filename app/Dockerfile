FROM python:3.9.7
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5432
CMD python main.py
