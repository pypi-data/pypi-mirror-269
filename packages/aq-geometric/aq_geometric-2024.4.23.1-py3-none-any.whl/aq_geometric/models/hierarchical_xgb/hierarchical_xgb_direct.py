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

from aq_geometric.models.hierarchical_xgb.base_hierarchical_xgb import BaseAqGeometricXGBModel


class AqGeometricXGBModel(BaseAqGeometricXGBModel):
    """
    Train and run inference using data reformed to long format (each row is a single observation for a single station)
    * forecast iteratively for a given station
    * train using X as the values from connected h3 indices
    * inference by forecasting the root node value and then going down from there
    * for each row (h3 index) we take as input the values from the prior timestamp of all connected rows from the graph (same edge index data as the AqHeirEdgeConvModel)
    * we also take as input the forecast values of each row (h3 index) connected to the node but at a coarser resolution
    * these shapes should be the same throughout time as we can handle missing values in the input
    * if the target is missing we can just skip the row!
    Args:
        name (str): the name of the model
        guid (str): the guid of the model
        stations (Union[List, None]): the stations
        features (List[str]): the features
        targets (List[str]): the targets
        num_samples_in_node_feature (int): the number of samples in the node feature
        num_samples_in_node_target (int): the number of samples in the node target
        sample_graph (Data): the sample graph
        finest_resolution (int): the finest resolution
        coarsest_resolution (int): the coarsest resolution
        xgb_kwargs (Dict): the XGBoost kwargs
        verbose (bool): whether to print out information about the model
    """
    def __init__(
        self,
        name: str = "AqGeometricXGBModel",
        guid: str = str(uuid.uuid4()),
        stations: Union[List, None] = None,
        features: List[str] = ["OZONE", "PM2.5", "NO2"],
        targets: List[str] = ["OZONE", "PM2.5", "NO2"],
        num_samples_in_node_feature: int = 48,
        num_samples_in_node_target: int = 12,
        is_iterative: bool = False,
        include_masks_in_features: bool = False,
        include_masks_in_targets: bool = False,
        sample_graph: "Data" = None,
        node_id_to_h3_index_map: Union[dict, None] = None,
        h3_index_to_node_id_map: Union[dict, None]= None,
        finest_resolution: int = 6,
        coarsest_resolution: int = -1,
        reshape_order: str = "F",
        xgb_max_depth: int = 5,
        xgb_n_estimators: int = 256,
        xbg_tree_method: str = "hist",
        xgb_early_stopping_rounds: int = 10,
        xgb_num_boost_round: int = 100,
        xgb_learning_rate: float = 0.08,
        xgb_objective: Union[str, Callable] = "reg:squarederror",
        xgb_model_filename: str = "xgb_model.ubj",  # the filename to save the model
        xgb_kwargs: Dict = {},  # additional kwargs for the XGBoost model
        xgb_strategy: str = "multi_output_tree",  # use multi-output model
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
            include_masks_in_features=include_masks_in_features,
            include_masks_in_targets=include_masks_in_targets,
            sample_graph=sample_graph,
            node_id_to_h3_index_map=node_id_to_h3_index_map,
            h3_index_to_node_id_map=h3_index_to_node_id_map,
            finest_resolution=finest_resolution,
            coarsest_resolution=coarsest_resolution,
            reshape_order=reshape_order,
            xgb_max_depth=xgb_max_depth,
            xgb_n_estimators=xgb_n_estimators,
            xbg_tree_method=xbg_tree_method,
            xgb_early_stopping_rounds=xgb_early_stopping_rounds,
            xgb_num_boost_round=xgb_num_boost_round,
            xgb_learning_rate=xgb_learning_rate,
            xgb_objective=xgb_objective,
            xgb_model_filename=xgb_model_filename,
            xgb_kwargs=xgb_kwargs,
            xgb_strategy=xgb_strategy,
            verbose=verbose,
        )

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
        
        self.node_id_to_h3_index_map = {i: v for i, v in enumerate(graph.h3_index)}  # map node id to h3 index
        self.h3_index_to_node_id_map = {v: i for i, v in enumerate(graph.h3_index)}  # map h3 index to node id
        valid_h3_indices, pred = self.predict(graph)
        
        if verbose:
            print(f"[{datetime.now()}] model generating forecasts for {len(valid_h3_indices)} valid h3 indices")

        if verbose:
            print(f"[{datetime.now()}] before re-indexing to h3_index,  predictions has shape {pred.shape}")

        # ensure we match the input h3_indecies
        preds_dfs = []
        for i, target in enumerate(targets):
            tmp = pd.DataFrame(
                pred[:,:,i], columns=target_timestamps, index=valid_h3_indices
            )
            tmp = tmp.join(pd.DataFrame(h3_indices, columns=["h3_index"]).set_index("h3_index"), how="right")
            preds_dfs.append(tmp)
        pred = np.stack([p.to_numpy() for p in preds_dfs], axis=2)
        
        if verbose:
            print(f"[{datetime.now()}] after re-indexing to h3_index, predictions has shape {pred.shape}")
        
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
