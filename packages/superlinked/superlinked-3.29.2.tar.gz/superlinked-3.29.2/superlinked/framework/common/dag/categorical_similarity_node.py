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

from superlinked.framework.common.dag.node import Node
from superlinked.framework.common.data_types import Vector
from superlinked.framework.common.embedding.categorical_similarity_embedding import (
    CategoricalSimilarityEmbedding,
)
from superlinked.framework.common.interface.has_length import HasLength
from superlinked.framework.common.space.normalization import Normalization


class CategoricalSimilarityNode(Node[Vector], HasLength):
    def __init__(
        self,
        parent: Node[str],
        categories: list[str],
        negative_filter: float,
        uncategorised_as_category: bool,
        normalization: Normalization,
    ) -> None:
        super().__init__([parent])
        self.embedding = CategoricalSimilarityEmbedding(
            categories=categories,
            negative_filter=negative_filter,
            uncategorised_as_category=uncategorised_as_category,
            normalization=normalization,
        )

    @property
    def length(self) -> int:
        return self.embedding.length
