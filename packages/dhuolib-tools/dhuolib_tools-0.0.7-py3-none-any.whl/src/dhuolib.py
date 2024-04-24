from src.config import logger
from src.oci.utils import OCIUtils
from src.services import ServiceAPIML


class DhuolibClient:
    def __init__(self, service_endpoint=None, config_file_path='~/.oci/config'):
        if not service_endpoint:
            raise ValueError("service_endpoint is required")

        self.service = ServiceAPIML(service_endpoint)
        self.oci = OCIUtils(config_file_path=config_file_path)

    def create_experiment(self, experiment_params) -> str:
        if "file_path" not in experiment_params.keys():
            file_path = experiment_params["file"]["filepath"]
            bucket_name = experiment_params["file"]["bucket"]
            namespace = experiment_params["file"]["namespace"]
            self.oci.upload_file(
                file_path=file_path, bucket_name=bucket_name, namespace=namespace
            )

        response = self.service.create_experiment_by_conf_json(experiment_params)
        experiment = response.json()
        logger.info(
            f"Experiment Name: {experiment_params['experiment_name']}"
            f"Experiment ID: {experiment['experiment_id']} created"
        )
        return experiment

    def run_experiment(self, run_params) -> str:
        if run_params["experiment_id"] is None:
            experiment_id = self.create_experiment(run_params)
            run_params["experiment_id"] = experiment_id

        response = self.service.run_experiment(run_params)
        logger.info(f"Experiment ID: {run_params['experiment_id']} running")
        return response.json()

    def load_model(self, model_name, tag) -> str:
        print("loading model")
        return "model_name.pkl"

    def predict(self):
        pass

    def read_from_bucket(self, bucket: str, filename: str):
        # OCI, GCP, AWS
        return f"folder/{filename}"

    # def read_from_bucket(self, filename: str):
    #     default_bucket = "s3://default"
    #     return self.read_from_bucket(default_bucket, filename)

    def execute_select(self, statement: str):
        # Acesso pela API ML Service
        # Processo assíncrono
        file = "s3://bucket/temp/file1.csv"
        return file

    def execute_dml(self, statement: str):
        # rows_count - linhas afetadas

        rows_count = 0
        return rows_count

    # Promover o model_name para "production"

    # - [ ] criar cluster no Dataflow
    # - [ ] informar o dado de schedule e criação de aplicação Dataflow
    # - [ ] inserção de lista de dependencias: libs + zip + script.py

    # @hydra.main(config_path="config", config_name="deploy")
    def deploy(self, params):

        # Enfileira o serviços

        return None

    def save_predictions(
        self, dataset_predictions, inputs, predictions, model_name, tag
    ):

        return ""


if __name__ == "__main__":
    dhuolib = Dhuolib()

    experiment = "classificacao para recomendação"
    experiment_id = dhuolib.create_experiment(experiment)

    file = "pickle.file"
    model_name = "model_decision_tree"
    tag = "1.0.1"

    save_status = dhuolib.save_model(experiment_id, file, model_name, tag)
    print(save_status)

    file = "pickle.file"
    model_name = "model_logistic"
    tag = "1.0.2"

    save_status = dhuolib.save_model(experiment_id, file, model_name, tag)
    print(save_status)

    file = dhuolib.load_model("model_decision_tree", "1.0.1")

    data_input = {"x": 1}
    predictions = dhuolib.predict("model_decision_tree", "1.0.1", data_input)

    dhuolib.deploy()
