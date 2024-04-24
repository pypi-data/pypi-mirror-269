import glob
import os
import shutil
import subprocess
from dataclasses import dataclass

from pi_conf import Config

from dpypi.connections.connection import Connection
from dpypi.wheel import Wheel


class IndexConfig(Config):
    name: str
    uri: str


@dataclass
class LocalReleaseAsset:
    name: str
    path: str

    @property
    def local_path(self):
        return self.path


@dataclass
class LocalConnection(Connection):
    name: str
    config: IndexConfig
    # def __init__(self, config: dict):
    #     self.config = config
    #     self.name = config["name"]
    #     self.uri = config["uri"]

    @property
    def uri(self):
        # return os.path.join(self.config["uri"], self.name)
        return self.config["uri"]

    def build_repo(self) -> str:
        """
        Build a local repository and return the output from the shell command
        """
        out = self.build()
        return out

    def get_repo(self, name: str):

        full_uri = os.path.join(self.uri, "dist", name)
        if os.path.exists(full_uri):
            return full_uri
        return self
        # return self.config["repos"].get(name)

    def list_release_assets(
        self,
    ) -> list:
        """
        Get all assets for all releases in a repository
        args:
            repo: Repository.Repository
        returns:
            list[LocalReleaseAsset]
        """
        assets = []
        for release in self.get_releases():
            assets.append(release)
        return assets

    def build(self) -> str:
        """Run `poetry export` to get content of requirements.txt as string"""

        subproc_out = subprocess.run(
            "poetry build", shell=True, cwd=self.uri, capture_output=True, encoding="utf-8"
        )

        if subproc_out.returncode != 0:
            raise RuntimeError("Unable to export requirements")

        return subproc_out.stdout

    def get_release_asset(
        self,
        repo: str,
        release: str,
        asset_name: str,
        dest_folder: str,
    ):
        print("repo", repo, release, asset_name, dest_folder)
        dist = os.path.join(self.uri, "dist")
        path = os.path.join(dist, asset_name)
        asset = LocalReleaseAsset(name=asset_name, path=path)
        if dest_folder:
            os.makedirs(dest_folder, exist_ok=True)
            shutil.copy(path, dest_folder)
        return asset

    def get_releases(self):
        dist = os.path.join(self.uri, "dist")
        for f in glob.glob(f"{dist}/*.whl"):
            bn = os.path.basename(f)
            yield LocalReleaseAsset(name=bn, path=f)
