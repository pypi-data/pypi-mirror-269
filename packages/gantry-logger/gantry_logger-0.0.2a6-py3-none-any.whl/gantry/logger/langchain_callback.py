import atexit
import collections
import dataclasses
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence
from uuid import UUID

from gantry.logger.eval_logger import EvalLogger, Record

try:
    from langchain.callbacks.base import BaseCallbackHandler
    from langchain.schema import LLMResult
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.documents import Document
    from langchain_core.load.serializable import Serializable
    from langchain_core.messages import BaseMessage
except ImportError:
    raise RuntimeError("Please run `pip install langchain` to use this module.")

from pydantic import BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION

logger = logging.getLogger(__name__)


class GantryCallbackHandler(BaseCallbackHandler):
    _inputs: Dict

    def __init__(
        self,
        logger: EvalLogger,
        query_name: str = "query",
        chat_history_name: str = "chat_history",
    ) -> None:
        super().__init__()

        self.reset()

        self._logger = logger
        self._query_name = query_name
        self._chat_history_name = chat_history_name

        atexit.register(self.close)

        self._usage = collections.Counter(
            [
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
            ]
        )

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        logger.debug("on_chain_start: %s; %s", serialized, inputs)

        # a chain contains many sub-chains and will call on_chain_start many
        # times during a chain invocation
        if self._inputs is None:
            if isinstance(inputs, str):
                inputs = {"query": inputs}
            self._inputs = inputs
            self._metadata["serialized_langchain"] = serialized

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain ends running."""
        logger.debug("on_chain_end: %s", outputs)

        # if we're not in a subchain, log the record
        if not parent_run_id:
            try:
                # langchain type annotation lies
                self._outputs = outputs.dict()  # type: ignore
            except Exception:
                if isinstance(outputs, str):
                    outputs = {"content": outputs}
                self._outputs = outputs

            self.end()

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug("on_chat_model_start: %s; %s", serialized, messages)

        self._curr_messages = messages

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        logger.debug("on_llm_start: %s; %s", serialized, prompts)

        self._curr_prompts = prompts

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        logger.debug("on_llm_end: %s", response)

        i = 0
        for generations in response.generations:
            for generation in generations:
                self._steps.append(
                    {
                        "type": "llm",
                        # "prompt": self._curr_prompts[i],
                        # TODO: not super sure if one on_chat_model_start maps to
                        # one on_llm_end
                        "messages": self._curr_messages[i],
                        "response": generation.text,
                    }
                )
                i += 1

        self._usage.update(response.llm_output.get("token_usage", {}))  # type: ignore

    def on_text(self, text: str, **kwargs: Any) -> Any:
        logger.debug("on_text: %s", text)

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        logger.debug("on_tool_start: %s; %s", serialized, input_str)

        self._curr_input = input_str

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        self._steps.append(
            {
                "type": "tool",
                "args": [self._curr_input],
                "output": output,
            }
        )

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        logger.debug("on_agent_action: %s", action)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        logger.debug("on_agent_finish: %s", finish)

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug("on_retriever_start: %s; %s", serialized, query)
        self._curr_query = query

    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug("on_retriever_end: %s", documents)
        self._steps.append(
            {
                "type": "retrieval",
                "query": self._curr_query,
                "documents": [self._format_document(d) for d in documents],
            }
        )

    def _format_document(self, doc: Document):
        return {"content": doc.page_content}

    def get_steps(self):
        return self._steps

    def get_usage(self):
        return self._usage

    def get_inputs(self):
        inputs = self._inputs.copy()
        inputs["query"] = self._inputs.pop(self._query_name, "")
        inputs["chat_history"] = self._inputs.pop(self._chat_history_name, [])

        return inputs

    def get_record(self):
        return _json_encode(
            {
                "inputs": self._inputs,
                "outputs": self._outputs,
                "steps": self._steps,
                "metadata": self._metadata,
            }
        )

    def reset(self):
        self._curr_prompts = []
        self._curr_messages = []
        self._curr_query = None
        self._curr_input = None
        self._inputs = None
        self._outputs = None
        self._steps = []
        self._metadata = {}

    def end(self):
        self._logger.write_record(Record(**self.get_record()))

        self.reset()

    def close(self):
        self._logger.close()


def _json_encode(obj):
    if isinstance(obj, Serializable):
        return obj.dict()
    if isinstance(obj, BaseModel):
        if PYDANTIC_VERSION.startswith("2."):
            obj_dict = obj.model_dump()
        else:
            obj_dict = obj.dict()
        if "__root__" in obj_dict:
            obj_dict = obj_dict["__root__"]
        return _json_encode(obj_dict)
    if dataclasses.is_dataclass(obj):
        obj_dict = dataclasses.asdict(obj)
        return _json_encode(obj_dict)
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, dict):
        encoded_dict = {}
        for key, value in obj.items():
            encoded_key = _json_encode(key)
            encoded_value = _json_encode(value)
            encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, tuple)):
        encoded_list = []
        for item in obj:
            encoded_list.append(_json_encode(item))
        return encoded_list

    return obj
