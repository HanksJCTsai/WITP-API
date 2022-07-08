FROM harbor.wistron.com/base_image/python:3.7-stretch
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
# Set external port
EXPOSE 8000
# CMD: python manage.py runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]