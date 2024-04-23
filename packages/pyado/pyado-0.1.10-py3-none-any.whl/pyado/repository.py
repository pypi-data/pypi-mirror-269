"""Module to interact with Azure DevOps repositories."""

from typing import Iterator
from typing import Literal
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from pydantic import NonNegativeInt

from pyado.api_call import ADOUrl
from pyado.api_call import ApiCall
from pyado.api_call import get_test_api_call
from pyado.project import ProjectInfo


RepositoryName: TypeAlias = str
BranchName: TypeAlias = str
RepositoryId: TypeAlias = UUID
CommitId: TypeAlias = str
TagName: TypeAlias = str
SshUrl: TypeAlias = str
VersionType: TypeAlias = Literal["branch", "commit", "tag"]


class RepositoryInfo(BaseModel):
    """Type to store work item details."""

    id: RepositoryId
    name: RepositoryName
    project: ProjectInfo
    default_branch: Optional[BranchName] = Field(alias="defaultBranch", default=None)
    size: NonNegativeInt
    remote_url: ADOUrl = Field(alias="remoteUrl")
    ssh_url: SshUrl = Field(alias="sshUrl")
    web_url: ADOUrl = Field(alias="webUrl")
    is_disabled: bool = Field(alias="isDisabled")
    is_in_maintenance: bool = Field(alias="isInMaintenance")


class _RepositoryInfoResults(BaseModel):
    """Type to read repository details results."""

    value: list[RepositoryInfo]


def iter_repository_details(project_api_call: ApiCall) -> Iterator[RepositoryInfo]:
    """Iterate over the repositories of the project."""
    response = project_api_call.get(
        "git",
        "repositories",
        version="7.0",
    )
    results = _RepositoryInfoResults.model_validate(response)
    yield from results.value


def get_repo_api_call(
    project_api_call: ApiCall, repository_id: RepositoryId
) -> ApiCall:
    """Get repository API call."""
    return project_api_call.build_call(
        "git",
        "repositories",
        repository_id,
    )


def read_file(
    repository_api_call: ApiCall,
    path: str,
    version: BranchName | CommitId | TagName,
    version_type: VersionType = "branch",
):
    # Version type should be determined from version (or type of the object)
    get_item_parameters = {
        "path": path,
        "versionDescriptor.versionType": version_type,
        "versionDescriptor.version": version,
    }
    response = repository_api_call.get_raw(
        "items", parameters=get_item_parameters, version="7.2-preview.1"
    )
    return response


def test() -> None:
    """Function to test the functions."""
    test_api_call, test_config = get_test_api_call()
    del test_config
    for repo in iter_repository_details(test_api_call):
        print(repo)
    test_repo_api_call = get_repo_api_call(test_api_call, test_config["repository_id"])
    print(
        read_file(
            test_repo_api_call,
            test_config["test_file_path"],
            test_config["test_file_branch"],
        )
    )


if __name__ == "__main__":
    test()
