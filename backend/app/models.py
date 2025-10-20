from typing import Optional, List
from datetime import date
from sqlmodel import JSON, Column, SQLModel, Field, Relationship
class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    work_summary: Optional[str] = None
    portfolio: Optional[str] = None
    links: "Links" = Relationship(back_populates="profile")
    educations: List["Education"] = Relationship(back_populates="profile")
    skills: List["Skill"] = Relationship(back_populates="profile")
    projects: List["Project"] = Relationship(back_populates="profile")
    work_experiences: List["WorkExperience"] = Relationship(back_populates="profile")
class Links(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id", unique=True)
    github: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    codeforces: Optional[str] = None
    gfg: Optional[str] = None
    profile: Profile = Relationship(back_populates="links")
class Education(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    school: str
    degree: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    score: Optional[str] = None
    profile: Profile = Relationship(back_populates="educations")
class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    name: str
    level: Optional[int] = 1
    profile: Profile = Relationship(back_populates="skills")
class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    title: str
    description: Optional[str] = None
    links: Optional[str] = None
    profile: Profile = Relationship(back_populates="projects")
    skills: Optional[List[str]] = Field(default_factory=list, sa_column=Column(JSON))
class WorkExperience(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    company: str
    title: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    profile: Profile = Relationship(back_populates="work_experiences")
