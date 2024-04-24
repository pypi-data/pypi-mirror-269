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
from dataclasses import dataclass

class Tool(ABC, BaseModel):
    """
        Tool is not built-in ability
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
        return await self.func.acall(*args, **kwargs)

@dataclass
class Action:
    name: str = ""
    action_input: str = ""