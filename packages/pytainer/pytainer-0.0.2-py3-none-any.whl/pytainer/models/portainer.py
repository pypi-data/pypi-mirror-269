from typing import List, Optional, Union
from pydantic import BaseModel
from pytainer.models import gittypes


class AuthAuthenticatePayload(BaseModel):
    username: str
    password: str


class AuthAuthenticateResponse(BaseModel):
    jwt: str


class SystemInfoResponse(BaseModel):
    agents: int
    edgeAgents: int
    platform: str


class SystemBuildInfo(BaseModel):
    buildNumber: str
    goVersion: str
    imageTag: str
    nodejsVersion: str
    webpackVarsion: str
    yarnVersion: str


class SystemVersionResponse(BaseModel):
    latestVersion: str
    UpdateAvailable: bool
    build: SystemBuildInfo
    databaseVersion: str
    serverVersion: str


class AutoUpdateSettings(BaseModel):
    forcePullImage: bool
    forceUpdate: bool
    interval: int
    jobID: str
    webhook: str


class StackOption(BaseModel):
    prune: bool


class TeamResourceAccess(BaseModel):
    AccessLevel: int
    TeamId: int


class UserResourceAccess(BaseModel):
    AccessLevel: int
    UserId: int


class ResourceControl(BaseModel):
    AccessLevel: Optional[int] = None
    AdministratorsOnly: bool
    Id: int
    OwnerId: Optional[int] = None
    Public: bool
    ResourceId: str
    SubResourceIds: List[str]
    System: bool
    TeamAccesses: List[TeamResourceAccess]
    Type: int
    UserAccesses: List[UserResourceAccess]


class Pair(BaseModel):
    name: str
    value: str


class Stack(BaseModel):
    AdditionalFiles: Optional[List[str]]
    AutoUpdate: Optional[AutoUpdateSettings]
    EndpointId: int
    EntryPoint: Union[List[str], str]
    Env: List[Pair]
    Id: int
    Name: str
    Option: StackOption | None
    ResourceControl: ResourceControl | None
    Status: int
    SwarmId: str
    Type: int
    CreatedBy: Optional[str]
    CreationDate: Optional[int]
    FromAppTemplate: Optional[bool]
    GitConfig: Optional[gittypes.RepoConfig]
    IsComposeFormat: bool
    Namespace: str
    ProjectPath: str
    UpdateDate: int
    UpdatedBy: str


class UpdateSwarmStackPayload(BaseModel):
    env: List[Pair]
    prune: bool = False
    pullImage: bool = False
    stackFileContent: str


class StackFileResponse(BaseModel):
    StackFileContent: str
