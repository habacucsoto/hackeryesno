FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /hackeryesno
WORKDIR /hackeryesno
COPY requirements.txt /hackeryesno/
RUN pip install -r requirements.txt
COPY . /hackeryesno/
CMD python manage.py runserver 0.0.0.0:8080
