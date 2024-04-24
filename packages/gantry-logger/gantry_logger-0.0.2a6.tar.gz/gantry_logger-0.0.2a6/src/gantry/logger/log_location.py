import os
import json
import logging
from abc import ABC, abstractmethod
from queue import Queue
from typing import Dict, List, Optional

import requests
from gantry.logger.consumer import BatchConsumer
from gantry.logger.eval_reports import EvaluationReport
from gantry.logger.utils import _init_gantry
from gantry.models.components.createragevaluationrequest import (
    CreateRAGEvaluationRequest,
)
from gantry.models.components.logragrecordrequest import LogRagRecordRequest

logger = logging.getLogger(__name__)


class EvalReportAlreadyCreated(Exception):
    pass


class OutputLog(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def open(self):
        """Start the output."""
        ...

    @abstractmethod
    def write(self, data: Dict):
        """Write a line of data to the output."""
        ...

    @abstractmethod
    def close(self):
        """Close the output."""
        ...


class FileLog(OutputLog):
    def __init__(self, filename: str, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self._f = None

    def open(self):
        """Open the file for appending"""
        self._f = open(self.filename, "a")

    def write(self, data):
        self._f.write(json.dumps(data))
        self._f.write("\n")

    def close(self):
        """Close the file"""
        self._f.close()


class EvalReportLog(OutputLog):
    def __init__(self, name: str, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._records: List[Dict] = []
        self._name = name
        self._sdk = _init_gantry(api_key)
        self._eval_id = None
        self._report_created = False

    def open(self):
        pass

    def write(self, data):
        """Add the record to the list of records to be uploaded."""
        self._records.append(data)

    def close(self):
        """Create the evaluation run and upload the records."""
        if not self._records:
            return

        pre_upload = self._sdk.evaluations.create_evaluation_run_pre_upload()
        pending_id = pre_upload.evaluation_run_pre_upload_response.data.id
        presigned_url = pre_upload.evaluation_run_pre_upload_response.data.presigned_url

        requests.put(
            presigned_url,
            data="\n".join(json.dumps(record) for record in self._records),
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )

        eval_run = self._sdk.evaluations.create_rag_evaluation_run(
            CreateRAGEvaluationRequest(
                concepts_mapping={"query": "query", "chat_history": "chat_history"},
                name=self._name,
                pending_dataset_id=pending_id,
            )
        )

        self._eval_id = eval_run.evaluation_run_response.data.id
        self._records = []
        return self._eval_id

    def create_evaluation_report(self):
        """Create the evaluation report."""
        if self._report_created:
            raise EvalReportAlreadyCreated(
                "An evaluation report has already been created. "
                "Please create a new EvalReportLogger to create a new report."
            )

        eval_report_id = self.close()
        self._report_created = True
        server_url, _ = self._sdk.sdk_configuration.get_server_details()
        print(
            "Evaluation report created! View it at "
            f"{server_url}/evaluations/{eval_report_id}"
        )
        return EvaluationReport(
            eval_report_id, api_key=self._sdk.sdk_configuration.security.api_key_auth
        )


class StreamLog(OutputLog):
    def __init__(
        self,
        source_name: str,
        api_key: Optional[str] = None,
        send_in_background: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._source_name = source_name
        self._sdk = _init_gantry(api_key)

        self.num_consumer_threads: int = 1
        if send_in_background:
            # We may need to override send_in_background=True if running in lambda.
            # Set sync behavior in case app is running in a lambda (scenario in which
            # we can't start a thread).
            # https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html
            send_in_background = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is None
        self.send_in_background = send_in_background
        self.queue: Queue = Queue()
        self.consumers = []

        if self.send_in_background:
            for _ in range(self.num_consumer_threads):
                consumer = BatchConsumer(self.queue, self.consumer_func)
                self.consumers.append(consumer)
                consumer.start()

    def consumer_func(self, batch):
        # Catch all errors and do not raise in order
        # for thread consumer to continue running.
        try:
            self._sdk.logs.log_rag_records(
                LogRagRecordRequest(records=batch, source_name=self._source_name)
            )
        except Exception as e:
            logger.error("Internal error sending batches: %s", e)

    def open(self):
        pass

    def write(self, data):
        """Push the record to the logs api."""
        if self.send_in_background:
            self.queue.put(data)
        else:
            self._sdk.logs.log_rag_records(
                LogRagRecordRequest(records=[data], source_name=self._source_name)
            )

    def close(self):
        for consumer in self.consumers:
            consumer.pause()
            try:
                consumer.join()
            except RuntimeError:
                # consumer thread has not started
                pass
