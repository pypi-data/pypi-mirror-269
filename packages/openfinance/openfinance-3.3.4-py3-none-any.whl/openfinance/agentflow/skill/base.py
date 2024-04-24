import asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from pydantic import BaseModel
from abc import ABC, abstractmethod

class Skill(ABC, BaseModel):
    """
        Skills is built-in ability
    """
    name: str
    description: str
    func: Callable    

    def __call__(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        return self.call(*args, **kwargs)

    def call(
        self,
        *args: Any,
        **kwargs: Any        
    ) -> Any:
        return self.func(*args, **kwargs)
    
    async def _acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        return await self.acall(*args, **kwargs)

    async def acall(
        self,
        *args: Any,        
        **kwargs: Any        
    ) -> Any:
        return await self.func(*args, **kwargs)