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
    path: str ## path to the asset, usually a wheel file in the dist folder
    local_path: str = None ## path to the asset in the artifact folder


@dataclass
class LocalConnection(Connection):
    name: str
    config: IndexConfig
    built: bool = False

    @property
    def uri(self):
        return os.path.expanduser(self.config["uri"])

    def build_repo(self, force_build: False) -> str:
        """
        Build a local repository and return the output from the shell command
        """
        if self.built and not force_build:
            return "Already built"
        out = self.build()
        self.built = True
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
        asset.local_path = os.path.join(dest_folder, asset_name)
        return asset

    def get_releases(self):
        dist = os.path.join(self.uri, "dist")
        for f in glob.glob(f"{dist}/*.whl"):
            bn = os.path.basename(f)
            yield LocalReleaseAsset(name=bn, path=f)
