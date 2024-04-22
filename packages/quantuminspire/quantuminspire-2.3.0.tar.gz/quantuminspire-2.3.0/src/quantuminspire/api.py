# Quantum Inspire SDK
#
# Copyright 2022 QuTech Delft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module api
==========

.. autoclass:: QuantumInspireAPI
   :members:
"""

import re
import itertools
import logging
import time
import uuid
from typing import Type, List, Dict, Union, Optional, Any, Tuple
from urllib.parse import urljoin

from coreapi.auth import TokenAuthentication, AuthBase
from coreapi.client import Client
from coreapi.exceptions import CoreAPIException, ErrorMessage
from coreapi.transports import HTTPTransport

from quantuminspire.credentials import load_account
from quantuminspire.exceptions import ApiError, AuthenticationError
from quantuminspire.job import QuantumInspireJob

logger = logging.getLogger(__name__)
V1_MEASUREMENT_BLOCK_INDEX = -1  # -1 for last block
QI_URL = 'https://api.quantum-inspire.com'


class VersionedAPITransport(HTTPTransport):  # type: ignore[misc]
    """ VersionedAPITransport makes it possible to address a specific version of the API of quantum inspire.
    """
    def __init__(self, api_version: str = '2.0', auth: AuthBase = None) -> None:
        self._api_version = api_version
        super().__init__(auth=auth, headers=self.headers)

    @property
    def headers(self) -> Dict[str, str]:
        """ Return accept string for versioned transport """
        return {
            'accept': f'application/coreapi+json, application/vnd.coreapi+json, */*; version={self._api_version};'
        }


class QuantumInspireAPI:
    def __init__(self, base_uri: str = QI_URL, authentication: Optional[AuthBase] = None,
                 project_name: Optional[str] = None,
                 coreapi_client_class: Type[Client] = Client) -> None:
        """ Python interface to the Quantum Inspire API (Application Programmer Interface).

        The Quantum Inspire API supplies an interface for executing programs and can be used to access the
        different entities in the Quantum Inspire database needed for running the programs.
        The entities for which an interface is provided are:

            * Backend types: Depending on the user account more qubits can be used and simulated on faster hardware.
            * Projects: Executing programs is done from a project. Projects keep track of the other entities.
            * Jobs: A job contains all the information and the parameters needed for executing the program.
            * Assets: A container for a cQASM program. Is part of a job.
            * Results: After the job is finished, the results are gathered in the result-entity.

        QuantumInspireAPI is a convenient interface (or wrapper) to the low level API and hides details for
        requesting data (via get) and performing operations on the different entities (via actions).

        The API version that is used by SDK version 2.0.0 and higher defaults to 2.0.
        Version 2.0 is introduced for serving backends that support multiple measurement algorithms.
        Backends that support multiple measurement algorithms have a flag defined called 'multiple_measurement' in their
        backend type structure (See :meth:`~.get_default_backend_type`).

        To support multiple measurement the results structure has changed to hold the results for each measurement block
        defined in a multiple measurement algorithm. Backends that do not support multiple measurement algorithms have
        1 measurement block. See :meth:`~.get_result` for details.

        For more documentation:
            * The knowledge base on: https://www.quantum-inspire.com/kbase/low-level-api/
            * The REST API can be found on: https://api.quantum-inspire.com/
            * The Core API schema is published on: https://api.quantum-inspire.com/schema/

        :param base_uri: The base uri of the Quantum Inspire API-location where the schema can be found
                in path 'schema/').
        :param authentication: The authentication, can be one of the following :mod:`coreapi` authentications:

                 * :class:`~coreapi.auth.BasicAuthentication(email, password)`,
                   HTTP authentication with valid email/password.
                 * :class:`~coreapi.auth.TokenAuthentication(token, scheme="token")`,
                   token authentication with a valid API-token.

                When authentication is :obj:`None`, a token is read from the default location.
        :param project_name: The name of the project used for executing the jobs.
        :param coreapi_client_class: Coreapi client to interact with the API through a schema.
                Default set to :class:`coreapi.Client`.

        :raises AuthenticationError: When no authentication is given
                and the token could not be loaded from the default location.
        :raises ApiError: When the schema could not be loaded.

        .. note::
            When no project name is given, a temporary project is created for the job and deleted after the job
            has finished. When a project name is given, a project is created if it does not exist, but re-used
            if a project with that name already exists. In either case, the project will not be deleted when
            the job has finished.

        """
        if authentication is None:
            token = load_account()
            if token is not None:
                authentication = TokenAuthentication(token, scheme="token")
            else:
                raise AuthenticationError('No credentials have been provided or found on disk')

        self.__client = coreapi_client_class(transports=[VersionedAPITransport(auth=authentication)])
        self.project_name = project_name
        self.base_uri = base_uri if base_uri[-1] == '/' else base_uri + '/'
        self.enable_fsp_warning = True
        try:
            self._load_schema()
        except (CoreAPIException, TypeError) as ex:
            raise ApiError(f'Could not connect to {base_uri}') from ex

    def _get(self, uri_path: str) -> Any:
        """ Method for making requests to the coreapi client instance to get some piece of information.

        The information requested depends on the uri_path parameter.

        :param uri_path: The URL where to request the data.

        :raises TypeError: When the uri_path is not correct.
        :raises CoreAPIException: When the get was not successful. Possible causes are:

            * The schema is not loaded, or
            * A network error occurred.

        :raises ErrorMessage: When the result of the get is not successful.

        :return: The resulting data from the get-request. The structure of the data depends on the request.

        .. note:
            This method will be made private in the near future. Usage is discouraged.

        """
        return self.__client.get(uri_path)

    def show_fsp_warning(self, enable: bool = True) -> None:
        """ Enable or disable the warning that is printed when a non-FSP (full state projection) job is about to run.

        :param enable: when True the fsp-warning is shown, otherwise not.

        """
        self.enable_fsp_warning = enable

    def _action(self, action: List[str], params: Optional[Dict[str, Any]] = None) -> Any:
        """ Adapter for performing an action on an object via the Quantum Inspire API.

        :param action: Path in the schema hierarchy selecting the requested action.
        :param params: Some actions may accept a set of parameters with names as keys.

        :raises CoreAPIException: When the action was not successful. Possible causes are:

            * One of the actions or parameters not supported,
            * the schema is not loaded, or
            * a network error occurred.

        :raises CoreAPIException.ErrorMessage: When the result of the action is not successful.

        :return: The resulting data from the action-request. The structure of the data depends on the request.
            Can be None when there is no content in the response.
        """
        return self.__client.action(self.document, action, params=params)

    def _load_schema(self) -> None:
        """ Loads the schema with metadata that explains how the api-data is structured."""
        self.document = self._get(urljoin(self.base_uri, 'schema/'))

    def list_backend_types(self) -> None:
        """ Prints the backend types with the name and the maximum number of qubits it supports."""
        backends = self.get_backend_types()
        for backend in backends:
            print(f'Backend type: {backend["name"]}, number of qubits: {backend["number_of_qubits"]}')

    def get_default_backend_type(self) -> Dict[str, Any]:
        """ Gets the properties of the default backend type.

        :return: The default backend type with all of its properties:

            =================================== =========== ============================================================
            Key                                 Type        Description
            =================================== =========== ============================================================
            ``url``                             str         The url for the backend type.
            ``name``                            str         Name of the backend.
            ``is_hardware_backend``             bool        Indicates whether the backend is a hardware backend (True)
                                                            or a simulating backend (False).
            ``required_permission``             str         Describes the permission that is required
                                                            to use this backend.
            ``number_of_qubits``                int         Maximum number of qubits the backend supports.
            ``description``                     str         Short description of the backend.
            ``topology``                        dict        Dictionary with property `edges` that contains a list of
                                                            tuples that define qubit connectivity for 2-qubit gates.
            ``is_allowed``                      bool        Indicates whether the user is allowed to use this backend.
            ``status``                          str         Status of the backend.
            ``status_message``                  str         Extra info about the status of the backend.
            ``chip_image_id``                   str         Unique identification of the chip.
            ``calibration``                     str         Calibration information (url).
            ``allowed_operations``              dict        The gates/operations names that the backend can handle.
            ``default_number_of_shots``         int         The default number of shots for an experiment.
            ``max_number_of_shots``             int         The maximum number of shots for an experiment.
            ``max_number_of_simultaneous_jobs`` int         The maximum number of jobs that is allowed to be queued for
                                                            the backend simultaneously (0 = no limit).
            ``operations_count``                dict        The maximum number of gates that is allowed in an experiment
                                                            for each qubit separately and for the experiment in total
                                                            (0 = no limit).
            ``flags``                           list[str]   flags defining capabilities of the backends. E.g.
                                                            'multiple_measurement', 'parallel_computing'
            =================================== =========== ============================================================

        """
        return dict(self._action(['backendtypes', 'default', 'list']))

    def get_backend_types(self) -> List[Dict[str, Any]]:
        """ Gets a list of backend types with properties.

        :return:
            A list of backend types with all of their properties.
            See :meth:`~.get_default_backend_type`
            for a description of the backend properties.
        """
        ret: List[Dict[str, Any]] = self._action(['backendtypes', 'list'])
        return ret

    def get_backend_type_by_id(self, backend_type_id: int) -> Dict[str, Any]:
        """ Gets the properties of a specific backend type, given the backend type id.

        :param backend_type_id: The backend identification number.

        :raises ApiError: When the backend type indicated by backend_type_id does not exist.

        :return:
            The requested backend type indicated by backend_type_id with all of its properties.
            See :meth:`~.get_default_backend_type`
            for a description of the backend type properties.
        """
        try:
            backend_type = self._action(['backendtypes', 'read'], params={'id': backend_type_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Backend type with id {backend_type_id} does not exist!') from err_msg
        return dict(backend_type)

    def get_backend_type_by_name(self, backend_name: str) -> Dict[str, Any]:
        """ Gets the properties of a backend type, given the backend name (case insensitive).

        :param backend_name: The backend name.

        :raises ApiError: When the backend name does not exist.

        :return:
            The properties of the backend type of the specific backend.
            See :meth:`~.get_default_backend_type`
            for a description of the backend type properties.
        """
        backend_type = next((backend for backend in self.get_backend_types()
                            if backend['name'].lower() == backend_name.lower()), None)
        if backend_type is None:
            raise ApiError(f'Backend type with name {backend_name} does not exist!')
        return dict(backend_type)

    def get_backend_type(self, identifier: Optional[Union[int, str]] = None) -> Dict[str, Any]:
        """Gets the properties of the backend type indicated by `identifier`.

        If no `identifier` is given,
        the default backend type will be returned. With an `identifier`
        of type :class:`string` or :class:`int`,
        the backend type will be searched by name or id respectively.

        :param identifier: The backend type identifier.

        :raises ApiError: If the requested backend type does not exist.
        :raises ValueError: If the backend type identifier is not of the correct type.

        :return:
            This method returns the default backend type or the backend type as identified by
            the `identifier` parameter , or the default backend type if no `identifier` is provided.
            See :meth:`~.get_default_backend_type`
            for a description of the backend type properties.
        """
        if identifier is None:
            return self.get_default_backend_type()
        if isinstance(identifier, int):
            return self.get_backend_type_by_id(identifier)
        if isinstance(identifier, str):
            return self.get_backend_type_by_name(identifier)
        raise ValueError('Identifier should be of type int, str or None!')

    #  projects  #

    def list_projects(self) -> None:
        """ Prints a list of projects.

        Prints all the projects registered to the current user the API is authenticated for.
        For each project the name, id and backend type is printed.
        """
        projects = self.get_projects()
        for project in projects:
            print(f'Project name: {project["name"]}, id: {project["id"]}, backend type: {project["backend_type"]}')

    def get_project(self, project_id: int) -> Dict[str, Any]:
        """ Gets the properties of a project, given the project id.

        :param project_id: The project identification number.

        :raises ApiError: If the requested project does not exist.

        :return: The properties describing the project:

            =========================== =========== ==============================================================
            Key                         Type        Description
            =========================== =========== ==============================================================
            ``url``                     str         The url for this project.
            ``id``                      int         Unique id of the project.
            ``name``                    str         Name of the project.
            ``owner``                   int         Url to get the owner of the project.
            ``assets``                  str         Url to get the assets of the project.
            ``backend_type``            str         Url to get the backend type of the project.
            ``default_number_of_shots`` int         Default number of executions for this project.
            ``created``                 str         Date/time when the project was created.
            ``number_of_jobs``          int         Number of jobs managed within this project.
            ``last_saved``              str         Date/time when the project was saved.
            =========================== =========== ==============================================================

        """
        try:
            project = self._action(['projects', 'read'], params={'id': project_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Project with id {project_id} does not exist!') from err_msg
        return dict(project)

    def get_projects(self) -> List[Dict[str, Any]]:
        """ Gets all the projects registered to the user the API is currently authenticated for.

        :return:
            The projects with all of their properties.
            See :meth:`~.get_project` for a description of the project properties.
        """
        ret: List[Dict[str, Any]] = self._action(['projects', 'list'])
        return ret

    def create_project(self, name: str, default_number_of_shots: int, backend_type: Dict[str, Any]) -> Dict[str, Any]:
        """ Creates a new project for executing jobs.

        :param name: The name for the project. The name need not be unique.
        :param default_number_of_shots: The default number of executions of the program before collecting
            the results.
        :param backend_type: The properties of the backend type.

        :return:
            The newly created project with all of its properties.
            See :meth:`~.get_project` for a description of the project properties.
        """
        payload = {
            'name': name,
            'default_number_of_shots': default_number_of_shots,
            'backend_type': backend_type['url'],
        }
        return dict((self._action(['projects', 'create'], params=payload)))

    def delete_project(self, project_id: int) -> None:
        """ Delete a project.

        Deletes the project identified by `project_id` together with all its assets, jobs and results.
        Only projects can be deleted that are registered for the user the API is currently authenticated for.

        :param project_id: The project identification number.

        :raises ApiError: If the project identified by project_id does not exist.
        """
        payload = {
            'id': project_id
        }
        try:
            self._action(['projects', 'delete'], params=payload)
        except ErrorMessage as err_msg:
            raise ApiError(f'Project with id {project_id} does not exist!') from err_msg

    #  jobs  #

    def list_jobs(self) -> None:
        """ Prints a list of jobs.

        Prints a list of all the jobs registered to the current user the API is authenticated for.
        For each job the name, identification number and status is printed.
        """
        jobs = self.get_jobs()
        for job in jobs:
            print(f'Job name: {job["name"]}, id: {job["id"]}, status: {job["status"]}')

    def get_job(self, job_id: int) -> Dict[str, Any]:
        """ Gets the properties of a job, given the job id.

        :param job_id: The job identification number.

        :raises ApiError: If the requested job does not exist.

        :return: The properties describing the job:

            ========================= =========== ==================================================================
            Key                       Type        Description
            ========================= =========== ==================================================================
            ``url``                   str         The url for the job.
            ``name``                  str         Name of the circuit that is executed by this job.
            ``id``                    int         Unique id of the job.
            ``status``                str         Execution status of the job:
                                                  e.g. 'NEW', 'COMPLETE', 'CANCELLED', 'RUNNING'.
            ``input``                 str         Url to get the assets of the job.
            ``backend``               str         Url to get the backend the job is executed on.
            ``backend_type``          str         Url to get the backend type of the backend
                                                  the job is executed on.
            ``results``               str         Url to get the results for the job.
            ``queued_at``             str         The date-time the job is queued at.
                                                  The format is 'yyyy-MM-ddTHH:mm:ss.SSSSSSZ' Zulu Time.
            ``number_of_shots``       int         Number of executions for this job.
            ``full_state_projection`` bool        Indicates if the backend uses full state projection
                                                  to determine the quantum state.
                                                  Used for optimizing simulations. For more information see:
                                                  https://www.quantum-inspire.com/kbase/optimization-of-simulations/
            ``user_data``             str         The user configuration data.
            ========================= =========== ==================================================================

        """
        try:
            job = self._action(['jobs', 'read'], params={'id': job_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Job with id {job_id} does not exist!') from err_msg
        return dict(job)

    def get_jobs(self) -> List[Dict[str, Any]]:
        """ Gets all the jobs registered to projects for the user the API is currently authenticated for.

        :return:
            The jobs with all of its properties.
            See :meth:`~.get_job` for a description of the job properties.
        """
        ret: List[Dict[str, Any]] = self._action(['jobs', 'list'])
        return ret

    def get_jobs_from_asset(self, asset_id: int) -> List[Dict[str, Any]]:
        """ Gets the jobs with its properties for an asset, given the asset id.

        :param asset_id: The asset identification number.

        :return:
            List of jobs with its properties for the asset with identification `asset_id`.
            An empty list is returned when the asset has no jobs.

        :raises ApiError: If the asset identified by `asset_id` does not exist.
        """
        try:
            jobs = self._action(['assets', 'jobs', 'list'], params={'id': asset_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Asset with id {asset_id} does not exist!') from err_msg
        ret: List[Dict[str, Any]] = jobs
        return ret

    def get_jobs_from_project(self, project_id: int) -> List[Dict[str, Any]]:
        """ Gets the jobs with its properties for a single project, given the project id.

        :param project_id: The project identification number.

        :return:
            List of jobs with its properties for the project with identification `project_id`.
            An empty list is returned when the project has no jobs.

        :raises ApiError: If the project identified by `project_id` does not exist.
        """
        try:
            jobs = self._action(['projects', 'jobs', 'list'], params={'id': project_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Project with id {project_id} does not exist!') from err_msg
        ret: List[Dict[str, Any]] = jobs
        return ret

    def delete_job(self, job_id: int) -> None:
        """ Deletes the job identified by `job_id`.

        Only jobs can be deleted that are registered for the user the API is currently authenticated for.

        :param job_id: The job identification number.

        :raises ApiError: If the job identified by `job_id` does not exist.
        """
        try:
            self._action(['jobs', 'delete'], params={'id': job_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Job with id {job_id} does not exist!') from err_msg

    def _create_job(self, name: str, asset: Dict[str, Any], number_of_shots: int,
                    backend_type: Dict[str, Any], full_state_projection: bool = False,
                    user_data: str = '') -> Dict[str, Any]:
        """ Creates a new job for executing cQASM code.

        This method is used by execute_qasm_async and indirectly by execute_qasm.

        :param name: The name for the job.
        :param asset: The asset with the cQASM code.
        :param number_of_shots: The number of executions before returning the result.
        :param backend_type: The backend type.
        :param full_state_projection: Used for optimizing simulations. For more information see:
            https://www.quantum-inspire.com/kbase/optimization-of-simulations/
        :param user_data: Data that the user wants to pass along with the job.

        :return:
            The properties describing the new job.
            See :meth:`~.get_job` for a description of the job properties.
        """
        full_state_projection = full_state_projection and not backend_type.get("is_hardware_backend", True)
        payload = {
            'status': 'NEW',
            'name': name,
            'input': asset['url'],
            'backend_type': backend_type['url'],
            'number_of_shots': number_of_shots,
            'full_state_projection': full_state_projection,
            'user_data': user_data
        }
        if not full_state_projection and self.enable_fsp_warning and not backend_type.get("is_hardware_backend", False):
            logger.warning("Your experiment can not be optimized and may take longer to execute, "
                           "see https://www.quantum-inspire.com/kbase/optimization-of-simulations/ for details.")
        try:
            return dict(self._action(['jobs', 'create'], params=payload))
        except (CoreAPIException, TypeError, ValueError) as err_msg:
            raise ApiError(f'Job with name {name} not created: {err_msg}') from err_msg

    #  results  #

    def list_results(self) -> None:
        """ Prints a list of results.

        Prints a list of all the results registered to the current user the API is authenticated for.
        For each result the identification number and creation date is printed.
        """
        results = self.get_results()
        for result in results:
            print(f'Result id: {result["id"]} (date: {result["created_at"]})')

    def get_result(self, result_id: int) -> Dict[str, Any]:
        """ Gets the results of the executed job, given the result_id.

        Using version 2.0 of the API, the results structure has changed to allow multiple measurement algorithms.
        Some items in the results structure (histogram, raw data, measurement mask, quantum states,
        measurement register) are defined as lists instead of single values. The lists hold the single values for each
        measurement block in the algorithm for backends that support multiple measurement. Backends that do not support
        multiple measurement always have a single measurement block and therefore return a single item in the
        results lists.
        For some items (raw data, measurement mask) in the results structure the type have changed to better express
        measured and not measured qubits. See :meth:`~.get_raw_data_from_result` for details.

        :param result_id: The result identification number.

        :raises ApiError: If the requested result does not exist.

        :return:
            The properties describing the result:

            ============================= ================ =============================================================
            Key                           Type             Description
            ============================= ================ =============================================================
            ``id``                        int              Unique id of the result.
            ``url``                       str              The url to get this result.
            ``job``                       str              The url to get the job that generated the result.
            ``created_at``                str              The date-time the result is created at.
                                                           The format is 'yyyy-MM-ddTHH:mm:ss.SSSSSSZ' Zulu Time.
            ``number_of_qubits``          int              Number of qubits in the circuit for this experiment.
            ``execution_time_in_seconds`` float            The execution time of the job.
            ``raw_text``                  str              Text string filled when an error occurred, else empty.
            ``raw_data_url``              str              Url to get the raw data of the result. The raw data exists of
                                                           a list of integer values depicting the state for each shot.
            ``histogram``                 list(dict)       The histograms as a list of dicts with tuples with state
                                                           (str) and its probability (float).
            ``histogram_url``             str              Url to get the histogram with probabilities. This results in
                                                           the dict as found in property ``histogram`` of result.
            ``measurement_mask``          list(list(0|1))  For each measurement block a list of 0 (not measured) or 1
                                                           (measured) values for all the qubits in the cQASM program.
            ``quantum_states_url``        str              Url to get a list of quantum states for each measurement
                                                           block.
            ``measurement_register_url``  str              Url to get a list of measurement registers for each
                                                           measurement block.
            ``calibration``               str              Url to get calibration information.
            ============================= ================ =============================================================
        """
        try:
            result = self._action(['results', 'read'], params={'id': result_id, })
        except ErrorMessage as err_msg:
            raise ApiError(f'Result with id {result_id} does not exist!') from err_msg
        return dict(result)

    def get_results(self) -> List[Dict[str, Any]]:
        """ Gets all the results registered for the user the API is currently authenticated for.

        :return:
            The results with all of its properties.
            See :meth:`~.get_result` for a description of the result properties.
        """
        ret: List[Dict[str, Any]] = self._action(['results', 'list'])
        return ret

    def get_result_from_job(self, job_id: int) -> Dict[str, Any]:
        """ Gets the result with its properties for a single job, given the job id.

        :param job_id: The job identification number.

        :return:
            The result with its properties for the job with identification `job_id`.
            See :meth:`~.get_result` for a description of the result properties.

        :raises ApiError: If the job identified by `job_id` does not exist.
        """
        try:
            result = self._action(['jobs', 'result', 'list'], params={'id': job_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Job with id {job_id} does not exist!') from err_msg
        return dict(result)

    def get_raw_data_from_result(self, result_id: int) -> List[List[Any]]:
        """ Gets the raw data from the result.

        Gets the raw data from the result of the executed job, given the result_id.
        The raw data consists of a list of measurements for each shot (job.number_of_shots).
        The measurements contain a list of data for each measurement in the job (len(measurement_mask)).
        The data consist of integer state values (0 or 1) for each measured qubit, else None (see measurement_mask).
        Actual type is: List[List[List[Optional[int]]]] with least significant qubit first.

        Example for :code:`"measurement_mask": [[0, 1], [1, 1]]` the raw_data for 6 shots is structured as follows:

        .. code-block::

            "raw_data": [
                [[None, 1], [0, 1]],
                [[None, 1], [1, 0]],
                [[None, 0], [1, 1]],
                [[None, 0], [1, 1]],
                [[None, 0], [0, 0]],
                [[None, 1], [0, 1]]
            ]

        In this example in the first measurement block only qubit[1] is measured, in the second measurement block
        qubit[0] and qubit[1] are measured.

        :param result_id: The identification number of the result.

        :raises ApiError: If the raw data url in result is invalid or the request for the raw data using the url failed.

        :return:
            The raw data as a list of structures. A list with an empty list is returned when raw data has no elements.
        """
        result = self.get_result(result_id)
        raw_data_url = str(result.get('raw_data_url'))
        try:
            token = raw_data_url.split('/')[-2]
        except IndexError as err_msg:
            raise ApiError(f'Invalid raw data url for result with id {result_id}!') from err_msg
        try:
            raw_data: List[List[Any]] = self._action(['results', 'raw-data', 'read'],
                                                     params={'id': result_id,
                                                             'token': token})
        except ErrorMessage as err_msg:
            raise ApiError(f'Raw data for result with id {result_id} does not exist!') from err_msg
        return raw_data

    def get_quantum_states_from_result(self, result_id: int) -> List[List[Any]]:
        """ Gets the quantum states for each measurement block from the result of the executed job, given the result_id.

        :param result_id: The identification number of the result.

        :raises ApiError: If the quantum states url in result is invalid or the request
            for the quantum states using the url failed.

        :return:
            A list of quantum states. The quantum states consists of a list of quantum state values and
            their corresponding probability.
            An empty list is returned when the backend does not return quantum states.
        """
        result = self.get_result(result_id)
        quantum_states_url = str(result.get('quantum_states_url'))
        try:
            token = quantum_states_url.split('/')[-2]
        except IndexError as err_msg:
            raise ApiError(f'Invalid quantum states url for result with id {result_id}!') from err_msg
        try:
            quantum_states: List[List[Any]] = self._action(['results', 'quantum-states', 'read'],
                                                           params={'id': result_id, 'token': token})
        except ErrorMessage as err_msg:
            raise ApiError(f'Quantum states for result with id {result_id} does not exist!') from err_msg
        return quantum_states

    def get_measurement_register_from_result(self, result_id: int) -> List[List[Any]]:
        """ Gets the measurement register for each measurement block from the result of the executed code,
        given the result_id.

        :param result_id: The identification number of the result.

        :raises ApiError: If the measurement register url in result is invalid
            or the request for the measurement register using the url failed.

        :return:
            A list of measurement registers. The measurement register consists of a list of measurement register values.
            An empty list is returned when there is no data.
        """
        result = self.get_result(result_id)
        measurement_register_url = str(result.get('measurement_register_url'))
        try:
            token = measurement_register_url.split('/')[-2]
        except IndexError as err_msg:
            raise ApiError(f'Invalid measurement register url for result with id {result_id}!') from err_msg
        try:
            measurement_register: List[List[Any]] = self._action(['results', 'measurement-register', 'read'],
                                                                 params={'id': result_id, 'token': token})
        except ErrorMessage as err_msg:
            raise ApiError(f'Measurement register for result with id {result_id} does not exist!') from err_msg
        return measurement_register

    def get_calibration_from_result(self, result_id: int) -> Optional[Any]:
        """ Gets the calibration information of the executed job, given the result_id.

        :param result_id: The identification number of the result.

        :raises ApiError: If the calibration url in result is invalid or the request
            for the calibration info using the url failed.

        :return:
            The calibration information from the backend. Calibration information may differ per backend type.
            None is returned when there is no calibration information (e.g. simulator backends).
        """
        calibration_info = None
        result = self.get_result(result_id)
        calibration_url = result.get('calibration')
        if calibration_url is not None:
            try:
                token = str(calibration_url).split('/')[-2]
            except IndexError as err_msg:
                raise ApiError(f'Invalid calibration url for result with id {result_id}!') from err_msg
            try:
                calibration_info = self._action(['calibration', 'read'], params={'id': token})
            except ErrorMessage as err_msg:
                raise ApiError(f'Calibration info for result with id {result_id} does not exist!') from err_msg
        return calibration_info

    #  assets  #

    def list_assets(self) -> None:
        """ Prints a list of the assets registered to the current user the API is authenticated for.

        For each asset the name, identification number and project identification number is printed."""
        assets = self.get_assets()
        for asset in assets:
            print(f'Asset name: {asset["name"]}, id: {asset["id"]}, (project_id: {asset["project_id"]})')

    def get_asset(self, asset_id: int) -> Dict[str, Any]:
        """ Gets the properties of the asset, given the asset_id.

        :param asset_id: The asset identification number.

        :raises ApiError: If the requested asset does not exist.

        :return:
            The properties describing the asset:

            ======================= =========== ==================================================================
            Key                     Type        Description
            ======================= =========== ==================================================================
            ``url``                 str         The url to get this asset.
            ``id``                  int         Unique id of this asset.
            ``name``                str         The name to get the asset.
            ``contentType``         str         The description of the content e.g. 'application/qasm' or
                                                'text/plain'.
            ``content``             str         The content itself.
                                                For example a cQASM program when linked to a job.
            ``project``             str         Url to get the project properties for which
                                                this asset was created.
            ``project_id``          int         The project id of the project for which this asset was created.
            ======================= =========== ==================================================================
        """
        try:
            asset = self._action(['assets', 'read'], params={'id': asset_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Asset with id {asset_id} does not exist!') from err_msg
        return dict(asset)

    def get_assets(self) -> List[Dict[str, Any]]:
        """ Gets all the assets registered for the user the API is currently authenticated for.

        :return:
            The assets with all of its properties.
            See :meth:`~.get_asset` for a description of the asset properties.
        """
        ret: List[Dict[str, Any]] = self._action(['assets', 'list'])
        return ret

    def get_assets_from_project(self, project_id: int) -> List[Dict[str, Any]]:
        """ Gets the assets with its properties for a single project, given the project id.

        :param project_id: The project identification number.

        :return:
            List of assets with its properties for the project with identification `project_id`.
            An empty list is returned when the project has no assets.

        :raises ApiError: If the project identified by `project_id` does not exist.
        """
        try:
            assets: List[Dict[str, Any]] = self._action(['projects', 'assets', 'list'], params={'id': project_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Project with id {project_id} does not exist!') from err_msg
        return assets

    def get_asset_from_job(self, job_id: int) -> Dict[str, Any]:
        """ Gets the asset data from the job, given the job_id.

        :param job_id: The identification number of the job.

        :raises ApiError: If the requested asset with identification from the job 'input' field does not exist.

        :return:
            The assets with all of its properties.
            See :meth:`~.get_asset` for a description of the asset properties.
        """
        job = self.get_job(job_id)
        asset_url = str(job.get('input'))
        try:
            asset_id = int(asset_url.split('/')[-2])
        except (ValueError, IndexError) as err_msg:
            raise ApiError(f'Invalid input url for job with id {job_id}!') from err_msg
        try:
            asset = self._action(['assets', 'read'], params={'id': asset_id})
        except ErrorMessage as err_msg:
            raise ApiError(f'Asset with id {asset_id} does not exist!') from err_msg
        return dict(asset)

    def _create_asset(self, name: str, project: Dict[str, Any], content: str) -> Dict[str, Any]:
        """ Create an asset.

        This method is used by execute_qasm_async to generate a new asset with a unique name to hold the
        content of the cQASM program for the project given. Assets are deleted when the project for which the asset
        was created is deleted.

        :param name: The name of the new asset.
        :param project: The project to which the asset is linked to.
        :param content: The cQASM code content.

        :return:
            The properties of the asset.
            See :meth:`~.get_asset` for a description of the asset properties.
        """
        payload = {
            'name': name,
            'contentType': 'application/qasm',
            'project': project['url'],
            'content': content,
        }
        return dict(self._action(['assets', 'create'], params=payload))

    #  other  #

    def wait_for_completed_job(self, quantum_inspire_job: QuantumInspireJob, collect_max_tries: Optional[int] = None,
                               sec_retry_delay: float = 0.5) -> Tuple[bool, str]:
        """ Wait for job completion.

        Delays the process and requests the job status. The waiting loop is broken when the job status is
        completed or cancelled, or when the maximum number of tries is set and has been reached.

        :param quantum_inspire_job: A job object.
        :param collect_max_tries: The maximum number of times the job status is checked. When set, the value should
            be > 0. When not set, the method waits until the job status is either completed or cancelled.
        :param sec_retry_delay: The time delay in between job status checks in seconds.

        :return:
            True if the job result could be collected else False in hte first part of the tuple.
            The latter part of the tuple contains an (error)message.
        """
        attempts = itertools.count() if collect_max_tries is None else range(collect_max_tries)
        for _ in attempts:
            time.sleep(sec_retry_delay)
            status = quantum_inspire_job.check_status()
            if status == 'COMPLETE':
                return True, 'Job completed.'
            if status == 'CANCELLED':
                return False, 'Failed getting result: job cancelled.'
        return False, 'Failed getting result: timeout reached.'

    @staticmethod
    def _generate_error_result(message: str) -> Dict[str, Any]:
        """Generate an error result object

        :param message: Reason for the failed job

        :return:
            Result object containing an empty histogram and an error message
        """
        result_obj = {
            'histogram': [],
            'raw_text': message
        }
        return result_obj

    def execute_qasm(self, qasm: str, backend_type: Optional[Union[Dict[str, Any], int, str]] = None,
                     number_of_shots: Optional[int] = None, collect_tries: Optional[int] = None,
                     default_number_of_shots: Optional[int] = None, identifier: Optional[str] = None,
                     full_state_projection: bool = False, user_data: str = '') -> Dict[str, Any]:
        """ With this method a cQASM program is executed, and the result is returned when the job is completed.

        The method :meth:`~.execute_qasm_async` is called which returns a QuantumInspireJob directly without waiting
        for the job to complete. After this call a waiting loop is started to wait for the job to finish and get
        the result.
        When no project name was given when the QuantumInspireAPI was created, the job is linked to a newly
        created temporary project in :meth:`~.execute_qasm_async`. When the job has finished running, this project is
        deleted.

        Depending on how busy the backend is, it takes some time to execute the job and
        returning the result. This method waits for the job to finish. The parameter collect_tries defines the
        maximum waiting time (collect_tries x 0.5 seconds). When the job takes longer to finish no results
        are returned. When set, the value of collect_tries must be > 0. When collect_tries is not set,
        the waiting time for completion is not limited.

        :param qasm: The cQASM code as string object.
        :param backend_type: The backend_type to execute the algorithm on.
        :param number_of_shots: Execution times of the algorithm before collecting the results.
        :param collect_tries: The number of times the status of the job is checked for completion before returning.
        :param default_number_of_shots: The default used number of shots for the project.
        :param identifier: The identifier to generate names for the project, asset and job when necessary.
        :param full_state_projection: Do not use full state projection with simulations when set to False (default).
        :param user_data: Data that the user wants to pass along with the job.

        :return:
            The results of the executed cQASM if successful else an error result if
            the results could not be collected within the given number of tries or the job failed.
            See :meth:`~.get_result` for a description of the result properties.
        """
        delete_project_afterwards = self.project_name is None
        quantum_inspire_job = None
        try:
            quantum_inspire_job = self.execute_qasm_async(qasm, backend_type=backend_type,
                                                          number_of_shots=number_of_shots,
                                                          default_number_of_shots=default_number_of_shots,
                                                          identifier=identifier,
                                                          full_state_projection=full_state_projection,
                                                          user_data=user_data)

            has_results, message = self.wait_for_completed_job(quantum_inspire_job, collect_tries)
            return dict(quantum_inspire_job.retrieve_results()) if has_results else \
                dict(self._generate_error_result(message))
        except (CoreAPIException, TypeError, ValueError, ApiError) as err_msg:
            message = f'Error raised while executing qasm: {err_msg}'
            return dict(self._generate_error_result(message))
        finally:
            if delete_project_afterwards and quantum_inspire_job is not None:
                project_identifier = quantum_inspire_job.get_project_identifier()
                self.delete_project(project_identifier)

    def execute_qasm_async(self, qasm: str, backend_type: Optional[Union[Dict[str, Any], int, str]] = None,
                           number_of_shots: Optional[int] = None, default_number_of_shots: Optional[int] = None,
                           identifier: Optional[str] = None, full_state_projection: bool = False,
                           project: Optional[Dict[str, Any]] = None, job_name: Optional[str] = None,
                           user_data: str = '') -> QuantumInspireJob:
        """With this method a cQASM program (job) is scheduled to be executed asynchronously.

        The method returns
        directly without waiting for the job to complete, as opposed to method :meth:`~.execute_qasm` which waits for
        the job to finish and returns the result.

        To execute a cQASM program a job is scheduled on a backend of type `backend type` as given by the
        parameter backend_type. Currently, there are 3 backend types available:

            1. QX single-node simulator (default for anonymous accounts)
            2. QX single-node simulator SurfSara (advanced account credentials needed)
            3. QX multi-node simulator SurfSara (advanced account credentials needed)

        When no `backend_type` is given, the default backend type currently being `QX single-node simulator`, is used.

        The job has to be linked with a project before it can be scheduled to execute.

        When a project name was supplied when the QuantumInspireAPI was created (see :meth:`~.__init__`), the job
        is linked to an existing project with this project name. When no project exists with this name a
        project with this name is created.

        When no project name was given when the QuantumInspireAPI was created, the job is linked to the project
        that is given as an argument `project`. When this `project` argument is empty, a project is created.
        First a project name is generated using the parameter `identifier` or when parameter `identifier` is
        empty an identifier is generated.

        When the project is created, it is created for the backend type and the default number of shots given.
        When the project already existed the values of the existing project are used for backend type and
        default number of shots.

        An asset with a unique id is created containing the cQASM program. This asset is linked to the project.

        When the project and the asset containing the program are known, a job is created with the name given by
        parameter `job_name`. When this parameter `job_name` is not filled, a job name is generated.

        The job that is created for running the program (contained in the asset) is linked to the project and will
        be executed `number_of_shots` times (as given by the parameter) before the results can be collected.

        The jobs' `user_data` is filled with the user data given as a parameter. This user data can be fetched and
        used later in the process.

        The default value of job parameter `full_state_projection` is set to False which
        means that the algorithm is treated as non-deterministic. As a result a deterministic algorithm may take
        longer to execute than strictly needed. When `full_state_projection` is set to True, a non-deterministic
        algorithm may give wrong results. Parameter `full_state_projection` is only used for simulations.

        Once the job is created, the method returns directly without waiting for the job to complete.
        The job is returned as a :class:`QuantumInspireJob`.
        This class encapsulates the job and contains methods the get
        the status of the job and retrieve the execution results when the job is completed.

        :param qasm: The qasm code as a string object.
        :param backend_type: The backend_type to execute the algorithm on.
        :param number_of_shots: Execution times of the algorithm before the results can be collected.
        :param default_number_of_shots: The default used number of shots for the project.
        :param identifier: The identifier used for generating names for the project, asset and job.
        :param full_state_projection: Do not use full state projection when set to False (default).
        :param project: The properties of an existing project, the asset and job are linked to. Only used
            when the project_name member of the api is empty.
        :param job_name: Name for the job that is to be executed, when None a job name is generated (see identifier)
        :param user_data: Data that the user wants to pass along with the job.

        :return:
            An encapsulated job object containing methods the get the status of the job and
            retrieve the execution results.
        """
        if not isinstance(backend_type, dict):
            if backend_type is None:
                backend_type = self.get_backend_type()
            elif isinstance(backend_type, int):
                backend_type = self.get_backend_type(int(backend_type))
            elif isinstance(backend_type, str):
                backend_type = self.get_backend_type(str(backend_type))

        if identifier is None:
            identifier = str(uuid.uuid1())

        if self.project_name is not None:
            project = next((project for project in self.get_projects()
                            if project['name'] == self.project_name), None)

        if project is None:
            if default_number_of_shots is None:
                default_number_of_shots = backend_type['default_number_of_shots']
            project_name = self.project_name if self.project_name else f'qi-sdk-project-{identifier}'
            project = self.create_project(project_name, default_number_of_shots, backend_type)

        if backend_type['url'] != project['backend_type']:
            logger.warning("The backend for which the project was created is different "
                           "from the backend type given: %s. The experiment is run on backend %s.",
                           backend_type['name'], backend_type['name'])

        qasm = qasm.lstrip()
        qasm = re.sub(r'[ \t]*\n[ \t]*', r'\n', qasm)
        asset_name = f'qi-sdk-asset-{identifier}'
        asset = self._create_asset(asset_name, project, qasm)

        if job_name is None:
            job_name = f'qi-sdk-job-{identifier}'
        if number_of_shots is None:
            number_of_shots = backend_type['default_number_of_shots']
        job = self._create_job(job_name, asset, number_of_shots, backend_type, user_data=user_data,
                               full_state_projection=full_state_projection)

        return QuantumInspireJob(self, job['id'])
