# base image
FROM python:3.8-slim-buster

#workdir
WORKDIR /app
#install python modules needed by the app
COPY requirements.txt requirements.txt
#RUN python -m venv venv
#RUN venv/bin/pip install --no-cache-dir -r ./requirements.txt
RUN pip3 install -r requirements.txt
#copy files required for the app run
COPY app migrations ./
COPY interview.py config.py ./
ENV FLASK_APP interview.py
#the port number the container should expose
EXPOSE 5000
#run the application
CMD ["python","-m","flask","run","--host=0.0.0.0"] 
