from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional
from apps.types import PyObjectId



from apps.utils import WithFormGen
@WithFormGen(method_name='form')
class Project(BaseModel):
    class TechnologyStack(BaseModel):
        class Database(str, Enum):
            POSTGRESQL = 'PostgreSQL'
            MYSQL = 'MySQL'
            MONGODB = 'MongoDB'


        class Library(str, Enum):
            FASTAPI = 'FastAPI'


        class Deployment(str, Enum):
            DOCKER = 'Docker'
            DOCKERCOMPOSE = 'Docker Compose'

        class Tool(str, Enum):
            PSQL = 'psql'

        class Other(str, Enum):
            ELASTICSEARCH = 'Elasticsearch'

        databases: List[Database] = Field(default_factory=list)
        libraries: List[Library] = Field(default_factory=list)
        deployment: List[Deployment] = Field(default_factory=list)
        tools: List[Tool] = Field(default_factory=list)
        other: List[Other] = Field(default_factory=list)

    class Interface(str, Enum):
        WEB = 'Web'
        CLI = 'CLI'
        API = 'API'
        LIBRARY = 'Library'

    class ProgrammingLanguage(str, Enum):
        PYTHON = 'Python'
        GOLANG = 'Golang'
        CXX = 'C++'
        C = 'C'
        ASSEMBLY = 'Assembly'
        WEBASSEMBLY = 'WebAssembly'
        SQL = 'SQL'

    class Tag(str, Enum):
        TOYPROJECT = 'Toy Project'
        WORKPROJECT = 'Work Project'

    class Status(str, Enum):
        IN_PROGRESS = 'In progress'
        COMPLETED = 'Completed'

    class MetaInfo(BaseModel):
        class TimestampInfo(BaseModel):
            started: int | None = None
            finished: int | None = None

        timestamps: TimestampInfo

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    interfaces: List[Interface] = Field(default_factory=list)
    programming_languages: List[ProgrammingLanguage] = Field(default_factory=list)
    technologies: TechnologyStack
    tags: List[Tag] = Field(default_factory=list)
    status: Status
    meta: MetaInfo

    @field_validator('programming_languages')
    @classmethod
    def is_programming_languages_valid(cls, v):
        assert len(v) >= 1, 'At least 1 programming language is required'
        return v

    def print_interfaces(self):
        return ', '.join(i.value for i in self.interfaces)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "TODO": "TODO",
            }
        },
    )
