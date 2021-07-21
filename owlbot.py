# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
from synthtool import gcp

common = gcp.CommonTemplates()

default_version = "v3"

for library in s.get_staging_dirs(default_version):
    # Resolve sphinx warning `Inline substitution_reference start-string without end-string`
    # Remove tables from docstring. Requested change upstream in cl/377766167 due to https://google.aip.dev/192#formatting.
    s.replace(
        [
            library / f"google/cloud/resourcemanager_{library.name}/services/folders/*client.py",
            library / f"google/cloud/resourcemanager_{library.name}/types/folders.py"
        ],
        "-------------------------[|]----------------------------------------",
        "-------------------------\|----------------------------------------"
    )
    s.replace(
        [
            library / f"google/cloud/resourcemanager_{library.name}/services/organizations/*client.py",
            library / f"google/cloud/resourcemanager_{library.name}/types/organizations.py"
        ],
        "------------------[|]--------------------------------------------",
        "------------------\|--------------------------------------------"
    )
    s.replace(
        [
            library / f"google/cloud/resourcemanager_{library.name}/services/projects/*client.py",
            library / f"google/cloud/resourcemanager_{library.name}/types/projects.py"
        ],
        "-------------------------[|]----------------------------------------------",
        "-------------------------\|----------------------------------------------"
    )
    s.replace(
        [
            library / f"google/cloud/resourcemanager_{library.name}/services/projects/*client.py",
            library / f"google/cloud/resourcemanager_{library.name}/types/projects.py"
        ],
        "------------------[|]-----------------------------------------------------",
        "------------------\|-----------------------------------------------------"
    )
    
    # Work around gapic generator bug https://github.com/googleapis/gapic-generator-python/issues/902
    s.replace(library / f"google/cloud/resourcemanager_{library.name}/types/folders.py",
                r""".
    Attributes:""",
                r""".\n
    Attributes:""",
    )

    s.move(library, excludes=["setup.py", "README.rst", "docs/index.rst"])

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=98, microgenerator=True)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)