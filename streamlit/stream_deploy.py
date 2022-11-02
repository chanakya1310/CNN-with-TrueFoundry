import logging

from servicefoundry import Build, PythonBuild, Service

logging.basicConfig(level=logging.INFO)

service = Service(
    name="streamlit",
    image=Build(
        build_spec=PythonBuild(
            command="streamlit run main.py",
        ),
    ),
    ports=[{"port": 8501}],
)

deployment = service.deploy(workspace_fqn="<YOUR WORKSPACE FQN HERE>")
