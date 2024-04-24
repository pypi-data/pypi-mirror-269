# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing_extensions import override

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.dag.text_embedding_node import TextEmbeddingNode
from superlinked.framework.common.data_types import Vector
from superlinked.framework.common.interface.has_length import HasLength
from superlinked.framework.common.parser.parsed_schema import ParsedSchema
from superlinked.framework.online.dag.default_online_node import DefaultOnlineNode
from superlinked.framework.online.dag.evaluation_result import (
    EvaluationResult,
    SingleEvaluationResult,
)
from superlinked.framework.online.dag.online_node import OnlineNode
from superlinked.framework.online.store_manager.evaluation_result_store_manager import (
    EvaluationResultStoreManager,
)


class OnlineTextEmbeddingNode(DefaultOnlineNode[TextEmbeddingNode, Vector], HasLength):
    def __init__(
        self,
        node: TextEmbeddingNode,
        parents: list[OnlineNode],
        evaluation_result_store_manager: EvaluationResultStoreManager,
    ) -> None:
        super().__init__(node, parents, evaluation_result_store_manager)

    @property
    def length(self) -> int:
        return self.node.length

    @override
    def evaluate_self(
        self,
        parsed_schemas: list[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector]]:
        if self._is_query_without_similar_clause(parsed_schemas, context):
            vector = Vector([0] * self.node.length)
            return [
                EvaluationResult(self._get_single_evaluation_result(vector))
                for _ in parsed_schemas
            ]
        return super().evaluate_self(parsed_schemas, context)

    @override
    def _evaluate_singles(
        self,
        parent_results: dict[OnlineNode, list[SingleEvaluationResult]],
        context: ExecutionContext,
    ) -> list[Vector] | None:
        if len(parent_results.items()) != 1:
            return None
        input_ = list(parent_results.values())[0]
        values = [result.value for result in input_]
        return self.__embed_texts(values)

    def __embed_texts(self, texts: list[str]) -> list[Vector]:
        return self.node.embedding.embed_multiple(texts)
