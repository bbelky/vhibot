import os
import dotenv
from langchain_openai import OpenAIEmbeddings 
from langchain_community.vectorstores import FAISS 
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application

dotenv.load_dotenv()
bot_token = os.getenv("TELEGRAM_API_TOKEN")
openai_token = os.getenv("OPENAI_API_KEY")
pdf_file = os.getenv("PDF_FILE_PATH")
#print(bot_token)

#Load PDF documents
loader = PyPDFLoader(pdf_file)
pages = loader.load_and_split()

#Create FAISS DB
faissindex = FAISS.from_documents(pages, OpenAIEmbeddings())
faissindex.save_local("faiss_vhi_docs")

#Request to OpenAI
chatbot = RetrievalQA.from_chain_type( 
    llm=ChatOpenAI(
        openai_api_key=openai_token,
        temperature=0, model_name="gpt-3.5-turbo", max_tokens=500
    ),
    chain_type="stuff",
    retriever=FAISS.load_local("faiss_vhissp_docs", OpenAIEmbeddings())
        .as_retriever(search_type="similarity", search_kwargs={"k":1})
)

template = """
{query} Respons with an example. 
"""

prompt = PromptTemplate( 
    input_variables=["query"], 
    template=template,
)
print("READY")

async def start_command(update, context):
  # Implement the start response
    await update.message.reply_text('Hello! Welcome to Virtuozzo Hybrid Infrastructure Support Bot!\nExample:\nHow to configure Kubernetes storage class?')

#handling chat message
async def handle_message(update, context):
  message = update.message.text
  chat_id = update.message.chat_id
  user = update.message.from_user
  first_name = user.first_name

  answer = chatbot.invoke( 
    prompt.format(query=message)
  )
  await update.message.reply_text("Question:\n" + message + "\n" + "Answer:\n" + answer)

#Polling Telegram bot
def main() -> None:

    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

    # Run the bot until you press Ctrl-C
    application.idle()

if __name__ == '__main__':
    main()