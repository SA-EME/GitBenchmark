"""
  Gitbenchmark

  (c) SAEME

  For the full copyright and license information, please view the LICENSE
  file that was distributed with this source code.
"""

from typing import List, Dict

from pydantic import BaseModel


class Files(BaseModel):
    """
    Files object.
    """
    path: str
    pattern: str


class GitBenchmark(BaseModel):
    """
    Git benchmark object.
    """
    branch: str
    commit_message: str
    tag: str


class ConventionalCommits(BaseModel):
    """
    Conventional commits object.
    """
    type: List[str]


class SemanticVersioning(BaseModel):
    """
    Semantic versioning object.
    """
    major: List[str]
    minor: List[str]
    patch: List[str]


class ChangeLog(BaseModel):
    """
    ChangeLog object.
    """
    enabled: bool
    header: str
    Section: Dict[str, List[str]]

class Scope(BaseModel):
    """
    Scope object.
    """
    enabled: bool

class Config(BaseModel):
    """
    Configuration object.
    """
    ConventionalCommits: ConventionalCommits
    SemanticVersioning: SemanticVersioning
    Scope: Scope
    ChangeLog: ChangeLog
    GitBenchmark: GitBenchmark

default_config = """
[Version]
version='0.0.0'

[Prerelease]
enabled="{prerelease}"

[GitBenchmark]
branch='release'
tag='v'
commit_message='upgrade: release v{version}'

[Scope]
enabled="False"

[InitialCommit]
message='chore: initial commit'

[ConventionalCommits]
enabled="{commit}"
type=['release', 'feat', 'fix', 'chore', 'doc', 'style', 'refractor', 'test', 'build', 'ci', 'perf', 'others']


[SemanticVersioning]
major=['!', 'release']
minor=['feat']
patch=['fix', 'chore', 'doc', 'style', 'refractor', 'test', 'build', 'ci', 'perf', 'others']


[ChangeLog]
enabled="{logging}"
header="# Change Log\\n\\nAll notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\\n\\n"


[ChangeLog.Section]
add=['feat']
change=['refractor', 'perf', 'chore', 'doc', 'style', 'test', 'build', 'ci']
fixed=['fix']
remove=['remove']
deprecate=['depracate']
security=['security']
"""