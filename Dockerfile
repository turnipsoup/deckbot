FROM python:3.9.4-buster

# Update the repositories, and install some stuff for us
RUN apt-get update && apt-get install git

# Make /app directory and navigate to it
RUN mkdir /app
WORKDIR /app

# Clone the master version of the respository
RUN git clone https://github.com/turnipsoup/deckbot.git
WORKDIR /app/deckbot

RUN pip3 install -r requirements.txt

# Start the application
CMD ["python3", "deck.py"]

