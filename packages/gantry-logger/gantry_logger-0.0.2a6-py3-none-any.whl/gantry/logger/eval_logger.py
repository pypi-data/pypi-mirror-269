import atexit
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

from gantry.logger.log_location import EvalReportLog, FileLog, OutputLog, StreamLog


@dataclass
class Record:
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    steps: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    session_id: Optional[str] = None

    def add_inputs(self, **kwargs):
        self.inputs.update(kwargs)

    def add_outputs(self, **kwargs):
        self.outputs.update(kwargs)

    def add_metadata(self, **kwargs):
        self.metadata.update(kwargs)

    def add_retrieval_step(self, query: str, documents: List[Dict]):
        self.steps.append(
            {
                "type": "retrieval",
                "query": query,
                "documents": documents,
            }
        )

    def add_function_step(self, name: str, args: Dict, output: str):
        self.steps.append(
            {
                "type": "function",
                "name": name,
                "args": args,
                "output": output,
            }
        )

    def add_llm_step(
        self,
        messages: List[Dict],
        response: str,
        params: Optional[Dict] = None,
        usage: Optional[Dict] = None,
    ):
        self.steps.append(
            {
                "type": "llm",
                "messages": list(messages),  # make a copy
                "response": response,
                "params": params,
                "usage": usage,
            }
        )

    def add_custom_step(self, data: Dict):
        self.steps.append(
            {
                "type": "custom",
                "data": data,
            }
        )


class EvalLogger:
    _record: Record

    def __init__(self, log_location: OutputLog) -> None:
        self._output = log_location
        self._output.open()

        atexit.register(self.close)

    def start_record(
        self,
        query: str,
        chat_history: Optional[List[Dict]] = None,
        session_id: Optional[str] = None,
        **kwargs,
    ):
        if not isinstance(query, str):
            raise TypeError(f"query must be a string, not {type(query)}")
        if not isinstance(chat_history, list) and chat_history is not None:
            raise TypeError(
                f"chat_history must be a list of dicts, not {type(chat_history)}"
            )

        self._record = Record()

        inputs: Dict = {"query": query}
        if chat_history:
            inputs["chat_history"] = chat_history
        inputs.update(kwargs)
        self.add_inputs(**inputs)

        if session_id:
            self._record.session_id = session_id

    def add_inputs(self, **kwargs):
        self._record.add_inputs(**kwargs)

    def add_outputs(self, **kwargs):
        self._record.add_outputs(**kwargs)

    def add_metadata(self, **kwargs):
        self._record.add_metadata(**kwargs)

    def add_retrieval_step(self, query: str, documents: List[Dict]):
        self._record.add_retrieval_step(query, documents)

    def add_function_step(self, name: str, args: Dict, output: str):
        self._record.add_function_step(name, args, output)

    def add_llm_step(
        self,
        messages: List[Dict],
        response: str,
        params: Optional[Dict] = None,
        usage: Optional[Dict] = None,
    ):
        self._record.add_llm_step(messages, response, params=params, usage=usage)

    def add_custom_step(self, data: Dict):
        self._record.add_custom_step(data)

    def end_record(self, response: str, **kwargs):
        if not isinstance(response, str):
            raise TypeError(f"response must be a string, not {type(response)}")

        self.add_outputs(response=response, **kwargs)

        self.write_record(self._record)

        self._record = None  # type: ignore

    def write_record(self, record: Record):
        self._output.write(asdict(record))

    def close(self):
        self._output.close()


class FileLogger(EvalLogger):
    _output: FileLog

    def __init__(self, path: str) -> None:
        super().__init__(FileLog(path))


class EvalReportLogger(EvalLogger):
    _output: EvalReportLog

    def __init__(self, name: str, api_key: Optional[str] = None) -> None:
        super().__init__(EvalReportLog(name=name, api_key=api_key))

    def create_evaluation_report(self):
        """Creates the evaluation report"""
        return self._output.create_evaluation_report()


class StreamLogger(EvalLogger):
    _output: StreamLog

    def __init__(
        self,
        source_name: str,
        api_key: Optional[str] = None,
        send_in_background: bool = True,
    ) -> None:
        super().__init__(
            StreamLog(
                source_name=source_name,
                api_key=api_key,
                send_in_background=send_in_background,
            )
        )
