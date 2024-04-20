import os
import requests
from urllib.parse import urlparse
from typing import List
from dektools.url import get_auth_url
from dektools.cfg import ObjectCfg
from dektools.file import read_chunked, sure_dir
from gitea import Gitea, Organization, Branch, Repository

cfg = ObjectCfg('dekcli/gitea')


def get_ins(url=None, token=None):
    return Gitea(url, token)


def create_org(ins: Gitea, name):
    user = ins.get_user()
    result = ins.requests_post(
        Gitea.CREATE_ORG % user.username,
        data={
            "repo_admin_change_team_access": True,
            "username": name,
            "visibility": "private",
        },
    )
    assert "id" in result
    return Organization.parse_response(ins, result)


def patch_org(ins: Gitea, name, data):
    ins.requests_patch(
        Organization.API_OBJECT.format(name=name),
        data=data,
    )


def get_orgs(ins):
    path = "/admin/orgs"
    results = ins.requests_get_paginated(path)
    return [Organization.parse_response(ins, result) for result in results]


def create_repo(ins: Gitea, org, name, branch_name):
    return ins.create_repo(org, name, autoInit=False, private=True, default_branch=branch_name)


def mirror_repo(ins: Gitea, org_name, repo_name, remote_repo):
    Repository.migrate_repo(
        ins,
        service=urlparse(remote_repo).netloc.split('.')[-2],
        mirror=True, private=False,
        clone_addr=remote_repo, repo_owner=org_name, repo_name=repo_name, mirror_interval='0'
    )


def patch_repo(ins: Gitea, org_name, repo_name, kwargs):
    args = {"owner": org_name, "name": repo_name}
    ins.requests_patch(Repository.API_OBJECT.format(**args), data=kwargs)


def get_branches(repo) -> List["Branch"]:
    results = repo.gitea.requests_get_paginated(
        Repository.REPO_BRANCHES % (repo.owner.username, repo.name)
    )
    return [Branch.parse_response(repo.gitea, result) for result in results]


def add_branch(repo, newname: str) -> "Branch":
    data = {"new_branch_name": newname}
    result = repo.gitea.requests_post(
        Repository.REPO_BRANCHES % (repo.owner.username, repo.name), data=data
    )
    return Branch.parse_response(repo.gitea, result)


def create_token(ins: Gitea, name, scopes):
    user = ins.get_user()
    result = ins.requests_post(
        '/users/%s/tokens' % user.username,
        data=dict(
            name=name,
            scopes=scopes
        )
    )
    return result['sha1']


def get_packages(ins: Gitea, org_name):
    results = ins.requests_get_paginated(
        '/packages/%s' % org_name
    )
    return results


packages_file_type = 'generic'


def get_file_url(ins: Gitea, org_name, project_name, version, file):
    user = ins.get_user()
    token = ins.headers["Authorization"].split(' ', 1)[1]
    url = f"{ins.url}/api/packages/{org_name}/{packages_file_type}/{project_name}/{version}/index{os.path.splitext(file)[-1]}"
    return get_auth_url(url, user.username, token)


def upload_file(ins: Gitea, org_name, project_name, version, file):
    OrgRepoSure(ins).get_org_repos(org_name)
    url = get_file_url(ins, org_name, project_name, version, file)
    requests.delete(url)
    requests.put(url, data=read_chunked(file))


def fetch_file(ins: Gitea, org_name, project_name, version, file):
    response = requests.get(get_file_url(ins, org_name, project_name, version, file), stream=True)
    sure_dir(os.path.dirname(file))
    with open(file, "wb") as f:
        for data in response.iter_content():
            f.write(data)


class OrgRepoSure:
    def __init__(self, ins: Gitea):
        self.ins = ins
        self.orgs = {x.name: x for x in get_orgs(self.ins)}
        self.orgs_repos = {}

    def get_org_repos(self, org_name):
        if org_name not in self.orgs:
            self.orgs[org_name] = create_org(self.ins, org_name)
        org = self.orgs[org_name]
        if org_name not in self.orgs_repos:
            self.orgs_repos[org_name] = {x.name: x for x in org.get_repositories()}
        org_repos = self.orgs_repos[org_name]
        return org, org_repos

    def get_or_create(self, org_name, repo_name, branch_name):
        org, org_repos = self.get_org_repos(org_name)
        if repo_name not in org_repos:
            org_repos[repo_name] = create_repo(self.ins, org, repo_name, branch_name)
        return org_repos[repo_name]

    def get_or_mirror(self, org_name, repo_name, remote_repo):
        org, org_repos = self.get_org_repos(org_name)
        if repo_name not in org_repos:
            org_repos[repo_name] = Repository.migrate_repo(
                self.ins,
                service=urlparse(remote_repo).netloc.split('.')[-2],
                mirror=True, private=False,
                clone_addr=remote_repo, repo_owner=org_name, repo_name=repo_name, mirror_interval='0'
            )
        return org_repos[repo_name]
