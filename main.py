import os
import dotenv
from langchain_openai import OpenAIEmbeddings 
from langchain_community.vectorstores import FAISS 
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application

#Load local environment variables for local tests or comment for production:
#dotenv.load_dotenv()
bot_token = os.getenv("TELEGRAM_API_TOKEN")
openai_token = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME")
pdf_file1 = os.getenv("PDF_FILE1_PATH")
pdf_file2 = os.getenv("PDF_FILE2_PATH")

#Load PDF documents
loader1 = PyPDFLoader(pdf_file1)
loader2 = PyPDFLoader(pdf_file2)
loader_all = MergedDataLoader(loaders=[loader1, loader2])
pages = loader_all.load_and_split()

#Create FAISS DB
faissindex = FAISS.from_documents(pages, OpenAIEmbeddings())
faissindex.save_local("faiss_vhi_docs")

#Request to OpenAI
chatbot = RetrievalQA.from_chain_type( 
    llm=ChatOpenAI(
        openai_api_key=openai_token,
        temperature=0, model_name=model_name, max_tokens=500
    ),
    chain_type="stuff",
    retriever=FAISS.load_local("faiss_vhi_docs", OpenAIEmbeddings())
        .as_retriever(search_type="similarity", search_kwargs={"k":1})
)

template = """
{query} Respond with an example. 
"""

prompt = PromptTemplate( 
    input_variables=["query"], 
    template=template,
)
print("READY")

async def start_command(update, context):
  # Implement the start response
    await update.message.reply_text('Welcome to the AI-powered Virtuozzo Hybrid Infrastructure Support Bot!\nExample:\nHow to configure Kubernetes storage class?')

async def wiki_command(update, context):
  # Implement the wiki response
    await update.message.reply_html(
        "The list of how-to, integration examples and troubleshooting guides\n"
        "<a href='https://virtuozzo.atlassian.net/wiki/spaces/WIKI/pages/2681176121/Virtuozzo+Hybrid+Infrastructure/'>Wiki Pages</a>",
    )

async def docs_command(update, context):
  # Implement the wiki response
    await update.message.reply_html(
        "<a href='https://docs.virtuozzo.com/virtuozzo_hybrid_infrastructure_6_0_admins_guide/index.html'>Administrator's Guide</a>\n"
        "<a href='https://docs.virtuozzo.com/virtuozzo_hybrid_infrastructure_6_0_self_service_guide/index.html'>Self-service Guide</a>\n"
        "<a href='https://docs.virtuozzo.com/virtuozzo_hybrid_infrastructure_6_0_compute_api_reference/index.html'>Compute API Reference</a>\n"
        "<a href='https://docs.virtuozzo.com/virtuozzo_integrations_acronis_cyber_cloud_migration_from_vmware/index.html'>VMware Migration with Acronis Cyber Cloud</a>\n"
        "<a href='https://docs.virtuozzo.com/virtuozzo_integrations_hystax_migration_from_vmware/index.html'>VMware Migration with Hystax</a>\n"
        "<a href='https://docs.virtuozzo.com/master/index.html'>All documentation</a>",
    )

async def support_command(update, context):
  # Implement the wiki response
     await update.message.reply_html(
        "<a href='https://virtuozzo.zendesk.com/auth/v2/login/signin'>Create Ticket</a>\n"
        "<a href='https://support.virtuozzo.com/hc/en-us'>Support Portal</a>\n"
        "<a href='https://www.virtuozzo.com/all-supported-products/severity-level-definitions/'>Priority Definitions</a>",
    )

#handling chat message
async def handle_message(update, context):
  message = update.message.text
  chat_id = update.message.chat_id
  user = update.message.from_user
  first_name = user.first_name

  answer = chatbot.invoke( 
    prompt.format(query=message)
  )
  #await update.message.reply_text("Question:\n" + message + "\n" + "Answer:\n" + answer.get('result'))
  await update.message.reply_html(answer.get('result'))

#Polling Telegram bot
def main() -> None:

    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('wiki', wiki_command))
    application.add_handler(CommandHandler('docs', docs_command))
    application.add_handler(CommandHandler('support', support_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

    # Run the bot until you press Ctrl-C
    application.idle()

if __name__ == '__main__':
    main()