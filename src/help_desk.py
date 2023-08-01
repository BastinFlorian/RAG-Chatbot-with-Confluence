import sys
import load_db
import collections

# Build prompt
# Prompt template
from langchain.prompts import PromptTemplate

sys.path.append('../')
from config import PERSIST_DIRECTORY


class HelpDesk():
    """Create the necessary objects to create a QARetrieval chain"""
    def __init__(self, new_db=True):
        self.template = self._get_template()
        self.persist_directory = PERSIST_DIRECTORY

        self.embeddings = self._get_embeddings()

        if new_db:
            self.db = load_db.DataLoader().set_db(self.embeddings)
        else:
            self.db = load_db.DataLoader().get_db(self.embeddings)

        self.retriever = self.db.as_retriever()
        self.prompt = self._load_prompt(self.template)

        self.llm = self._get_llm()
        self.retrieval_qa_chain = self._load_retrieval_qa()

    def _get_template(self):
        template = """
        Given this text extracts:
        -----
        {context}
        -----
        Please answer with to the following question:
        Question: {question}
        Helpful Answer:
        """
        return template

    def _load_prompt(self, template):
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        return prompt

    def _get_embeddings(self):
        from langchain.embeddings import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
        return embeddings

    def _get_llm(self):
        from langchain.llms import OpenAI
        llm = OpenAI()
        return llm

    def _load_retrieval_qa(self):
        from langchain.chains import RetrievalQA
        chain_type_kwargs = {"prompt": self.prompt}
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
        )
        return qa

    def retrieval_qa_inference(self, question):
        query = {"query": question}
        answer = self.retrieval_qa_chain(query)
        sources = self.list_top_k_sources(answer, k=2)
        print(sources)

        return answer["result"], sources

    def list_top_k_sources(self, answer, k=2):
        # Display sources as [title_of_source](source_url)
        sources = [f'[{res.metadata["title"]}]({res.metadata["source"]})' for res in answer["source_documents"]]
        if sources:
            k = min(k, len(sources))
            distinct_sources = list(zip(*collections.Counter(sources).most_common()))[0][:k]
            distinct_sources_str = "  \n- ".join(distinct_sources)
        if len(distinct_sources) == 1:
            return f"Voici la source qui pourrait t'être utile :  \n- {distinct_sources_str}"
        elif len(distinct_sources) > 1:
            return f"Voici {len(distinct_sources)} sources qui pourraient t'être utiles :  \n- {distinct_sources_str}"
        else:
            return "Désolé je n'ai trouvé aucune ressource pour répondre à ta question"
