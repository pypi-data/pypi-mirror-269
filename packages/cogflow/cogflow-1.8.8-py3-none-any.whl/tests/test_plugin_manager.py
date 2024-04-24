"""
    This file contains unittest for PluginManager methods
"""

import unittest
from io import StringIO
from unittest.mock import patch
from cogflow.cogflow.pluginmanager import PluginManager
from cogflow.cogflow.mlflowplugin import MlflowPlugin
from cogflow.cogflow.kubeflowplugin import KubeflowPlugin
from cogflow.cogflow.dataset_plugin import DatasetPlugin
from cogflow.cogflow.plugin_status import plugin_statuses


class TestPluginManager(unittest.TestCase):
    """
    Test class for PluginManger
    """

    def setUp(self):
        """
            Initial setup
        :return:
        """
        self.plugin_manager = PluginManager()
        self.mlflow_plugin = MlflowPlugin()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.is_alive")
    @patch("cogflow.cogflow.kubeflowplugin.KubeflowPlugin.is_alive")
    @patch("cogflow.cogflow.mlflowplugin.MlflowPlugin.is_alive")
    def test_check_is_alive(
        self, mock_mlflow_plugin, mock_kubeflow_plugin, mock_dataset_plugin
    ):
        """
            test case to check the is_alive method
        :param mock_mlflow_plugin:
        :param mock_kubeflow_plugin:
        :param mock_dataset_plugin:
        :return:
        """
        self.plugin_manager.check_is_alive(MlflowPlugin)
        mock_mlflow_plugin.assert_called_once()

        self.plugin_manager.check_is_alive(KubeflowPlugin)
        mock_kubeflow_plugin.assert_called_once()

        self.plugin_manager.check_is_alive(DatasetPlugin)
        mock_dataset_plugin.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.version")
    @patch("cogflow.cogflow.kubeflowplugin.KubeflowPlugin.version")
    @patch("cogflow.cogflow.mlflowplugin.MlflowPlugin.version")
    def test_check_version(
        self, mock_mlflow_plugin, mock_kubeflow_plugin, mock_dataset_plugin
    ):
        """
            test case to check the version method
        :param mock_mlflow_plugin:
        :param mock_kubeflow_plugin:
        :param mock_dataset_plugin:
        :return:
        """
        self.plugin_manager.version(MlflowPlugin)
        mock_mlflow_plugin.assert_called_once()

        self.plugin_manager.version(KubeflowPlugin)
        mock_kubeflow_plugin.assert_called_once()

        self.plugin_manager.version(DatasetPlugin)
        mock_dataset_plugin.assert_called_once()

    def test_activate_plugins(self):
        """
            test case for activate_plugins
        :return:
        """
        self.plugin_manager.activate_all_plugins()
        for item, value in plugin_statuses.items():
            print(item, ":", value)
            self.assertEqual(value, "activated")

    def test_deactivate_plugins(self):
        """
            test case for deactivate_plugins
        :return:
        """
        self.plugin_manager.deactivate_all_plugins()
        for item, value in plugin_statuses.items():
            print(item, ":", value)
            self.assertEqual(value, "deactivated")

    @patch("sys.stdout", new_callable=StringIO)
    def test_activate_plugin(self, mock_stdout):
        """
            test case for activate_plugin check
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.activate_plugin("MlflowPlugin")

        printed_output = mock_stdout.getvalue()

        # Assert that the printed output contains the specified string
        self.assertIn("activated", printed_output)
        self.assertNotIn("deactivated", printed_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_activate_plugin_not_valid(self, mock_stdout):
        """
            test case for activate_plugin when plugin is not valid
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.activate_plugin("XPlugin")

        printed_output = mock_stdout.getvalue()

        # Assert that the printed output contains the specified string
        self.assertIn("does not exist.", printed_output)
        # self.assertNotIn("deactivated", printed_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_deactivate_plugin(self, mock_stdout):
        """
            test to check deactivate_plugin
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.deactivate_plugin("MlflowPlugin")

        printed_output = mock_stdout.getvalue()

        # Assert that the printed output contains the specified string
        self.assertIn("deactivated", printed_output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_deactivate_plugin_not_valid(self, mock_stdout):
        """
            test to check deactivate_plugin when plugin is not valid
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.deactivate_plugin("XPlugin")

        printed_output = mock_stdout.getvalue()

        # Assert that the printed output contains the specified string
        self.assertIn("does not exist.", printed_output)
        # self.assertNotIn("deactivated", printed_output)

    @patch("cogflow.cogflow.mlflowplugin.MlflowPlugin.is_alive")
    @patch("sys.stdout", new_callable=StringIO)
    def test_get_plugin(self, mock_stdout, mock_mlflow_plugin):
        """
            test for get_plugin given a plugin type
        :param mock_stdout:
        :param mock_mlflow_plugin:
        :return:
        """
        mock_mlflow_plugin.side_effect = Exception()

        self.plugin_manager.get_plugin(MlflowPlugin)

        self.assertIn("Plugin error", mock_stdout.getvalue())

    def test_get_mlflow_plugin(self):
        """
            test for get_mlflow_plugin
        :return:
        """
        self.plugin_manager.activate_plugin("MlflowPlugin")

        self.assertIsInstance(self.plugin_manager.get_mlflow_plugin(), MlflowPlugin)

    @patch("sys.stdout", new_callable=StringIO)
    def test_get_mlflow_plugin_deactivated(self, mock_stdout):
        """
            test for get_mlflow_plugin when plugin deactivated
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.deactivate_plugin("MlflowPlugin")
        self.plugin_manager.get_mlflow_plugin()
        self.assertIn("MlflowPlugin is in deactivated status", mock_stdout.getvalue())

    def test_get_kubeflow_plugin(self):
        """
            test for get_kubeflow_plugin
        :return:
        """
        self.plugin_manager.activate_plugin("KubeflowPlugin")

        self.assertIsInstance(self.plugin_manager.get_kflow_plugin(), KubeflowPlugin)

    @patch("sys.stdout", new_callable=StringIO)
    def test_get_kubeflow_plugin_deactivated(self, mock_stdout):
        """
            test to get_kubeflow_plugin when plugin deactivated
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.deactivate_plugin("KubeflowPlugin")
        self.plugin_manager.get_kflow_plugin()
        self.assertIn("KubeflowPlugin is in deactivated status", mock_stdout.getvalue())

    def test_get_dataset_plugin(self):
        """
            test to get dataset_plugin
        :return:
        """
        self.plugin_manager.activate_plugin("DatasetPlugin")

        self.assertIsInstance(self.plugin_manager.get_dataset_plugin(), DatasetPlugin)

    @patch("sys.stdout", new_callable=StringIO)
    def test_get_dataset_plugin_deactivated(self, mock_stdout):
        """
            test to get dataset_plugin when plugin deactivated
        :param mock_stdout:
        :return:
        """
        self.plugin_manager.deactivate_plugin("DatasetPlugin")
        self.plugin_manager.get_dataset_plugin()
        self.assertIn("DatasetPlugin is in deactivated status", mock_stdout.getvalue())
