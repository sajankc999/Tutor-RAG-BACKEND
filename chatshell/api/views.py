from rest_framework.views import APIView
from chatshell.api.serializers import AskQuerySerializer
from chatshell.embeddings.vector_store import vector_store
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from Pleias_RAG_Library.pleias_rag_interface import RAGWithCitations
from langchain.chains.retrieval_qa.base import RetrievalQA

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.prompts import PromptTemplate

model_name = "PleIAs/Pleias-RAG-350M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=100,      # short, concise replies
                do_sample=True,         # allows some variability
                temperature=0.5,        # lower = more focused/shorter
                top_p=0.9,              # typical nucleus sampling
                   )
llm = HuggingFacePipeline(pipeline=pipe)




PROMPT_TEMPLATE = """
You are a friendly, Tutor.
Use the following context to answer the question. Include metadata information if present.
Only answer if relevant. If no information is available, say "No answer found."
You can use metadata for reasoning and answer generation.

{context}

Question: {question}
Answer:
"""

prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "question"]
)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt":prompt}
)            

rag = RAGWithCitations("PleIAs/Pleias-RAG-350M")


class AskQueryView(APIView):
    
    def post(self,request,*args, **kwargs):
        #get query
        serializer = AskQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get('query')
        metadata_filter = serializer.validated_data.get("metadata_filter",None)

        if metadata_filter:
            docs = retriever.get_relevant_documents(query, filter=metadata_filter)
        else:
            docs = retriever.get_relevant_documents(query)
        sources = [
            {"text": doc.page_content, "metadata": doc.metadata}
            for doc in docs
        ]
        response = rag.generate(query=query, sources=sources)

        clean_answer = response.get("processed", {}).get("clean_answer", "No answer found.")

        return Response({
            "answer": response,
            "source":sources
            # "sources": sources  
        }, status=HTTP_200_OK)



        