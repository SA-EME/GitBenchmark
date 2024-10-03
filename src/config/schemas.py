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
    Files: List[Files]


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
    header: str
    Section: Dict[str, List[str]]


class Config(BaseModel):
    """
    Configuration object.
    """
    ConventionalCommits: ConventionalCommits
    SemanticVersioning: SemanticVersioning
    ChangeLog: ChangeLog
    GitBenchmark: GitBenchmark
