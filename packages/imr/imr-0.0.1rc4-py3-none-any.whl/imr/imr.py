"""Intelligent Model Registry (imr)"""
import configparser
import shutil
from collections.abc import MutableMapping
from pathlib import Path

from artifactory import ArtifactoryPath
from requests.auth import HTTPBasicAuth

default_local_path = Path.home() / ".imr"
default_file_name = "imr.conf"


def load_config(config_name: str) -> MutableMapping:
    """Load configuration"""
    return load_config_from_file(default_local_path / default_file_name, config_name)


def load_config_from_file(file_path: Path, config: str) -> MutableMapping:
    """Load configuration from file."""
    config_params = configparser.ConfigParser()
    if file_path.exists():
        config_params.read(file_path)
    else:
        raise FileProcessingError(str(file_path), "Configuration file does not exist.")
    if config not in config_params:
        raise FileProcessingError(str(file_path), "Configuration does not exist: " + config)
    return config_params[config]


class FileProcessingError(Exception):
    """File does not exists Error."""

    def __init__(self, filename: str, message: str):
        self.filename = filename
        self.message = message
        super().__init__(f"Error processing file '{filename}': {message}")


class IMRRemote:
    """Remote repository class."""

    def __init__(self, repo: str, user: str, password: str):
        self.repo = repo
        self.user = user
        self.password = password
        self.home = str(Path.home())

    def list(self) -> list:
        """List models from the remote repository."""
        path = ArtifactoryPath(self.repo, auth=(self.user, self.password), auth_type=HTTPBasicAuth)
        return [str(package).replace(self.repo + "/", "") for package in path.glob("*/*")]

    def push(self, directory: str, package: str, version: str = "latest") -> None:
        """Push a local model to the remote repository."""
        path = ArtifactoryPath(
            self.repo + "/" + package + "/" + version,
            auth=(self.user, self.password),
            auth_type=HTTPBasicAuth,
        )
        path.mkdir()
        shutil.make_archive("model", "zip", directory)
        path.deploy_file("model.zip")

    def pull(self, directory: str, package: str, version: str = "latest") -> None:
        """Pull a remote model to the local repository."""
        path = ArtifactoryPath(
            self.repo + "/" + package + "/" + version + "/model.zip",
            auth=(self.user, self.password),
            auth_type=HTTPBasicAuth,
        )
        file_path: Path = Path(directory) / package / version
        if not Path(file_path).exists():
            Path.mkdir(file_path, parents=True)
        with path.open() as fd, Path.open(file_path / "model.zip", "wb") as out:
            out.write(fd.read())
        shutil.unpack_archive(file_path / "model.zip", file_path / "model")

    def rm(self, package: str, version: str = "latest") -> None:
        """Remove a model from the remote repository."""
        artefact = self.repo + "/" + package
        if version is not None:
            artefact = self.repo + "/" + package + "/" + version
        path = ArtifactoryPath(artefact, auth=(self.user, self.password), auth_type=HTTPBasicAuth)
        if path.exists():
            path.unlink()

    def path(self, package: str, version: str = "latest") -> ArtifactoryPath:
        """Return the path to the model."""
        artefact = self.repo + "/" + package
        if version is not None:
            artefact += "/" + version
        return ArtifactoryPath(artefact, auth=(self.user, self.password), auth_type=HTTPBasicAuth)


class IMRLocal:
    """Local repository class."""

    repo: Path
    home: Path

    def __init__(self, repo: str | None = None):
        self.home = Path.home()
        if repo is None:
            self.repo = self.home / ".imr"
        else:
            self.repo = Path.expanduser(Path(repo))
        if not Path(self.repo).exists():
            Path(self.repo).mkdir(parents=True)

    def list(self) -> list[str]:
        """List local models.

        returns all the paths in the repository after main directory
        BASE/modela/version1
        BASE/modela/version2
        BASE/modelb/version3

        results in ["modela/version1", "modela/version2", "modelb/version3"]
        """
        return ["/".join(version.parts[-2:]) for version in self.repo.rglob("*/*/")]

    def push(self, directory: str, package: str, version: str = "latest") -> None:
        """Push a model in a directory to the local repository."""
        shutil.copytree(src=directory, dst=self.repo / package / version)

    def rm(self, package: str, version: str = "latest") -> None:
        """Remove a model from the local repository."""
        if version is None:
            shutil.rmtree(self.repo / package)
        else:
            shutil.rmtree(self.repo / package / version)

    def path(self, package: str, version: str = "latest") -> Path:
        """Return the path to the model."""
        path: Path = self.repo / package
        if version is not None:
            path = self.repo / package / version
        return path


def imr_from_config(config_name: str) -> IMRRemote | IMRLocal:
    """Create a repository based on the given configuration name."""
    return imr_from_file(default_local_path / default_file_name, config_name)


def imr_from_file(file_path: Path, config_name: str) -> IMRRemote | IMRLocal:
    """Create a repository based on the given configuration name."""
    repo_config = load_config_from_file(file_path, config_name)
    if "type" not in repo_config:
        raise FileProcessingError("imr.conf", "Repository type not specified.")
    if repo_config["type"] == "local":
        repo_path = repo_config["path"]
        return IMRLocal(repo_path)
    if repo_config["type"] == "remote":
        repo_path = repo_config["path"]
        user = repo_config["user"]
        password = repo_config["password"]
        return IMRRemote(repo_path, user, password)
    raise FileProcessingError("imr.conf", "Repository type not known: " + repo_config["type"])
