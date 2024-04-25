import unittest

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from tabpfn import TabPFNClassifier as LocalTabPFNClassifier

from tabpfn_client import tabpfn_classifier, TabPFNClassifier
from tabpfn_client.tests.mock_tabpfn_server import with_mock_server
from tabpfn_client.service_wrapper import UserAuthenticationClient
from tabpfn_client.client import ServiceClient


class TestTabPFNClassifier(unittest.TestCase):
    def setUp(self):
        X, y = load_breast_cancer(return_X_y=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    def tearDown(self):
        tabpfn_classifier.reset()
        ServiceClient().delete_instance()

    def test_use_local_tabpfn_classifier(self):
        tabpfn_classifier.init(use_server=False)
        tabpfn = TabPFNClassifier(device="cpu", model="tabpfn_1_local")
        tabpfn.fit(self.X_train, self.y_train)

        self.assertTrue(isinstance(tabpfn.classifier_, LocalTabPFNClassifier))
        pred = tabpfn.predict(self.X_test)
        self.assertEqual(pred.shape[0], self.X_test.shape[0])

    @with_mock_server()
    def test_use_remote_tabpfn_classifier(self, mock_server):
        # create dummy token file
        token_file = UserAuthenticationClient.CACHED_TOKEN_FILE
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_file.write_text("dummy token")

        # mock connection and authentication
        mock_server.router.get(mock_server.endpoints.root.path).respond(200)
        mock_server.router.get(mock_server.endpoints.protected_root.path).respond(200)
        mock_server.router.get(mock_server.endpoints.retrieve_greeting_messages.path).respond(
            200, json={"messages": []})
        tabpfn_classifier.init(use_server=True)

        tabpfn = TabPFNClassifier()

        # mock fitting
        mock_server.router.post(mock_server.endpoints.upload_train_set.path).respond(
            200, json={"train_set_uid": 5})
        tabpfn.fit(self.X_train, self.y_train)

        # mock prediction
        mock_server.router.post(mock_server.endpoints.predict.path).respond(
            200,
            json={"y_pred": LocalTabPFNClassifier().fit(self.X_train, self.y_train).predict(self.X_test).tolist()}
        )
        pred = tabpfn.predict(self.X_test)
        self.assertEqual(pred.shape[0], self.X_test.shape[0])
