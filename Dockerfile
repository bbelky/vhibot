FROM python:3.11 
# Or any preferred Python version.
ADD main.py .
COPY vhissp.pdf .
RUN pip3 install python-dotenv lxml bs4 unstructured beautifulsoup4 pypdf faiss-cpu openai langchain-openai certifi langchain python-telegram-bot
CMD ["python3", "./main.py"] 
# Or enter the name of your unique directory and parameter set.