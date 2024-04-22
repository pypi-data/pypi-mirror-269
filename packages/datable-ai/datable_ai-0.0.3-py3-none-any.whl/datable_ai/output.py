import os
import tiktoken
from datable_ai.core.llm import LLM_TYPE, create_llm

from langchain.chains.summarize import load_summarize_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import CharacterTextSplitter
from langchain.docstore.document import Document


class Output:
    def __init__(
        self,
        llm_type: LLM_TYPE,
        prompt_template: str,
    ) -> None:
        self.llm_type = llm_type
        self.prompt_template = prompt_template
        self.prompt = ChatPromptTemplate.from_template(self.prompt_template)
        self.llm = create_llm(self.llm_type)
        self.encoding_name = self._encoding_name()

    def invoke(self, **kwargs):
        try:
            summarized_kwargs = {}
            for key, value in kwargs.items():
                num_tokens = self._num_tokens_from_string(value)
                if num_tokens > 8000:
                    summarized_value = self._summarize(value)
                    summarized_kwargs[key] = summarized_value["output_text"]
                else:
                    summarized_kwargs[key] = value

            chain = self.prompt | self.llm | StrOutputParser()
            return chain.invoke(summarized_kwargs)
        except Exception as e:
            raise RuntimeError(f"Error invoking Output: {str(e)}") from e

    def _num_tokens_from_string(self, text: str) -> int:
        try:
            encoding = tiktoken.encoding_for_model(self.encoding_name)
            num_tokens = len(encoding.encode(text))
            return num_tokens
        except Exception as e:
            raise RuntimeError(f"Error calculating number of tokens: {str(e)}") from e

    def _summarize(self, long_text: str):
        try:
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=7000, chunk_overlap=100
            )
            split_docs = text_splitter.split_text(long_text)
            docs = [Document(page_content=chunk) for chunk in split_docs]
            return load_summarize_chain(
                self.llm, chain_type="map_reduce", verbose=False
            ).invoke(docs)
        except Exception as e:
            raise RuntimeError(f"Error summarizing text: {str(e)}") from e

    def _encoding_name(self):
        if self.llm_type == LLM_TYPE.OPENAI:
            return os.environ.get("OPENAI_API_MODEL")
        elif self.llm_type == LLM_TYPE.AZURE_OPENAI:
            return os.environ.get("AZURE_OPENAI_API_MODEL")
        elif self.llm_type == LLM_TYPE.ANTHROPIC:
            return os.environ.get("ANTHROPIC_API_MODEL")
        else:
            raise ValueError(f"Unsupported LLM type: {self.llm_type}")
