import argparse
import logging

from servicefoundry import Build, PythonBuild, Resources, Service

# parsing the input arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--workspace_fqn",
    type=str,
    required=True,
    help="fqn of workspace where you want to deploy",
)
parser.add_argument(
    "--model_version_fqn",
    type=str,
    required=True,
    help="fqn of model_version where you want to deploy",
)
args = parser.parse_args()

# creating a service object and defining all the configurations
service = Service(
    name="cat-dog-classifier",
    image=Build(
        build_spec=PythonBuild(
            command="uvicorn infer_realtime:app --port 4000 --host 0.0.0.0",
            python_version="3.9",
        ),
    ),
    env={
        # These will automatically map the secret value to the environment variable.
        "MLF_HOST": "https://app.develop.truefoundry.tech",
        "MLF_API_KEY": "<YOUR API KEY HERE>",
        "MLF_MODEL_VERSION_FQN": args.model_version_fqn,
    },
    ports=[{"port": 4000}],
    resources=Resources(
        cpu_request=0.5, cpu_limit=1.5, memory_limit=2500, memory_request=1500
    ),
)
service.deploy(workspace_fqn=args.workspace_fqn)
