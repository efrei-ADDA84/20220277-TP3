FROM python:3.11.0

# set the working directory in the container
WORKDIR /weather-api

# ADD all files 
COPY . .

# install required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# command to run on container start
CMD [ "python3", "main.py" ]

