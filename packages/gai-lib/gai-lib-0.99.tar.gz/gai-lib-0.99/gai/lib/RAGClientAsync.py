import asyncio
import os
import json
import uuid
from gai.common.http_utils import http_post_async, http_get_async,http_delete_async
from gai.common.logging import getLogger
from gai.common.errors import ApiException
logger = getLogger(__name__)
logger.setLevel("DEBUG")
from gai.lib.ClientBase import ClientBase
import websockets
from gai.common.StatusListener import StatusListener

class RAGClientBase(ClientBase):
    
    def __init__(self,config_path=None):
        super().__init__(config_path)
        self.base_url = os.path.join(
            self.config["gai_url"], 
            self.config["generators"]["rag"]["url"].lstrip('/'))
        logger.debug(f'base_url={self.base_url}')

    def _prepare_files_and_metadata(self, collection_name, file_path, metadata):
        mode = 'rb' if file_path.endswith('.pdf') else 'r'
        with open(file_path, mode) as f:
            files = {
                "file": (os.path.basename(file_path), f if mode == 'rb' else f.read(), "application/pdf"),
                "metadata": (None, json.dumps(metadata), "application/json"),
                "collection_name": (None, collection_name, "text/plain")
            }
            return files

class RAGClientAsync(RAGClientBase):

    def __init__(self,config_path=None):
        super().__init__(config_path)

    ### ----------------- INDEXING ----------------- ###

    # Provides an updater to get chunk indexing status
    # NOTE: The update is only relevant if this library is used in a FastAPI application with a websocket connection
    async def index_file_async(
        self, 
        collection_name, 
        file_path, 
        title="",
        source="",
        authors="",
        publisher="",
        published_date="",
        comments="",
        keywords="", 
        listener_callback=None):
        
        url=os.path.join(self.base_url,"index-file")
        metadata = {
            "title": title,
            "source": source,
            "authors": authors,
            "publisher": publisher,
            "published_date": published_date,
            "comments": comments,
            "keywords": keywords
        }

        # Send file
        async def send():
            try:
                mode = 'rb'
                with open(file_path, mode) as f:
                    files = {
                        "file": (os.path.basename(file_path), f, "application/pdf"),
                        "metadata": (None, json.dumps(metadata), "application/json"),
                        "collection_name": (None, collection_name, "text/plain")
                    }
                    response = await http_post_async(url=url, files=files)
                    return response
            except Exception as e:
                logger.error(e)
                raise e
    
        if listener_callback:
            try:
                # Create listener
                ws_url=os.path.join(self.base_url,f"index-file/ws").replace("http","ws")
                listener = StatusListener(ws_url, collection_name)

                # Start both tasks and return when first task completes then cancel the other
                send_task=asyncio.create_task(send())
                listen_task=asyncio.create_task(listener.listen(listener_callback))
                pending, done = await asyncio.wait([send_task], return_when=asyncio.FIRST_COMPLETED)
                listen_task.cancel()
            except Exception as e:
                logger.error(e)
                raise e
        else:
            await send()

        logger.info("Indexing complete.")

    ### ----------------- RETRIEVAL ----------------- ###

    async def retrieve_async(self, collection_name, query_texts, n_results=None):
        url = os.path.join(self.base_url,"retrieve")
        data = {
            "collection_name": collection_name,
            "query_texts": query_texts
        }
        if n_results:
            data["n_results"] = n_results

        response = await http_post_async(url, data=data)
        return response

#Collections-------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_collection_async(self, collection_name):
        url = os.path.join(self.base_url,"collection",collection_name)
        logger.info(f"RAGClient.delete_collection: Deleting collection {url}")
        try:
            response = await http_delete_async(url)
        except ApiException as e:
            if e.code == 'collection_not_found':
                return {"count":0}
            logger.error(e)
            raise e
        return json.loads(response.text)

    async def list_collections_async(self):
        url = os.path.join(self.base_url,"collections")
        response = await http_get_async(url)
        return json.loads(response.text)

#Documents-------------------------------------------------------------------------------------------------------------------------------------------

    async def list_documents_async(self):
        url = os.path.join(self.base_url,"documents")
        response = await http_get_async(url)
        return json.loads(response.text)

    async def delete_document_async(self,collection_name,document_id):
        url = os.path.join(self.base_url,f"document/{collection_name}/{document_id}")
        response = await http_delete_async(url)
        return json.loads(response.text)
    
