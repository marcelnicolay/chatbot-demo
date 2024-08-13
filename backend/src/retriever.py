from contextvars import ContextVar
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader


from src.config import Settings, get_settings


class VectorStore:
    """Setup and contain our retriver."""

    def __init__(self, settings: Settings):
        self._retriever: ContextVar[VectorStoreRetriever] = ContextVar('_retriever')
        self.persist_directory = settings.vectorstore_persist_directory
        self.vectorstore_load_dir = settings.vectorstore_load_dir
        self.settings = settings
        self.load_vectorstore()

    def load_vectorstore(self):
        vectorstore = Chroma(persist_directory=self.persist_directory, embedding_function=OpenAIEmbeddings(api_key=self.settings.openai_api_key))
        _retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        self._retriever.set(_retriever)

    @property
    def retriever(self):
        return self._retriever.get()

    def load_and_save_vectorstore(self):
        loader = DirectoryLoader(self.vectorstore_load_dir, show_progress=True)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=self.settings.openai_api_key), persist_directory=self.persist_directory)
        vectorstore.persist()

        self.load_vectorstore()


vs = VectorStore(get_settings())


if __name__ == "__main__":
    vs.load_and_save_vectorstore()