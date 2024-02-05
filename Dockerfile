FROM python:3.11 
ADD main.py .
COPY vhissp.pdf .
#Load local .env file if needed
#COPY .env .
RUN pip3 install python-dotenv lxml bs4 unstructured beautifulsoup4 pypdf faiss-cpu openai langchain-openai certifi langchain python-telegram-bot
CMD ["python3", "./main.py"] 
