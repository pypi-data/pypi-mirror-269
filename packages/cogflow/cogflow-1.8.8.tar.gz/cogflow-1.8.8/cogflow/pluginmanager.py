"""
Plugin Manager Module

This module provides a PluginManager class responsible for managing plugins such as MlflowPlugin,
KubeflowPlugin, and DatasetPlugin.
It also includes functions to activate, deactivate, and check the status of plugins.

Attributes:
    mlplugin (class): The Mlflow plugin class.
    kfplugin (class): The Kubeflow plugin class.
    dsplugin (class): The Dataset plugin class.
"""

import importlib
import pandas as pd
from sqlalchemy import create_engine, Column, FLOAT, BIGINT, String
from sqlalchemy.orm import declarative_base
from . import plugin_config
from .kubeflowplugin import KubeflowPlugin
from .mlflowplugin import MlflowPlugin
from .dataset_plugin import DatasetPlugin
from . import plugin_status
from .plugin_status import plugin_statuses


Base = declarative_base()


class ModelTraining(Base):
    """
    SQLAlchemy ORM class representing the 'Model_training' table in the PostgreSQL database.

    This table stores information related to model training, including parameters, metrics,
    and other metadata associated with training runs.

    Attributes:
        param_key (str): Key for the parameter.
        param_value (str): Value of the parameter.
        model_name (str): Name of the model.
        model_version (float): Version of the model.
        creation_time (int): Creation time of the model, represented as a Unix timestamp.
        metric_key (str): Key for the metric.
        metric_value (float): Value of the metric.
        run_name (str): Name of the training run.
        run_uuid (str): UUID of the training run, serves as the primary key.
        user_id (str): Identifier for the user who initiated the training run.
    """

    __tablename__ = "Model_training"
    param_key = Column(String)
    param_value = Column(String)
    model_name = Column(String)
    model_version = Column(FLOAT)
    creation_time = Column(BIGINT)
    metric_key = Column(String)
    metric_value = Column(FLOAT)
    run_name = Column(String)
    run_uuid = Column(String, primary_key=True)
    user_id = Column(String)


class PluginManager:
    """
    Class responsible for managing plugins.

    Attributes:
        mlplugin (class): The Mlflow plugin class.
        kfplugin (class): The Kubeflow plugin class.
        dsplugin (class): The Dataset plugin class.
    """

    def __init__(self):
        """
        Initializes the PluginManager with plugin classes.
        """
        self.mlplugin = MlflowPlugin
        self.kfplugin = KubeflowPlugin
        self.dsplugin = DatasetPlugin

    @staticmethod
    def plugin_names():
        """
        Returns a list of plugin names.

        Returns:
            list: A list of plugin names.
        """
        return ["MlflowPlugin", "KubeflowPlugin", "DatasetPlugin"]

    def check_is_alive(self, name):
        """
        Checks if the plugin is alive.

        Args:
            name (str): The name of the plugin.

        Returns:
            tuple: A tuple containing the status and status code.
        """
        name.is_alive(self)

    def version(self, name):
        """
        Gets the version of the plugin.

        Args:
            name (str): The name of the plugin.
        """
        name.version()

    @staticmethod
    def activate_all_plugins():
        """
        Activates all plugins.
        """
        plugins = PluginManager.plugin_names()
        for plugin_name in plugins:
            PluginManager.activate_plugin(plugin_name)

    @staticmethod
    def deactivate_all_plugins():
        """
        Deactivates all plugins.
        """
        plugins = PluginManager.plugin_names()
        for plugin_name in plugins:
            PluginManager.deactivate_plugin(plugin_name)

    @staticmethod
    def activate_plugin(name):
        """
        Activates a specific plugin.

        Args:
            name (str): The name of the plugin to activate.
        """
        if name not in plugin_statuses:
            print(f"{name} does not exist.")
            return
        if plugin_statuses.get(name) == "activated":
            print(f"{name} already in activated status")
        else:
            plugin_statuses[name] = "activated"
            # Reload plugin_status module to reflect changes
            importlib.reload(plugin_status)

            updated_dict = plugin_status.plugin_statuses

            updated_dict.update(plugin_statuses)

            print(f"{name} is now {plugin_statuses.get(name)}")

    @staticmethod
    def deactivate_plugin(name):
        """
        Deactivates a specific plugin.

        Args:
            name (str): The name of the plugin to deactivate.
        """
        if name not in plugin_statuses:
            print(f"{name} does not exist.")
            return
        if plugin_statuses.get(name) == "deactivated":
            print(f"{name} already in deactivated status")
        else:
            plugin_statuses[name] = "deactivated"
            # Reload plugin_status module to reflect changes
            importlib.reload(plugin_status)

            updated_dict = plugin_status.plugin_statuses

            updated_dict.update(plugin_statuses)

            print(f"{name} is now {plugin_statuses.get(name)}")

    @staticmethod
    def plugin_status():
        """
        Prints the status of all plugins.
        """
        print(plugin_statuses)

    def get_plugin(self, name):
        """
        Gets a specific plugin.

        Args:
            name (str): The name of the plugin to get.
        """
        try:
            PluginManager.version(self, name=name)
            PluginManager.check_is_alive(self, name=name)
        except Exception as e:
            print(f"Plugin error : {e}")

    def get_mlflow_plugin(self):
        """
        Gets the Mlflow plugin if activated.
        """
        if plugin_statuses.get("MlflowPlugin") == "activated":
            # If activated, get the plugin
            PluginManager.get_plugin(self, name=self.mlplugin)
            return MlflowPlugin()
        print("MlflowPlugin is in deactivated status")

    def get_kflow_plugin(self):
        """
        Gets the Kubeflow plugin if activated.
        """
        if plugin_statuses.get("KubeflowPlugin") == "activated":
            PluginManager.get_plugin(self, name=self.kfplugin)
            return KubeflowPlugin()
        print("KubeflowPlugin is in deactivated status")

    def get_dataset_plugin(self):
        """
        Gets the Dataset plugin if activated.
        """
        if plugin_statuses.get("DatasetPlugin") == "activated":
            PluginManager.get_plugin(self, name=self.dsplugin)
            return DatasetPlugin()
        print("DatasetPlugin is in deactivated status")

    def connect_to_cogflow_db(self, dialect="postgresql+psycopg2"):
        """
        Create and return an SQLAlchemy engine for a PostgreSQL database.

        Args:
            dialect (str): The connection string for the PostgreSQL database.

        Returns:
            sqlalchemy.engine.Engine: The SQLAlchemy engine.
        """
        postgres_connection_str = f"{dialect}://hiro:hiropwd@postgres:5432/cognitiveDB"
        engine = create_engine(postgres_connection_str)
        engine.connect()
        return engine

    def insert_data_to_table(self, if_exists: str = "append"):
        """
        Insert data from a pandas DataFrame into a PostgreSQL table.

        Args:
            df (pd.DataFrame): The DataFrame containing data to insert.
            engine: The SQLAlchemy engine to use for the connection.
            table_name (str): The name of the PostgreSQL table to insert data into.
            if_exists (str): Behavior if the table already exists. 'append' to add data,
                             'replace' to drop and recreate the table. Defaults to 'append'.

        Returns:
            None
        """
        df = self.get_params_and_metrics_from_mlflow_db()
        engine = self.connect_to_cogflow_db()
        table_name = ModelTraining.__tablename__
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)

    def connect_to_mlflow_db(self, dialect="mysql+pymysql"):
        """
        Establishes a connection to the MLflow database.

        This method creates an SQLAlchemy engine using the provided database dialect and connection
        parameters from the configuration. It then establishes a connection to the MLflow database
        and returns the engine.

        Args:
            dialect (str): The database dialect to use for the connection (e.g., "mysql+pymysql").
                           Defaults to "mysql+pymysql".

        Returns:
            sqlalchemy.engine.Engine: The SQLAlchemy engine connected to the MLflow database.
        """

        connection_str = (
            f"{dialect}://{plugin_config.ML_USERNAME}:{plugin_config.ML_PASSWORD}"
            f"@{plugin_config.ML_HOST}:{plugin_config.ML_PORT}/{plugin_config.ML_DATABASE_NAME}"
        )
        engine = create_engine(connection_str)
        engine.connect()
        return engine

    def get_params_and_metrics_from_mlflow_db(self):
        """
        Retrieves parameters and metrics from the MLflow database.

        This method queries the MLflow database to retrieve parameters, metrics, and associated
        information such as model name, version, creation time, and other metadata for each run.
        The method executes a SQL query to join multiple tables and returns the results as a pandas
        DataFrame.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the parameters and metrics data from the
                          MLflow database. Each row represents a run with columns for the parameter key,
                          parameter value, model name, model version, creation time, metric key,
                          metric value, run name, run UUID, and user ID.
        """

        metric_query = """
        SELECT p.key AS param_key, p.value AS param_value,
               mv.name AS model_name, mv.version AS model_version, mv.creation_time,
               m.key AS metric_key, m.value AS metric_value,
               r.name AS run_name, r.run_uuid AS run_uuid, r.user_id
        FROM params p
        JOIN model_versions mv ON p.run_uuid = mv.run_id
        JOIN metrics m ON p.run_uuid = m.run_uuid
        JOIN runs r ON p.run_uuid = r.run_uuid;
        """
        engine = self.connect_to_mlflow_db()

        df = pd.read_sql_query(metric_query, engine)
        return df
