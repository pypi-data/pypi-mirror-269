import os
from datetime import datetime
from typing import Dict, List, Tuple, Union

import uuid
import torch
import numpy as np
import pandas as pd
import torch.nn.functional as F
import torch.nn as nn
from torch_geometric.data import Data
from torch.nn import Sequential as  ReLU
from torch_geometric.nn import GCNConv

from aq_geometric.models.base_model import BaseModel


def masked_layer_norm(x, mask, normalized_shape=(0, 1)):
    # Assumes mask is a boolean tensor where True = missing
    x = x.masked_fill(~mask, 0.)  # Set missing to zero 

    mean = x.sum(dim=normalized_shape, keepdim=True) / mask.sum(dim=normalized_shape, keepdim=True)  
    variance = ((x - mean) ** 2).sum(dim=normalized_shape, keepdim=True) / mask.sum(dim=normalized_shape, keepdim=True)
    normalized = (x - mean) * torch.rsqrt(variance + 1e-10) 

    return normalized

class MPNNLayer(nn.Module):
    def __init__(self, embedding_dim):
        super().__init__()

        self.message_passing = GCNConv(
            in_channels=embedding_dim,
            out_channels=embedding_dim,
            aggr="add", flow="source_to_target"
        )
        self.relu = ReLU()
        self.linear = nn.Linear(embedding_dim, embedding_dim, bias=False)

    def forward(self, x, edge_index):
        x = self.linear(x)
        x = self.message_passing(x, edge_index)
        x = self.relu(x)

        return x

class AqGeometricEncoder(nn.Module):

    def __init__(self, num_samples_per_feature, input_feature_dim, embedding_dim, num_heads):
        super().__init__()

        self.num_samples_per_feature = num_samples_per_feature
        self.input_feature_dim = input_feature_dim

        self.embedding_layer = nn.Linear(num_samples_per_feature * input_feature_dim, embedding_dim)
        self.attention = nn.MultiheadAttention(embedding_dim, num_heads)
        self.linear = nn.Linear(embedding_dim * num_samples_per_feature, embedding_dim, bias=False)

    def forward(self, x, x_mask):
        x = masked_layer_norm(x, x_mask)  # Apply normalization first
        x = self.embedding_layer(x.view(-1, self.num_samples_per_feature * self.input_feature_dim))  # Embed the input
        x, attention_weights = self.attention(x, x, x)
        return x, attention_weights

class AqGeometricProcessor(nn.Module):
    def __init__(self, embedding_dim, num_message_passing_steps):
        super().__init__()

        self.mpnn_layers = nn.ModuleList()
        for _ in range(num_message_passing_steps):
            self.mpnn_layers.append(MPNNLayer(embedding_dim))

    def forward(self, x, edge_index):
        for layer in self.mpnn_layers:
            x = layer(x, edge_index)
        return x

class AqGeometricDecoder(nn.Module):

    def __init__(self, embedding_dim, num_samples_per_target, output_feature_dim, output_shape):
        super().__init__()

        self.embedding_layer = nn.Linear(embedding_dim, num_samples_per_target * output_feature_dim)
        self.output_shape = output_shape

    def forward(self, x):
        x = self.embedding_layer(x) 
        x = x.reshape(x.shape[0], *self.output_shape)
        return x

class AqGeometricMessagePassingModel(BaseModel):
    
    def __init__(
        self,
        name: str = "AqGeometricMessagePassingModel",
        guid: str = str(uuid.uuid4()),
        stations: Union[List, None] = None,
        features: List[str] = ["OZONE", "PM2.5", "NO2"],
        targets: List[str] = ["OZONE", "PM2.5", "NO2"],
        num_samples_in_node_feature: int = 48,
        num_samples_in_node_target: int = 12,
        is_iterative: bool = True,
        finest_resolution: int = 7,
        coarsest_resolution: int = -1,
        num_h3_index: int = 100,
        num_message_passing_steps: int = 4,
        embedding_dim: int = 64,
        num_heads: int = 4,

        verbose: bool = False,
    ):
        super().__init__(name=name, guid=guid, stations=stations, features=features, targets=targets, num_samples_in_node_feature=num_samples_in_node_feature, num_samples_in_node_target=num_samples_in_node_target)
        self.is_iterative = is_iterative
        self.num_features_in_node_feature = len(features)
        self.num_features_in_node_target = len(targets)
        self.finest_resolution = finest_resolution
        self.coarsest_resolution = coarsest_resolution
        self.num_h3_index = num_h3_index
        self.num_message_passing_steps = num_message_passing_steps
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.verbose = verbose
       
        self.encoder = AqGeometricEncoder(self.num_samples_in_node_feature, self.num_features_in_node_feature, embedding_dim, num_heads)
        self.processor = AqGeometricProcessor(embedding_dim, num_message_passing_steps)
        self.decoder = AqGeometricDecoder(embedding_dim, 1, self.num_features_in_node_target, (1, self.num_features_in_node_target))

    def forward(self, x, edge_index, x_mask):
        x, _ = self.encoder(x, x_mask)
        x = self.processor(x, edge_index)
        x = self.decoder(x)

        return x

    def save(self, path: str):
        """Save the model to a file."""
        # ensure the model is on the CPU
        self.cpu()

        # ensure the path exists
        # check if the path has a directory
        if os.path.dirname(path):
            # create the directory if it does not exist
            os.makedirs(os.path.dirname(path), exist_ok=True)

        # gather the model data
        model_data = {
            "name": self.name,
            "guid": self.guid,
            "stations": self.stations,
            "features": self.features,
            "targets": self.targets,
            "num_samples_in_node_feature": self.num_samples_in_node_feature,
            "num_samples_in_node_target": self.num_samples_in_node_target,
            "is_iterative": self.is_iterative,
            "finest_resolution": self.finest_resolution,
            "coarsest_resolution": self.coarsest_resolution,
            "num_h3_index": self.num_h3_index,
            "num_message_passing_steps": self.num_message_passing_steps,
            "embedding_dim": self.embedding_dim,
            "num_heads": self.num_heads,
            "state_dict": self.state_dict(),
            **self.kwargs
        }
        # save the model data
        torch.save(model_data, path)

    def load(self, path: str):
        """Load the model from a file."""
        # load the model data
        model_data = torch.load(path)

        # set the model data
        self.name = model_data["name"]
        self.guid = model_data["guid"]
        self.stations = model_data["stations"]
        self.features = model_data["features"]
        self.targets = model_data["targets"]
        self.num_samples_in_node_feature = model_data[
            "num_samples_in_node_feature"]
        self.num_samples_in_node_target = model_data[
            "num_samples_in_node_target"]
        self.is_iterative = model_data["is_iterative"]
        self.finest_resolution = model_data.get("finest_resolution")
        self.coarsest_resolution = model_data.get("coarsest_resolution")
        self.num_h3_index = model_data.get("num_h3_index")
        self.num_message_passing_steps = model_data.get("num_message_passing_steps")
        self.embedding_dim = model_data.get("embedding_dim")
        self.num_heads = model_data.get("num_heads")

        self.load_state_dict(model_data["state_dict"])

        # set the kwargs
        for key, value in model_data.items():
            if key not in ["name", "guid", "stations", "features", "targets", "num_samples_in_node_feature", "num_samples_in_node_target", "is_iterative", "num_features_in_node_feature", "num_features_in_node_target", "state_dict"]:
                setattr(self, key, value)

    def __repr__(self):
        """Use the torch default representation, add new attrs."""
        representation = super().__repr__()
        # add new lines with the name, guid, and stations
        representation += f"\nNumber of h3 indices: {self.num_h3_index}"
        representation += f"\nFinest h3 resolution: {self.finest_resolution}"
        representation += f"\Coarsest h3 resolution: {self.coarsest_resolution}"
        representation += f"\nNumber of message passing steps: {self.num_message_passing_steps}"
        representation += f"\nEmbedding dimension: {self.embedding_dim}"
        representation += f"\nNumber of heads: {self.num_heads}"

        return representation

    def _generate_forecasts_direct(
        self,
        graph: "Data",
        targets: List[str],
        include_history: bool = False,
        verbose: bool = False,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, np.ndarray]:
        """
        Generate forecasts using the model provided
        """
        forecasts = []

        inputs = graph.x
        input_edge_index = graph.edge_index
        input_x_mask = graph.x_mask
        h3_indices = graph.h3_index
        aqsids = graph.aqsid
        timestamps = graph.timestamps
        feature_timestamps = graph.feature_timestamps
        target_timestamps = graph.target_timestamps

        with torch.no_grad():
            if verbose:
                print(f"[{datetime.now()}] generating forecasts for {len(h3_indices)} h3 indices")
            pred = self(inputs, input_edge_index, input_x_mask)
            # reshape the prediction to the shape of the target
            pred = pred.numpy().reshape(graph.y_mask.shape)
        
        # prepare the forecasts, including the history
        target_dfs = {}
        history = graph.x.detach().numpy()
        testmask = graph.x_mask[:, 0, :].detach().numpy()
        forecasts = (testmask.reshape(-1, 1, len(targets)) * pred)

        for i, target in enumerate(targets):
            if verbose:
                print(f"[{datetime.now()}] preparing forecast for {target}")
            history_df = pd.DataFrame(
                history[:,:,i], columns=feature_timestamps, index=h3_indices
            ) if include_history else pd.DataFrame()
            if verbose:
                print(f"[{datetime.now()}] history df shape for {target}: {history_df.shape}")
            forecast_df = pd.DataFrame(
                forecasts[:,:,i], columns=target_timestamps, index=h3_indices
            )
            if verbose:
                print(f"[{datetime.now()}] forecast df shape for {target}: {forecast_df.shape}")
            df = pd.concat([history_df, forecast_df], axis=1)
            target_dfs[target] = df
            if verbose:
                print(f"[{datetime.now()}] added DataFrame {df.shape}")

        return target_dfs, forecasts, pred

    def generate_forecasts(
        self,
        graph: "Data",
        targets: Union[List[str], None] = None,
        include_history: bool = False,
        verbose: Union[List[str], None] = None,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, List[np.ndarray]]:
        """
        Generate forecasts using the model provided
        """
        return self._generate_forecasts_iterative(
            graph=graph,
            targets=targets if targets is not None else self.targets,
            include_history=include_history,
            verbose=verbose if verbose is not None else self.verbose
        )

    def _generate_forecasts_iterative(
        self,
        graph: "Data",
        targets: Union[List[str], None] = None,
        include_history: bool = False,
        verbose: Union[List[str], None] = None,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, List[np.ndarray]]:
        """
        Generate itertive forecasts using the model provided
        """
        forecasts = []

        inputs = graph.x
        input_edge_index = graph.edge_index
        input_x_mask = graph.x_mask
        h3_indices = graph.h3_index
        aqsids = graph.aqsid
        timestamps = graph.timestamps
        feature_timestamps = graph.feature_timestamps
        target_timestamp = graph.target_timestamps
        freq = graph.freq

        preds = []
        with torch.no_grad():
            for i in range(self.num_samples_in_node_target):
                if verbose:
                    print(f"[{datetime.now()}] generating forecasts for {len(h3_indices)} h3 indices")
                pred = self(inputs, input_edge_index, input_x_mask)
                if verbose:
                    print(f"[{datetime.now()}] generated new iterative pred shape: {pred.shape}")
                preds.append(pred)
                # update the inputs and input_x_mask
                inputs = torch.cat([inputs[:, 1:, :], pred], dim=1)
                if verbose:
                    print(f"[{datetime.now()}] next input shape: {inputs.shape}")
                input_x_mask = torch.cat([input_x_mask[:, 1:, :], input_x_mask[:, -1:, :]], dim=1)
                if verbose:
                    print(f"[{datetime.now()}] next input_x_mask shape: {input_x_mask.shape}")
        # each prediction in preds is (n_h3_index, 1, n_targets)
        # we want to stack them to get (n_h3_index, n_timestamps, n_targets)
        pred = np.stack(preds, axis=1).reshape(-1, self.num_samples_in_node_target, len(targets))
        if verbose:
            print(f"[{datetime.now()}] pred shape: {pred.shape}")

        # prepare the forecasts, including the history
        target_dfs = {}
        history = graph.x.detach().numpy()
        testmask = graph.x_mask[:, 0, :].detach().numpy()
        forecasts = (testmask.reshape(-1, 1, len(targets)) * pred)
        target_timestamps = pd.date_range(start=target_timestamp[0], periods=self.num_samples_in_node_target, freq=freq)

        if verbose:
            print(f"[{datetime.now()}] after applying mask, forecast shape: {forecasts.shape}")

        for i, target in enumerate(targets):
            if verbose:
                print(f"[{datetime.now()}] preparing forecast for {target}")
            history_df = pd.DataFrame(
                history[:,:,i], columns=feature_timestamps, index=h3_indices
            ) if include_history else pd.DataFrame()
            if verbose:
                print(f"[{datetime.now()}] history df shape for {target}: {history_df.shape}")
            forecast_df = pd.DataFrame(
                forecasts[:,:,i], columns=target_timestamps, index=h3_indices
            )
            if verbose:
                print(f"[{datetime.now()}] forecast df shape for {target}: {forecast_df.shape}")
            df = pd.concat([history_df, forecast_df], axis=1)
            target_dfs[target] = df
            if verbose:
                print(f"[{datetime.now()}] added DataFrame {df.shape}")

        return target_dfs, forecasts, pred
