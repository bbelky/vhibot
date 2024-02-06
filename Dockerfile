FROM python:3.11 
ADD main.py .
COPY vhissp.pdf .
#Load local .env file if needed
#COPY .env .
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "./main.py"] 
