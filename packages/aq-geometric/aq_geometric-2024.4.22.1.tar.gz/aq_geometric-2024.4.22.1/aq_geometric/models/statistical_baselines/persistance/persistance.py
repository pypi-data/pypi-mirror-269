import os
from datetime import datetime
from typing import Dict, List, Tuple, Union, Callable

import uuid
import h3
import torch  # already required, used for serialization
import xgboost as xgb
import numpy as np
import pandas as pd
from torch_geometric.data import Data
from aq_utilities.data import hourly_predictions_to_postgres

from aq_geometric.models.base_model import BaseModel


class AqGeometricPersistanceModel(BaseModel):
    
    def __init__(
        self,
        name: str = "AqGeometricPersistanceModel",
        guid: str = str(uuid.uuid4()),
        stations: Union[List, None] = None,
        features: List[str] = ["OZONE", "PM2.5", "NO2"],
        targets: List[str] = ["OZONE", "PM2.5", "NO2"],
        num_samples_in_node_feature: int = 48,
        num_samples_in_node_target: int = 12,
        is_iterative: bool = False,
        verbose: bool = False,
    ):
        super().__init__(
            name=name,
            guid=guid,
            stations=stations,
            features=features,
            targets=targets,
            num_samples_in_node_feature=num_samples_in_node_feature,
            num_samples_in_node_target=num_samples_in_node_target,
            is_iterative=is_iterative,
        )
        self.num_features_in_node_feature = len(features)
        self.num_features_in_node_target = len(targets)
        self.verbose = verbose
        self.last_training_obs = None

    def fit(self, g: "Data"):
        # obtain the training data from `g`
        graph_data = g.x.detach().numpy()
        last_training_obs = graph_data[:, -1:, :]  # (n_h3_index, 1, n_targets)
        last_trianing_h3_index = g.h3_index

        if self.verbose:
            print(f"last_training_obs shape: {np.shape(last_training_obs)}")
        
        self.state_dict = {
            "last_training_obs": last_training_obs,
            "last_trianing_h3_index": last_trianing_h3_index,
        }

    def predict(self, g: "Data") -> Tuple[np.ndarray, np.ndarray]:
        """Use the trained boosters to predict the target values for each feature in `g`."""
        assert self.state_dict is not None, "model must be trained before predicting"
        
        valid_h3_indices = self.state_dict["last_trianing_h3_index"]
        pred_data = self.state_dict["last_training_obs"]

        h3_indices = g.h3_index
        target_timestamps = g.target_timestamps

        # repeat pred_data len(target_timesamps) times
        pred = np.repeat(pred_data, len(target_timestamps), axis=1)
        
        if self.verbose:
            print(f"[{datetime.now()}] before re-indexing to h3_index, predictions has shape {pred.shape}")
        
        # ensure we match the input h3_indecies
        preds_dfs = []
        for i in range(len(self.targets)):
            tmp = pd.DataFrame(
                pred[:,:,i], columns=target_timestamps, index=valid_h3_indices
            )
            tmp = tmp.join(pd.DataFrame(h3_indices, columns=["h3_index"]).set_index("h3_index"), how="right")
            preds_dfs.append(tmp)
        pred = np.stack([p.to_numpy() for p in preds_dfs], axis=2)
        
        if self.verbose:
            print(f"[{datetime.now()}] after re-indexing to h3_index, predictions has shape {pred.shape}")

        return h3_indices, pred

    def eval(self):
        """We match the interface of other models."""
        pass

    def cpu(self):
        """We match the interface of other models."""
        pass

    def save(self, path: str):
        """Save the model to a file."""
        assert self.state_dict is not None, "model must be trained before saving"

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
            "state_dict": self.state_dict,
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
        self.num_samples_in_node_feature = model_data["num_samples_in_node_feature"]
        self.num_samples_in_node_target = model_data["num_samples_in_node_target"]
        self.num_features_in_node_feature = len(self.features)
        self.num_features_in_node_target = len(self.targets)
        self.is_iterative = model_data.get("is_iterative", False)  # for backwards compatability
        self.load_state_dict(model_data["state_dict"])

        # set the kwargs
        for key, value in model_data.items():
            if key not in ["name", "guid", "stations", "features", "targets", "num_samples_in_node_feature", "num_samples_in_node_target", "num_features_in_node_feature", "num_features_in_node_target", "is_iterative", "state_dict"]:
                setattr(self, key, value)

    def load_state_dict(self, state_dict: Dict):
        """We match the interface of other models."""
        self.state_dict = state_dict

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
        return self._generate_forecasts_direct(
            graph=graph,
            targets=targets if targets is not None else self.targets,
            include_history=include_history,
            verbose=verbose if verbose is not None else self.verbose
        )

    def _generate_forecasts_direct(
        self,
        graph: "Data",
        targets: Union[List[str], None] = None,
        include_history: bool = False,
        verbose: Union[List[str], None] = None,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, List[np.ndarray]]:
        """
        Generate direct forecasts using the model provided
        """
        forecasts = []

        h3_indices = graph.h3_index
        feature_timestamps = graph.feature_timestamps
        target_timestamps = graph.target_timestamps

        if verbose:
            print(f"[{datetime.now()}] generating forecasts for {len(h3_indices)} h3 indices")
        
        valid_h3_indices, pred = self.predict(graph)
        
        if verbose:
            print(f"[{datetime.now()}] model generating forecasts for {len(valid_h3_indices)} valid h3 indices")

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
