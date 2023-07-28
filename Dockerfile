FROM continuumio/miniconda3:latest

# Setting Working Directory
WORKDIR /backend

#Creating the environment
COPY ./backend/requirements.txt /backend/requirements.txt
RUN conda env create -f /backend/requirements.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "TheRoast", "/bin/bash", "-c"]

