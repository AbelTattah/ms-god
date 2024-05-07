import os
# import pdf loader from langchain_community
from langchain_community.document_loaders import PyPDFLoader
# import the openai embeddings from langchain_openai
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# import the openai embeddings
from langchain_openai import OpenAIEmbeddings
# import the openai embeddings from langchain_openai
from langchain_community.vectorstores import Chroma
# Import create_retrieval_chain document for retrieval with the aid of an llm 
from langchain.chains.combine_documents import create_stuff_documents_chain
# Import ConversationalRetrievalChain for doc retrieval and chatbot question answering with the aid of an llm 
from langchain.chains import create_retrieval_chain
# Import Chat prompt template from langchain_core
from langchain_core.prompts import ChatPromptTemplate
# Import Chatmodel
from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv,find_dotenv

persist_directory = 'data/chroma/'
# Load the .env file
_ = load_dotenv(find_dotenv()) # read local .env file


# Set the openai api key
openai.api_key  = os.environ['OPENAI_API_KEY']

# Create an instance of the openai embeddings
embedding = OpenAIEmbeddings()

#Pdf content loading
loader1 = PyPDFLoader("./structure.pdf")
pages = loader1.load()

# Set the chunk size and overlap
chunk_size = 1500
chunk_overlap = 4

# Create an instance of the recursive character text splitter
r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=0,
    separators= ['\n\n', '\n',"(?<=\. )", " ",""]
)


# Split the documents
docs = r_splitter.split_documents(pages)

# Load the vector store
vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory=persist_directory
)

# Print the number of documents in the vector store
print(vectordb._collection.count())

# Set the llm
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Create a doc retriever
retriever=vectordb.as_retriever()


def qa(input):
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}""")

    # Create an instance of ConversationalRetrievalChain
    document_chain = create_stuff_documents_chain(llm, prompt)

    answer = create_retrieval_chain(retriever,document_chain)
    
    return answer.invoke({
        "input":input,
        "contex":"Computer Science, DCIT, Major, IT, Chemistry, Physics, Statistics, Minor, Level 100, Level 200, level 300, level 400, Semester"
    })