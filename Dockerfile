FROM python:3.11 
ADD main.py .
COPY vhissp.pdf .
#Load local .env file if needed
#COPY .env .
RUN pip3 install -r requirements.txt
CMD ["python3", "./main.py"] 
