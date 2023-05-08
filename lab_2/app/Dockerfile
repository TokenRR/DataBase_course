FROM python:3.11-bullseye AS base

WORKDIR /app
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends p7zip-full

RUN mkdir data
RUN cd data && wget https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO2021.7z \
    && 7z x -y OpenDataZNO2021.7z && rm OpenDataZNO2021.7z \
    && sed -i 's/,/./g' Odata2021File.csv \
    && sed -i 's/\"null\"/null/g' Odata2021File.csv \
    && mkdir OpenDataZNO2021 \
    && tail -n +2 Odata2021File.csv | split -d -a 6 -l 10000 - --filter='sh -c "{ head -n1 Odata2021File.csv; cat; } > OpenDataZNO2021/$FILE.csv"' part_ \
    && rm Odata2021File.csv
RUN cd data && wget https://zno.testportal.com.ua/yearstat/uploads/OpenDataZNO2020.7z \
    && 7z x -y OpenDataZNO2020.7z && rm OpenDataZNO2020.7z \
    && sed -i 's/,/./g' Odata2020File.csv \
    && mkdir OpenDataZNO2020 \
    && tail -n +2 Odata2020File.csv | split -d -a 6 -l 10000 - --filter='sh -c "{ head -n1 Odata2020File.csv; cat; } > OpenDataZNO2020/$FILE.csv"' part_ \
    && rm Odata2020File.csv

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["/bin/bash", "run.sh"]
