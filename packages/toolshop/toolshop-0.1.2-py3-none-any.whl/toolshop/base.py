from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Optional
from textwrap import dedent

import re

from .logging import logger


class Parameter(BaseModel):
    model_config = dict(extra="forbid") # No extra fields allowed

    name: str
    type: str 
    description: Optional[str] = None
    required: bool = True


class Documentation(BaseModel):
    model_config = dict(extra="forbid") # No extra fields allowed

    description: str
    parameters: Optional[list[Parameter]] = None
    usage: Optional[str] = None

    def __str__(self):
        parameter_string = "Args:\n"
        for p in self.parameters:
            if not p.required:
                type_string = f"{p.type}, optional"
            else:
                type_string = p.type
            
            parameter_string += f"    {p.name} ({type_string}): {p.description}\n"

        doc = dedent(self.description)
        doc += "\n\n" + dedent(parameter_string)

        if self.usage:
            doc += "\n\n" + dedent(self.usage)

        return doc


class Tool(ABC):
    def __init__(self, state = None, require_confirmation: bool = None):
        self.__name__ = self._camel_to_snake(self.__class__.__name__)
        self._state = state

        if hasattr(self, "_require_confirmation"):
            self.require_confirmation = getattr(self, "_require_confirmation")
        
        if require_confirmation is not None:
            self.require_confirmation = require_confirmation

        if self.call.__doc__:
            self.__doc__ = self.call.__doc__  

    @abstractmethod
    def call(self, *args, **kwargs):
        pass

    @staticmethod
    def _camel_to_snake(name):
        "Convert camel-case to snake-case."
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @property
    def state(self):
        if self._state:
            return self._state
        else:
            class NoOp:
                def __getattr__(self, name):
                    logger.info(f"No shared state provided for the tool. Ignoring call to self.state.{name} by returning a no-op function.")
                    return lambda *args, **kwargs: None

            return NoOp()
    

    def return_result_to_agent(self):
        if hasattr(self, "_return_result_to_agent"):
            return self._return_result_to_agent
        else:
            return True
    
    def log_header(self):
        logger.info(f"=== {self.__name__}() ===")

    def log_params(self, *args, **kwargs):
        if args:
            logger.info(f"args: {args}")

        if kwargs:
            kwarg_items = sorted(kwargs.items(), key=lambda x: len(str(x[1])))

            for k, v in kwarg_items:
                if isinstance(v, str) and "\n" in v:
                    logger.info(f"{k}:\n{v}")
                else:
                    logger.info(f"{k}: {v}")

    def log_result(self, result):
        logger.info(f"\nresult:\n{result}")

    def log_footer(self, result):
        logger.info("=" * len(f"=== {self.__name__}() ==="))

    def __call__(self, *args, **kwargs):
        self.log_header()
        self.log_params(*args, **kwargs)

        if hasattr(self, 'require_confirmation') and self.require_confirmation:
            confirmation = input(f"Do you want to allow agent to run {self.__name__}?  Type 'yes' to allow: ")
            if confirmation != "yes":
                raise Exception(f"Request to run {self.__name__} was denied by the user.")

        result = self.call(*args, **kwargs)
        self.log_result(result)
        self.log_footer(result)

        if self.return_result_to_agent():
            return result

    def to_marvin(self):
        import inspect

        # Create a new function that wraps 'self.__call__' following the exact signature of 'call'
        def partial_func(*args, **kwargs):
            return self.__call__(*args, **kwargs)

        partial_func.__signature__ = inspect.signature(self.call)
        partial_func.__doc__ = self.call.__doc__
        partial_func.__annotations__ = self.call.__annotations__
        partial_func.__name__ = self.__name__

        return partial_func

