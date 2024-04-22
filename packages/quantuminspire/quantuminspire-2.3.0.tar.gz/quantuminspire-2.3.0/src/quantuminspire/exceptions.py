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
Module exceptions
=================

"""


class QiskitBackendError(Exception):
    """ Exception for SDK errors related to the Qiskit backend."""


class ProjectQBackendError(Exception):
    """ Exception for SDK errors related to the ProjectQ backend."""


class AuthenticationError(Exception):
    """ Exception for SDK errors related to authentication."""


class ApiError(Exception):
    """ Exception for SDK errors related to the API functionality."""
