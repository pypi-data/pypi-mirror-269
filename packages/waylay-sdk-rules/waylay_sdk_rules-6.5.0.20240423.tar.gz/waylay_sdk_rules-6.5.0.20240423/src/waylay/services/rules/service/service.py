"""Rules Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.about_api import AboutApi
from ..api.plugs_execution_api import PlugsExecutionApi
from ..api.push_data_api import PushDataApi
from ..api.task_nodes_api import TaskNodesApi
from ..api.tasks_api import TasksApi
from ..api.tasks_batch_operations_api import TasksBatchOperationsApi
from ..api.template_runs_api import TemplateRunsApi
from ..api.templates_api import TemplatesApi


class RulesService(WaylayService):
    """Rules Service Class."""

    name = "rules"
    title = "Rules Service"

    about: AboutApi
    plugs_execution: PlugsExecutionApi
    push_data: PushDataApi
    task_nodes: TaskNodesApi
    tasks: TasksApi
    tasks_batch_operations: TasksBatchOperationsApi
    template_runs: TemplateRunsApi
    templates: TemplatesApi

    def __init__(self, api_client: ApiClient):
        """Create the rules service."""

        super().__init__(api_client)
        self.about = AboutApi(api_client)
        self.plugs_execution = PlugsExecutionApi(api_client)
        self.push_data = PushDataApi(api_client)
        self.task_nodes = TaskNodesApi(api_client)
        self.tasks = TasksApi(api_client)
        self.tasks_batch_operations = TasksBatchOperationsApi(api_client)
        self.template_runs = TemplateRunsApi(api_client)
        self.templates = TemplatesApi(api_client)
