"""Convenience API to initialize and access all Edge impulse."""

# Import the sub packages here to expose them to the user
# ruff: noqa: F401, D107
import os
import edgeimpulse.model
import edgeimpulse.exceptions
import edgeimpulse.experimental
from edgeimpulse.util import configure_generic_client, default_project_id_for

import edgeimpulse_api as edge_api
from typing import Optional
from edgeimpulse.util import (
    run_project_job_until_completion as run_project_job_until_completion_util,
    run_organization_job_until_completion as run_organization_job_until_completion_util,
)


class EdgeImpulseApi:
    """Initialize the Edge Impulse Api.

    Args:
        host (str, optional): The host address. None will use the production host. Defaults to None
        key (str, optional): The authentication key to use. If none given, it will use no authentication.
        key_type (str, optional): The type of key. Can be `api`, `jwt` or `jwt_http`. Defaults to `api`.
    """

    @property
    def user(self) -> edge_api.UserApi:
        """Manage user activating, creation, updating and information."""
        return self._user

    @property
    def classify(self) -> edge_api.ClassifyApi:
        """Classify samples."""
        return self._classify

    @property
    def deployment(self) -> edge_api.DeploymentApi:
        """Work with deployment targets."""
        return self._deployment

    @property
    def devices(self) -> edge_api.DevicesApi:
        """Work with devices in your project."""
        return self._devices

    @property
    def dsp(self) -> edge_api.DSPApi:
        """Work with digital signal processing (feature extraction)."""
        return self._dsp

    @property
    def export(self) -> edge_api.ExportApi:
        """Export datasets and projects."""
        return self._export

    @property
    def feature_flags(self) -> edge_api.FeatureFlagsApi:
        """Enable and disable feature flags."""
        return self._feature_flags

    @property
    def impulse(self) -> edge_api.ImpulseApi:
        """Work and manage your impulse."""
        return self._impulse

    @property
    def jobs(self) -> edge_api.JobsApi:
        """Start and manage long running jobs."""
        return self._jobs

    @property
    def learn(self) -> edge_api.LearnApi:
        """Work with keras and pretrained models."""
        return self._learn

    @property
    def login(self) -> edge_api.LoginApi:
        """Login and authenticate."""
        return self._login

    @property
    def optimization(self) -> edge_api.OptimizationApi:
        """Optimize the model with the eon tuner."""
        return self._optimization

    @property
    def organization_blocks(self) -> edge_api.OrganizationBlocksApi:
        """Work with organization blocks."""
        return self._organization_blocks

    @property
    def organization_create_project(self) -> edge_api.OrganizationCreateProjectApi:
        """Automate project creation for organizations."""
        return self._organization_create_project

    @property
    def organization_data(self) -> edge_api.OrganizationDataApi:
        """Work with organization data."""
        return self._organization_data

    @property
    def organization_data_campaigns(self) -> edge_api.OrganizationDataCampaignsApi:
        """Work with organization campaigns."""
        return self._organization_data_campaigns

    @property
    def organization_jobs(self) -> edge_api.OrganizationJobsApi:
        """Start run and manage organization jobs."""
        return self._organization_jobs

    @property
    def organization_pipelines(self) -> edge_api.OrganizationPipelinesApi:
        """Work with organization pipelines."""
        return self._organization_pipelines

    @property
    def organization_portals(self) -> edge_api.OrganizationPortalsApi:
        """Create and manage organization portals."""
        return self._organization_portals

    @property
    def organizations(self) -> edge_api.OrganizationsApi:
        """Work with your organizations."""
        return self._organizations

    @property
    def performance_calibration(self) -> edge_api.PerformanceCalibrationApi:
        """Calibrate your model with real world data."""
        return self._performance_calibration

    @property
    def projects(self) -> edge_api.ProjectsApi:
        """Create and manage your projects."""
        return self._projects

    @property
    def raw_data(self) -> edge_api.RawDataApi:
        """Work with your project data."""
        return self._raw_data

    @property
    def upload_portal(self) -> edge_api.UploadPortalApi:
        """Create and manage data upload portals."""
        return self._upload_portal

    @property
    def host(self) -> Optional[str]:
        """Edge Impulse studio host (defaults to production)."""
        return self._host

    @property
    def client(self) -> edge_api.ApiClient:
        """The client used for initializing the apis, use `set_client` to update the client."""
        return self._client

    def __init__(
        self,
        host: Optional[str] = None,
        key: Optional[str] = None,
        key_type: str = "api",
    ):
        self._host = host
        config = edge_api.Configuration(self._host)
        if key is None:
            client = edge_api.ApiClient(config)
            self.set_client(client)
        else:
            self.authenticate(key=key, key_type=key_type)

    def run_project_job_until_completion(
        self,
        job_id: int,
        data_cb=None,
        client=None,
        project_id: Optional[int] = None,
        timeout_sec: Optional[int] = None,
    ) -> None:
        """Runs a project job until completion.

        Args:
            job_id (int): The ID of the job to run.
            data_cb (callable, optional): Callback function to handle job data.
            client (object, optional): An API client object. If None, a generic client will be configured.
            project_id (int, optional): The ID of the project. If not provided, a default project ID will be used.
            timeout_sec (int, optional): Number of seconds before timeing out the job with an exception. Default is None

        Returns:
            None
        """
        if client is None:
            client = self._client

        return run_project_job_until_completion_util(
            job_id=job_id,
            client=client,
            data_cb=data_cb,
            project_id=project_id,
            timeout_sec=timeout_sec,
        )

    def run_organization_job_until_completion(
        self,
        organization_id: int,
        job_id: int,
        data_cb=None,
        client=None,
        timeout_sec: Optional[int] = None,
    ) -> None:
        """Runs an organization job until completion.

        Args:
            organization_id (int): The ID of the organization.
            job_id (int): The ID of the job to run.
            data_cb (callable, optional): Callback function to handle job data.
            client (object, optional): An API client object. If None, a generic client will be configured.
            timeout_sec (int, optional): Number of seconds before timeing out the job with an exception. Default is None.

        Returns:
            None
        """
        if client is None:
            client = self._client

        return run_organization_job_until_completion_util(
            job_id=job_id,
            client=client,
            data_cb=data_cb,
            organization_id=organization_id,
            timeout_sec=timeout_sec,
        )

    def default_project_id(self) -> int:
        """Retrieve the default project ID from the api key.

        Returns:
            int: The project associated with the api key.
        """
        return default_project_id_for(self._client)

    def authenticate(
        self, key: str, key_type: str = "api", host: Optional[str] = None
    ) -> None:
        """Authenticate against Edge Impulse.

        Args:
            key (str): The authentication key to use. If none give, it will use no authentication.
            key_type (str, optional): The type of key. Can be `api`, `jwt` or `jwt_http`. Defaults to `api`.
            host (str, optional): The host address. None will use the production host. Defaults to None
        """
        host_url = host or self._host
        client = configure_generic_client(key=key, key_type=key_type, host=host_url)
        self.set_client(client)

    def set_client(self, client: edge_api.ApiClient) -> None:
        """Set the API client and initialize the APIs wit that client.

        Args:
            client: The API client.
        """
        self._client = client
        self._user = edge_api.UserApi(client)
        self._classify = edge_api.ClassifyApi(client)
        self._deployment = edge_api.DeploymentApi(client)
        self._devices = edge_api.DevicesApi(client)
        self._dsp = edge_api.DSPApi(client)
        self._export = edge_api.ExportApi(client)
        self._feature_flags = edge_api.FeatureFlagsApi(client)
        self._impulse = edge_api.ImpulseApi(client)
        self._jobs = edge_api.JobsApi(client)
        self._learn = edge_api.LearnApi(client)
        self._login = edge_api.LoginApi(client)
        self._optimization = edge_api.OptimizationApi(client)
        self._organization_blocks = edge_api.OrganizationBlocksApi(client)
        self._organization_create_project = edge_api.OrganizationCreateProjectApi(
            client
        )
        self._organization_data = edge_api.OrganizationDataApi(client)
        self._organization_data_campaigns = edge_api.OrganizationDataCampaignsApi(
            client
        )
        self._organization_jobs = edge_api.OrganizationJobsApi(client)
        self._organization_pipelines = edge_api.OrganizationPipelinesApi(client)
        self._organization_portals = edge_api.OrganizationPortalsApi(client)
        self._organizations = edge_api.OrganizationsApi(client)
        self._performance_calibration = edge_api.PerformanceCalibrationApi(client)
        self._projects = edge_api.ProjectsApi(client)
        self._raw_data = edge_api.RawDataApi(client)
        self._upload_portal = edge_api.UploadPortalApi(client)
