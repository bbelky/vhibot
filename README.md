# Virtuozzo Hybrid Infrastructure Telegram Bot
### General purpose bot
While the initial purpose of this bot is to serve Virtuozzo-related question, you can use it as a basisi for your own bot by providing your own documentation or any kind of context. What is context?

This bot uses AI model together with Retrieval-augmented generation (RAG) approach. You can read more about RAG here https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/

### Create Telegram Bot
Find @BotFather in Telegram and follow the guide. Your main goal is to obtain API Token.

### Create OpenAI Account
Go to OpenAI https://openai.com/, create an account, go to API, and get the API Key.

### Run the bot using Docker compose
Clone the bot to your machine. It could be any Linux, Mac or Windows (Docker must be installed and configured):

    git clone https://github.com/bbelky/vhibot.git 

Create .env file in your working directory with the following content:

    OPENAI_API_KEY=your_openai_api_key
    TELEGRAM_API_TOKEN=your_telegram_api_key
    MODEL_NAME="gpt-3.5-turbo"
    EMB_MODEL_NAME="text-embedding-3-large"
    LOAD_TYPE="PDF"
    BETTERSTACK_TOKEN=your_betterstack_source_token
    FILE1_PATH='https://vhibot.s3.eu-central-1.amazonaws.com/vhiadm.pdf'
    FILE2_PATH='https://vhibot.s3.eu-central-1.amazonaws.com/vhissp.pdf'

Here:
- LOAD_TYPE can be PDF or JSON. Just upload your pdf or json-based documentation somewhere, add a link(s), and bot will use as a context. You can upload up to 2 files.
- Please add BETTERSTACK_TOKEN if you want to send logs to BetterStack. If you don't, just leave it empty.

Run docker compose:

    docker compose pull && docker compose up -d

Enjoy.
