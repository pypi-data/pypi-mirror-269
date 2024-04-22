from typing import (Optional,
                    List
                    )
from bson.objectid import ObjectId
from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic import parse_obj_as

from sharedkernel.string_extentions import camel_to_snake
from .adapter import MongoDBClient


from sharedkernel.exception.exception import BusinessException
from sharedkernel.enum.error_code import ErrorCode

mongo_client= MongoDBClient()

ResultT = TypeVar("ResultT")

T = TypeVar("T", bound=BaseModel)

class RepositoryBase(Generic[T]):
    
    def __init__(self,model):
      self.model = model
      self.model_name= camel_to_snake(self.model.__name__)
      
      
    def find(self,id: str) -> T:
        if (not ObjectId.is_valid(id)):
            raise BusinessException(ErrorCode.Item_NotFound)
        
        query = {"_id": ObjectId(id),"is_deleted":False}
        
        item = mongo_client.domain[self.model_name].find_one(query)
        
        if (not item):
            raise BusinessException(ErrorCode.Item_NotFound)
        
        item['_id']=str(item['_id'])
        item['id']= item['_id']
        item.pop('_id')

        return self.model.parse_obj(item) if item else None
    
        
    def get_all(self,query:dict = None) -> Optional[List]:
        if query:
            query["is_deleted"]= False
        else:
            query= {"is_deleted":False}
        items = list(mongo_client.domain[self.model_name].find(query))

        for item in items:
            item['_id'] = str(item['_id'])
            item['id']= item['_id']
            item.pop('_id')
        
        return parse_obj_as(List[self.model],items)
    

    def insert(self, insert_data: T) -> str:
        delattr(insert_data, "id")
        inserted_data= mongo_client.domain[self.model_name].insert_one(insert_data.dict())
        
        return str(inserted_data.inserted_id)
    
    def bulk_insert(self, insert_data: List[T]):
        insert_data=[delattr(data, "id") for data in insert_data]
        mongo_client.domain[self.model_name].insert_many(insert_data)



    def update(self,id:str,update_data: T):
        query = {"_id": ObjectId(id)}
        delattr(update_data, "id")
        mongo_client.domain[self.model_name].update_one(query,  {"$set": update_data.dict()}, upsert=False)
        

    def query(self):
        return mongo_client.domain[self.model_name]
        