from pydantic import BaseModel


class GitAuthentication(BaseModel):
    gitCredentialID: int
    password: str
    username: str


class RepoConfig(BaseModel):
    authentication: GitAuthentication
    configFilePath: str
    configHash: str
    referenceName: str
    tlsskipVerify: bool
    url: str
