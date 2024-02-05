# Virtuozzo Hybrid Infrastructure Support Bot
### To run the bot using docker compose
Clone the bot to your machine:

    git clone https://github.com/bbelky/vhibot.git 

Create .env file in your working directory with the following content:

    OPENAI_API_KEY=your_openai_api_key
    TELEGRAM_API_TOKEN=your_telegram_api_key
    PDF_FILE_PATH='vhissp.pdf'

Run docker compose:

    docker compose up -d

Enjoy.
