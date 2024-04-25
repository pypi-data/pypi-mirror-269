from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.schema.vectorstore import VectorStore
from langchain.schema.embeddings import Embeddings
from langchain.chains import RetrievalQA
from langchain.schema.language_model import BaseLanguageModel

from rag_doc_search.src.prompt_templates.default_prompt_templates import (
    DEFAULT_PROMPT_TEMPLATE,
    DEFAULT_CHAT_HISTORY_PROMPT,
)
from rag_doc_search.utils.miscellaneous import get_chat_history
from rag_doc_search.utils.miscellaneous import get_logger


class ChatBotModel:
    """
    A class representing the Base ChatBot.

    This class serves as an implementation of a base chatbot for diff LLM's.
    """

    def __init__(
        self, embeddings: Embeddings, vector_store: VectorStore, retriever_args: dict
    ):
        self.prompt_template = DEFAULT_PROMPT_TEMPLATE
        self.embeddings = (embeddings,)
        self.vector_store = vector_store
        self.logger = get_logger()
        self.retriever_args = retriever_args
        self.logger.info(
            f"search_type: {self.retriever_args.get('search_type')} \n search_args: {self.retriever_args.get('search_args')}"
        )

    def create_stream_manager(self, stream_handler, tracing) -> AsyncCallbackManager:
        """
        Creates and returns an instance of AsyncCallbackManager for handling asynchronous callbacks.

        Parameters:
        - `stream_handler`: The handler for managing the stream.
        - `tracing`: A boolean indicating whether tracing is enabled.

        Returns:
        An instance of AsyncCallbackManager.
        """
        manager = AsyncCallbackManager([])
        stream_manager = AsyncCallbackManager([stream_handler])
        if tracing:
            tracer = LangChainTracer()
            tracer.load_default_session()
            manager.add_handler(tracer)
            stream_manager.add_handler(tracer)

        return stream_manager

    def create_qa_chain(self, cl_llm: BaseLanguageModel) -> RetrievalQA:
        """
        Creates and returns an instance of RetrievalQA for question-answering using a provided language model.

        Parameters:
        - `cl_llm`: An instance of LanguageModel such as OpenAI or Bedrock Model.

        Returns:
        An instance of RetrievalQA.
        """
        PROMPT = PromptTemplate(
            template=self.prompt_template, input_variables=["context", "question"]
        )

        qa = RetrievalQA.from_chain_type(
            llm=cl_llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_type=self.retriever_args.get("search_type"),
                search_kwargs=self.retriever_args.get("search_args"),
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT},
        )
        return qa

    def create_conversational_qa_chain(
        self, cl_llm: BaseLanguageModel
    ) -> ConversationalRetrievalChain:
        """
        Creates and returns an instance of ConversationalRetrievalChain for handling conversational question-answering
        using a provided language model.

        Parameters:
        - `cl_llm`: An instance of LanguageModel such as OpenAI or Bedrock Model.

        Returns:
        An instance of ConversationalRetrievalChain.
        """
        memory_chain = ConversationBufferWindowMemory(
            memory_key="chat_history",
            ai_prefix="Assistant",
            return_messages=True,
            k=0,
            output_key="answer",
        )

        # the condense prompt for Claude
        condense_prompt = PromptTemplate.from_template(DEFAULT_CHAT_HISTORY_PROMPT)

        qa = ConversationalRetrievalChain.from_llm(
            llm=cl_llm,
            retriever=self.vector_store.as_retriever(
                search_type=self.retriever_args.get("search_type"),
                search_kwargs=self.retriever_args.get("search_args"),
            ),
            # return_source_documents=True,
            memory=memory_chain,
            get_chat_history=get_chat_history,
            condense_question_prompt=condense_prompt,
            chain_type="stuff",  # 'refine',
        )

        # the LLMChain prompt to get the answer. the ConversationalRetrievalChange does not expose this parameter in the constructor
        qa.combine_docs_chain.llm_chain.prompt = PromptTemplate.from_template(
            self.prompt_template
        )
        return qa
