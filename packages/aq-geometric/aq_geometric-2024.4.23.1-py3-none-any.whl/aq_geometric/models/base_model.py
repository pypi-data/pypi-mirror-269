import os
from datetime import datetime
from typing import Tuple, Dict, Union, List

import torch
import numpy as np
import pandas as pd
from torch_geometric.data import Data
from aq_utilities.data import hourly_predictions_to_postgres


class BaseModel(torch.nn.Module):
    r"""Base class for all models."""
    def __init__(self, name: str = "BaseModel",
                 guid: str = "00000000-0000-0000-0000-000000000000",
                 stations: Union[List, None] = None,
                 features: List[str] = [],
                 targets: List[str] = [],
                 num_samples_in_node_feature: int = -1,
                 num_samples_in_node_target: int = -1,
                 is_iterative: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.guid = guid
        self.stations = stations
        self.features = features
        self.targets = targets
        self.num_samples_in_node_feature = num_samples_in_node_feature
        self.num_samples_in_node_target = num_samples_in_node_target
        self.num_features_in_node_feature: int = len(self.features),
        self.num_features_in_node_target: int = len(self.targets),
        self.is_iterative = is_iterative,
        self.kwargs = kwargs

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

    def __repr__(self):
        """Use the torch default representation, add new attrs."""
        representation = super().__repr__()
        
        # add new lines with the name, guid, and stations
        representation += f"\nName: {self.name}"
        representation += f"\nGUID: {self.guid}"
        representation += f"\nStations: {self.stations}"
        representation += f"\nFeatures: {self.features}"
        representation += f"\nTargets: {self.targets}"
        representation += f"\nIs iterative: {self.is_iterative}"
        representation += f"\nNum samples in node feature: {self.num_samples_in_node_feature}"
        representation += f"\nNum samples in node target: {self.num_samples_in_node_target}"
        representation += f"\nNum features in node feature: {self.num_features_in_node_feature}"
        representation += f"\nNum features in node target: {self.num_features_in_node_target}"

        return representation

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
        raise NotImplementedError

    def forecasts_df_to_db(
        self,
        engine: str,
        graph: "Data",
        target_dfs: Dict[str, pd.DataFrame],
        run_id: Union[str, None] = None,
        chunksize: int = 1000,
        continue_on_error: bool = False,
        verbose: bool = False,
    ) -> int:
        """
        Write the forecasts to the database
        """
        # generate a random run id if none is provided
        if run_id is None:
            import uuid
            run_id = str(uuid.uuid4())

        # obtain model attributes
        model_id = self.guid
        model_name = self.name

        for target, forecast_df in target_dfs.items():
            if verbose:
                print(f"[{datetime.now()}] writing forecast for {target} to database")
            # read from the graph used to generate forecasts
            assert len(graph.h3_index) == len(graph.aqsid)
            df = pd.DataFrame(np.stack((graph.h3_index.T, graph.aqsid.T), axis=1), columns=["h3_index", "aqsid"])

            # obtain the timestamps
            timestamps = forecast_df.columns.to_list()
            data = forecast_df.values
            max_timestamp_in_samples = graph.feature_end_time
            predicted_at_timestamp = pd.Timestamp.now()

            # prepare the data
            for i, timestamp in enumerate(timestamps):
                df["value"] = data[:, i]
                df["timestamp"] = timestamp
                df["predicted_at_timestamp"] = predicted_at_timestamp
                df["max_timestamp_in_samples"] = max_timestamp_in_samples
                df["model_id"] = model_id
                df["model_name"] = model_name
                df["run_id"] = run_id
                df["measurement"] = target

                # write the predictions to postgres
                err = hourly_predictions_to_postgres(
                    predictions=df,
                    engine=engine,
                    chunksize=chunksize,
                )
                if err == 1:
                    print(f"failed to write predictions to postgres: {err}")
                    if continue_on_error: continue
                    else: return 1

        return 0

    def forecasts_df_to_json(
        self,
        targets: List[str],
        target_dfs: Dict[str, pd.DataFrame],
        verbose: bool = False,
    ) -> dict:
        """Prepare the forecast in json format"""
        # generate the frontend data
        fe_data = {}
        fe_data["num_history_samples"] = self.num_samples_in_node_feature
        fe_data["num_forecast_samples"] = self.num_samples_in_node_target
        model_name = self.name
        
        # we also want to include the history and the forecasts
        fe_data[model_name] = {
            **{target_name: {} for target_name in targets},
        }
        timestamps = None
        history_and_forecasts_len = -1
        for target_name, forecast_df in target_dfs.items():
            if verbose:
                print(f"[{datetime.now()}] preparing forecast for {target_name}")
            if timestamps is None:
                timestamps = forecast_df.columns.to_list()
            for row_ in forecast_df.iterrows():
                h3_index = row_[0]
                fe_data[model_name][target_name][h3_index] = [int(v) for v in row_[1].fillna(0).tolist()]
                if history_and_forecasts_len == -1:
                    history_and_forecasts_len = len(row_[1])
                else:
                    if history_and_forecasts_len != len(row_[1]):
                        raise ValueError("forecast lengths do not match")
        
        # if we did not include history, we still want to include the timestamps'
        if history_and_forecasts_len == self.num_samples_in_node_target:
            fe_data["num_history_samples"] = 0
            if verbose:
                print(f"[{datetime.now()}] no history included in forecast")

        # we want access to the timestamps when displaying the data
        fe_data["timestamps"] = [
            str(t) for t in timestamps
        ]

        if verbose:
            print(f"[{datetime.now()}] frontend datetimes: [{fe_data['timestamps'][0]}, {fe_data['timestamps'][-1]}]")
            print(f"[{datetime.now()}] prepared forecast for frontend")

        return fe_data


    def _generate_forecasts_direct(
        self,
        graph: "Data",
        targets: List[str],
        include_history: bool = False,
        verbose: bool = False,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, np.ndarray]:
        """
        Generate direct forecasts using the model provided
        """
        raise NotImplementedError

    def _generate_forecasts_iterative(
        self,
        graph: "Data",
        targets: List[str],
        include_history: bool = False,
        verbose: bool = False,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, np.ndarray]:
        """
        Generate iterative forecasts using the model provided
        """
        raise NotImplementedError

