from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from autocoder.common import SourceCode,AutoCoderArgs
from autocoder.common.llm_rerank import LLMRerank

from byzerllm.apps.llama_index.simple_retrieval import SimpleRetrieval
from byzerllm.apps.llama_index import get_service_context,get_storage_context
from llama_index.core import QueryBundle
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.core.node_parser import SentenceSplitter,SentenceWindowNodeParser
from llama_index.core.indices.document_summary import DocumentSummaryIndex
from llama_index.core.base.llms.types import ChatMessage,MessageRole
import byzerllm
from loguru import logger

class SimpleRAG:
    def __init__(self,llm,args:AutoCoderArgs,path:str) -> None:
        self.llm = llm
        self.args = args
        self.retrieval = byzerllm.ByzerRetrieval()
        self.retrieval.launch_gateway()        
        self.path = path
        self.namespace = "default"
        self.chunk_collection = "default"
        self.service_context = get_service_context(self.llm)
        self.storage_context = get_storage_context(self.llm,self.retrieval,
                                                   chunk_collection=self.chunk_collection,
                                                   namespace=self.namespace)

    def stream_search(self,query:str):     
        query_bundle = QueryBundle(query_str=query)   
        index = VectorStoreIndex.from_vector_store(vector_store = self.storage_context.vector_store,
                                                   service_context=self.service_context)
        query_engine = index.as_query_engine(streaming=True)                
        streaming_response = query_engine.query(query_bundle)
        contexts = []
        for node in streaming_response.source_nodes:
            contexts.append({
                "raw_chunk":node.node.text,
                "doc_url":node.node.metadata["file_path"],
                "_id":node.node.id_,
                
            })
        return streaming_response.response_gen,contexts 
    
    def retrieve(self,query:str)->List[SourceCode]:
        query_bundle = QueryBundle(query_str=query)
        index = VectorStoreIndex.from_vector_store(vector_store = self.storage_context.vector_store,
                                                   service_context=self.service_context)
        retrieval_engine = index.as_retriever()
        nodes = retrieval_engine.retrieve(query_bundle)        
        reranker = LLMRerank(llm=self.llm)
        retrieved_nodes = reranker.postprocess_nodes(nodes, query_bundle,choice_batch_size=5, top_n=1)
        return [
            {
                "raw_chunk":node.node.text,
                "doc_url":node.node.metadata["file_path"],
                "_id":node.node.id_,
                
            } for node in retrieved_nodes
        ]
    
    def stream_chat_oai(self,conversations, model:Optional[str]=None, role_mapping=None,llm_config:Dict[str,Any]={}):        
        index = VectorStoreIndex.from_vector_store(vector_store = self.storage_context.vector_store,
                                                   service_context=self.service_context)
        chat_engine = index.as_chat_engine(
            chat_mode="condense_plus_context",                       
            verbose=False,
        )
        history = []
        for conv in conversations[:-1]:
            if conv["role"] == "user":
                role = MessageRole.USER
            elif conv["role"] == "assistant":
                role = MessageRole.ASSISTANT    
            else:
                role = MessageRole.SYSTEM
            history.append(ChatMessage(role=role,content=conv["content"]))
        return chat_engine.stream_chat(conversations[-1]["content"],chat_history=history).response_gen,[]
        

    def stream_chat_repl(self,query:str):
        from llama_index.core.memory import ChatMemoryBuffer

        memory = ChatMemoryBuffer.from_defaults(token_limit=8092)
        index = VectorStoreIndex.from_vector_store(vector_store = self.storage_context.vector_store,
                                                   service_context=self.service_context)

        chat_engine = index.as_chat_engine(
            chat_mode="condense_plus_context",
            memory=memory,            
            verbose=False,
        )
        chat_engine.streaming_chat_repl()  
    
    def search(self,query:str) -> List[SourceCode]:
        if self.args.enable_rag_search:
            texts,contexts = self.stream_search(query)
            s = "".join([text for text in texts])
            urls = ",".join(set([context["doc_url"] for context in contexts]))
            ## append RAG: prefix is used to protect avoid the source code is modified by the code auto execute
            return [SourceCode(module_name=f"RAG:{urls}", source_code=s)]
        elif self.args.enable_rag_context:
            contexts = self.retrieve(query) 
            for context in contexts:  
                context["raw_chunk"]
                try:
                    with open(context["doc_url"],"r") as f:
                        context["raw_chunk"] = f.read()
                except Exception as e:
                    logger.warning(f"Error reading file {context['doc_url']}")
                    pass

            return [SourceCode(module_name=context["doc_url"], source_code=context["raw_chunk"]) for context in contexts]
        return []

    def build(self):            
        retrieval_client = SimpleRetrieval(llm=self.llm,retrieval=self.retrieval)
        retrieval_client.delete_from_doc_collection(self.namespace)
        retrieval_client.delete_from_chunk_collection(self.chunk_collection)
        
        required_exts = self.args.required_exts or None
        documents = SimpleDirectoryReader(self.path,
                                          recursive=True,
                                          filename_as_id=True,
                                          required_exts=required_exts).load_data()        

        sp = SentenceSplitter(chunk_size=1024, chunk_overlap=0)        

        nodes = sp.get_nodes_from_documents(
            documents, show_progress=True
        )
        _ = VectorStoreIndex(nodes=nodes,
                             store_nodes_override=True,
                             storage_context=self.storage_context, 
                             service_context=self.service_context)        
        
                
        
                    