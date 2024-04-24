from typing import Optional

from gantry.logger.utils import _init_gantry
from gantry.models.operations.get_rag_evaluation_results import (
    GetRagEvaluationResultsRequest,
)


class EvaluationReport:
    def __init__(self, evaluation_id: str, api_key: Optional[str] = None) -> None:
        self._sdk = _init_gantry(api_key)
        self._eval_id = evaluation_id

    def get_results(self):
        return self._sdk.evaluations.get_rag_evaluation_results(
            GetRagEvaluationResultsRequest(
                evaluation_run_id=self._eval_id, start=0, limit=10_000
            )
        ).get_rag_evaluation_results_response_response.data
