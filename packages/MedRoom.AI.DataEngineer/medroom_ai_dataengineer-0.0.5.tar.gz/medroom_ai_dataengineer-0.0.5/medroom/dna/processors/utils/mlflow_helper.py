# Importando Libs
import json
import pickle
import tempfile

import mlflow
from mlflow.entities import Experiment
from PIL import Image


class MLFlowHelper:
    def __init__(self, server_url, experiment_name):
        mlflow.set_tracking_uri(f"{server_url}")  # Define o URI de rastreamento do MLflow
        self.experiment = self.create_or_get_experiment(experiment_name)  # Cria ou recupera um experimento
        self.artifact_handlers = {
            "img": self._process_image_artifact,  # Handler para imagens
            "df_example": self._process_dataframe_artifact,  # Handler para exemplos de DataFrame
            "model": self._process_model_artifact,  # Handler para modelos
        }

    def load_data_pickle(self, nome_arquivo):
        with open(nome_arquivo, "rb") as arquivo:
            return pickle.load(arquivo)  # Carrega dados de um arquivo pickle

    def create_or_get_experiment(self, experiment_name: str) -> Experiment:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            experiment_id_created = mlflow.create_experiment(experiment_name)
            print(f"Experimento '{experiment_name}' não existe, criando ele com id {experiment_id_created}.")
            return mlflow.get_experiment_by_name(experiment_name)
        else:
            print(f"Experimento '{experiment_name}' já existe, usando ele com id {experiment.experiment_id}.")
            return experiment

    def log_run(self, consolidated_data):
        with mlflow.start_run(experiment_id=self.experiment.experiment_id):
            self._log_parameters(consolidated_data["params"])  # Registra os parâmetros do experimento
            self._log_metrics(consolidated_data["metrics"])  # Registra as métricas do experimento
            self._set_tags(consolidated_data["tags"])  # Define tags para o experimento
            try:
                self._process_artifacts(consolidated_data["artifacts"])  # Processa e registra os artefatos
                print("Todos os artefatos foram logados com sucesso.")
            except Exception as e:
                print(f"Erro ao logar artefatos: {e}")

    def _log_parameters(self, params):
        try:
            for key, value in params.items():
                mlflow.log_param(key, str(value))  # Registra um parâmetro no MLflow
            print("Parâmetros logados com sucesso.")
        except Exception as e:
            print(f"Erro ao logar parâmetros: {e}")

    def _log_metrics(self, metrics):
        try:
            for key, value in metrics.items():
                mlflow.log_metric(key, value)  # Registra uma métrica no MLflow
            print("Métricas logadas com sucesso.")
        except Exception as e:
            print(f"Erro ao logar métricas: {e}")

    def _set_tags(self, tags):
        try:
            for key, value in tags.items():
                mlflow.set_tag(key, value)  # Define uma tag no MLflow
            print("Tags definidas com sucesso.")
        except Exception as e:
            print(f"Erro ao definir tags: {e}")

    def _process_artifacts(self, artifacts):
        for key, value in artifacts.items():
            handler = self._get_artifact_handler(key)  # Obtém o manipulador de artefatos adequado
            if handler:
                try:
                    handler(key, value)  # Processa o artefato específico
                except Exception as e:
                    print(f"Erro ao processar o artefato {key}: {e}")

    def _get_artifact_handler(self, key):
        for handler_key, handler in self.artifact_handlers.items():
            if handler_key in key:
                return handler  # Retorna o manipulador de artefatos com base na chave
        return None

    def _process_image_artifact(self, key, value):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            value.seek(0)
            img = Image.open(value)
            img.save(tmp.name)
            mlflow.log_artifact(tmp.name, f"images/{key}")  # Registra a imagem no MLflow
            print(f"Imagem '{key}' processada e logada com sucesso.")

    def _process_dataframe_artifact(self, key, value):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tmp:
            json.dump(value, tmp)
            tmp.flush()
            mlflow.log_artifact(tmp.name, f"data/{key}")  # Registra o DataFrame no MLflow
            print(f"DataFrame '{key}' processado e logado com sucesso.")

    def _process_model_artifact(self, key, value):
        with tempfile.TemporaryDirectory() as tmpdirname:
            value.save_pretrained(tmpdirname)
            mlflow.pytorch.log_model(pytorch_model=value, artifact_path="model")  # Registra o modelo no MLflow
            print(f"Modelo '{key}' processado e logado com sucesso.")
