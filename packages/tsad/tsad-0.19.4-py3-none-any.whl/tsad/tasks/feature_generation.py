from ..base.task import Task, TaskResult

import re
import pandas as pd
from tsflex.features import FeatureCollection, MultipleFeatureDescriptors
from tsflex.features.utils import make_robust
from tsflex.features.integrations import tsfresh_settings_wrapper
from IPython.display import display
from typing import List, Dict
from tsfresh.feature_extraction import EfficientFCParameters


class FeatureGenerationResult(TaskResult):
    """
    Stores the result of feature generation.

    Attributes:
        selected_features (list[str]): List of selected features.
        generated_features (list[str]): List of generated features.
        feature_collection (FeatureCollection): Collection of feature descriptors.
    """
    def __init__(self):
        self.selected_features = None
        self.generated_features = None
        self.feature_collection = None
        self.raw_columns = None
        self.renamed_columns = {}
        self.inversed_renamed_columns = {}

    def show(self) -> None:
        """
        Display or process the generated features as needed.

        This method displays the total number of generated features.
        """
        display(f"Total generated features: {len(self.generated_features)}")


class FeatureGenerationTask(Task):
    """
    A task for generating features from a DataFrame based on a configuration.

    Attributes:
        config (List[Dict] | None): Configuration for feature generation (optional).
        features (List[str] | None): List of features to consider (optional).
    """

    def __init__(self, config: List[Dict] | None = None, features: List[str] | None = None):
        
        self.features = features
        self.config = config
        super().__init__()

    def validate_input(self):
        """
        Validate the input parameters, raising exceptions for invalid inputs.
        """
        if self.features is not None and not isinstance(self.features, list):
            raise ValueError("The 'features' parameter must be a list.")
        if self.config is not None and not isinstance(self.config, list):
            raise ValueError("The 'config' parameter must be a list of dictionaries.")


    def fit_predict(self, df: pd.DataFrame) -> tuple[pd.DataFrame, FeatureGenerationResult]:
        """
        Fit the feature generation task to the input data.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            tuple[pd.DataFrame, FeatureGenerationResult]: A tuple containing the DataFrame with
            generated features and the FeatureGenerationResult.
        """
        # Check if the DataFrame has a DatetimeIndex with a specified frequency
        self.validate_input()

        # Prepare the feature collection based on the provided config or default config
        if self.config is not None:
            feature_collection = self._prepare_feature_collection(self.config, df)
        else:
            feature_collection = self._prepare_feature_collection(self.get_default_config(df))

        # Calculate features and drop columns with all NaN values
        df_prep = feature_collection.calculate(df, return_df=True, show_progress=False)
        df_prep = df_prep.dropna(axis=1, how='all')

        # Rename columns to remove special characters
        renamed_columns = {col:re.sub("[{']|[}']|[:]", '', col) for col in df_prep.columns}
        inverse_renamed_columns_to_fc = {v:k for k,v in renamed_columns.items()}
        
        df_prep = df_prep.rename(columns=renamed_columns)


        result = FeatureGenerationResult()
        result.generated_features = df_prep.columns.tolist()
        result.raw_columns = df.columns.tolist()
        result.feature_collection = feature_collection
        result.renamed_columns = renamed_columns
        result.inversed_renamed_columns = inverse_renamed_columns_to_fc

        result.selected_features = df_prep.columns

        return pd.concat([df, df_prep], axis=1), result

    def predict(self, df: pd.DataFrame, result: FeatureGenerationResult) -> tuple[pd.DataFrame, FeatureGenerationResult]:
        """
        Predict using the generated features.

        Args:
            df (pd.DataFrame): The input DataFrame.
            result (FeatureGenerationResult): The result of feature generation.

        Returns:
            tuple[pd.DataFrame, FeatureGenerationResult]: A tuple containing the DataFrame with
            generated features and the FeatureGenerationResult.
        """
        
        # Use selected or generated features for prediction
        if result.selected_features is None:
            selected_features = result.generated_features
        else:
            selected_features = result.selected_features

        # Reduce the feature collection to selected features
        fc_reduced = result.feature_collection.reduce([result.inversed_renamed_columns[col] for col in selected_features])

        # Calculate predictions using the reduced feature collection
        out_df = fc_reduced.calculate(df, return_df=True, show_progress=False)
        out_df = out_df.rename(columns=result.renamed_columns)
        return pd.concat([df, out_df[selected_features]], axis=1), None


    def get_params_from_df(self, df: pd.DataFrame):
        """
        Get window and stride parameters based on the DataFrame's frequency.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            list[str]: List of window sizes.
            list[str]: List of stride sizes.
        """
        freq_in_seq = df.index.freq.delta.seconds
        windows = [f"{freq_in_seq*4}s", f"{freq_in_seq*10}s"]
        strides = [f"{freq_in_seq}s",]
        return windows, strides
    
    def get_default_config(self, df: pd.DataFrame):
        """
        Get the default configuration for feature extraction.

        Args:
            df (pd.DataFrame): The input DataFrame.

        Returns:
            List[Dict]: List of dictionaries containing feature extraction configuration.
        """
        if self.features is None:
            series_names = df.columns
        else:
            series_names = self.features
        windows, strides = self.get_params_from_df(df)

        # List of slow feature functions to be excluded
        slow_funcs = [
            "number_cwt_peaks",
            "augmented_dickey_fuller",
            "partial_autocorrelation",
            "agg_linear_trend",
            "lempel_ziv_complexity",
            "benford_correlation",
            "ar_coefficient",
            "permutation_entropy",
            "friedrich_coefficients",
            "max_langevin_fixed_point"
        ]

        # Initialize feature extraction parameters
        funcs = EfficientFCParameters()

        # Remove slow features from the feature extraction parameters
        for func in slow_funcs:
            del funcs[func]

        config = [
            {"functions": tsfresh_settings_wrapper(funcs),
             "series_names": series_names,
             "windows": windows,
             "strides": strides,
            },
        ]
        return config
    
    def _prepare_feature_collection(self, config: List[Dict], df: pd.DataFrame | None = None):
        """
        Prepare the feature collection based on the provided configuration.

        Args:
            config (List[Dict]): Configuration for feature extraction.

        Returns:
            FeatureCollection: The prepared feature collection.
        """
        # Prepare feature descriptors based on the provided config
        feature_descriptors = []
        for item in config:
            funcs = [make_robust(f) for f in item["functions"]]
            if "strides" not in item:
                _, strides = self.get_params_from_df(df)
                item["strides"] = strides
            feature_descriptors.append(
                MultipleFeatureDescriptors(
                    functions=funcs,
                    series_names=item["series_names"],
                    windows=item["windows"],
                    strides=item["strides"],
                )
            )
        feature_collection = FeatureCollection(feature_descriptors=feature_descriptors)
        return feature_collection
