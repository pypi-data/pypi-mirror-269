from torch_geometric.data import Data
from torch_geometric.transforms import BaseTransform


class DifferenceTransform(BaseTransform):

    def __init__(
        self,
        num_samples_in_node_target: int,
        node_missing_value: float,
    ):
        self.num_samples_in_node_target = num_samples_in_node_target
        self.node_missing_value = node_missing_value

    def forward(
        self,
        graph: "Data",
    ) -> "Data":
        new_y = graph.y.clone()
        new_y[:, 0, :] -= graph.x[:, -1, :]
        for i in range(1, self.num_samples_in_node_target):
            new_y[:, i, :] = graph.y[:, i, :] - graph.y[:, i-1, :]
        graph.y = new_y

        return graph

    def __call__(
        self,
        graph: "Data",
    ) -> "Data":
        return self.forward(graph)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(num_samples_in_node_target={self.num_samples_in_node_target})'
