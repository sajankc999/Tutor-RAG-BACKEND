from rest_framework.views import APIView
from chatshell.api.serializers import AskQuerySerializer
from chatshell.embeddings.vector_store import vector_store
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# from Pleias_RAG_Library.pleias_rag_interface import RAGWithCitations
# from langchain.chains.retrieval_qa.base import RetrievalQA

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from google import genai
from langchain_huggingface import HuggingFaceEmbeddings

from chatshell.enums import get_dict_value


client = genai.Client()




"""Model to run locally """
# model_name = "PleIAs/Pleias-RAG-350M"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# pipe = pipeline(
#                 "text-generation",
#                 model=model,
#                 tokenizer=tokenizer,
#                 max_new_tokens=100,      # short, concise replies
#                 do_sample=True,         # allows some variability
#                 temperature=0.5,        # lower = more focused/shorter
#                 top_p=0.9,              # typical nucleus sampling
#                    )
# llm = HuggingFacePipeline(pipeline=pipe)




PROMPT_TEMPLATE = """

{persona}

{context}

---

Answer the question based on the above context: {question}
"""



# retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# qa = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=retriever,
#     chain_type_kwargs={"prompt":prompt}
# )            

# rag = RAGWithCitations("PleIAs/Pleias-RAG-350M")
db = vector_store
class AskQueryView(APIView):
    
    def post(self,request,*args, **kwargs):
        #get query
        serializer = AskQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data.get('query')
        personality_id = serializer.validated_data.get("personality_id",None)
        metadata_filter = serializer.validated_data.get("metadata_filter",None)


        persona_text = get_dict_value(personality_id)


        if not metadata_filter:
            results = db.similarity_search_with_relevance_scores(query,k=3)
        else:
            results = db.similarity_search_with_relevance_scores(query,k=3,filter=metadata_filter)

        
        if len(results) == 0 or results[0][1] < 0.5:
            print(f"Unable to find matching results.")
            return Response(
                {
                "detail":"Unable to gather response.",
                "score":results[0][1],

                 }
            )
        

        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["personality","context", "question"]
        )

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(persona=persona_text,context=context_text, question=query)
        print(prompt)


        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt.format(persona=persona_text,context=context_text,question = query)
        )
        answer_text = getattr(response, "text", None) or getattr(response, "candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No answer found.")

        return Response({
            # "response": response,
            "answer":answer_text,
            "source": [doc.metadata for doc, _score in results],
            "query": query,
            "personality_id":personality_id
        }, status=HTTP_200_OK)



        