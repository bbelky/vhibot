# Virtuozzo Hybrid Infrastructure Telegram Bot
### General purpose bot
While the initial purpose of this bot is to serve Virtuozzo-related questions, you can use it as a basis for your own bot by providing your documentation or any kind of context. What is context?

This bot uses the OpenAI GPT model together with the Retrieval-augmented generation (RAG) approach. You can read more about RAG here https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/

### Create Telegram Bot
Find @BotFather on Telegram and follow the guide. Your main goal is to obtain an API Token.

### Create OpenAI Account
Go to OpenAI https://openai.com/, create an account, go to API, and get the API Key.

### Run the bot using Docker compose
Clone the bot to your machine. It could be any Linux, Mac, or Windows (Docker must be installed and configured):

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

- OPENAI_API_KEY - the API Key you got from OpenAI
- TELEGRAM_API_TOKEN - the API Token you got from @BotFather
- MODEL_NAME - the name of OpenAI model. I recommend using 'gpt-3.5-turbo' as it is enough in most cases, but you can find more models (and pricing) here https://openai.com/pricing
- EMB_MODEL_NAME - model name for embeddings, If your context page is small, you can switch to 'text-embedding-3-small'
- LOAD_TYPE can be PDF or JSON. Just upload your PDF or JSON-based documentation somewhere, add a link(s), and the bot will use it as a context. You can upload up to 2 files, or more if you change the code a little bit.
- Please add BETTERSTACK_TOKEN if you want to send logs to BetterStack https://betterstack.com/. If you don't, just leave it empty.
- FILE1_PATH and FILE2_PATH - links (and only public HTTP links are supported) to your PDF or JSON files. I recommend using any S3 service. If you have only a single file, leave the second one empty.

Run docker compose:

    docker compose pull && docker compose up -d

Enjoy.
