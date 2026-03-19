from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.database import Base

from app.db.code_embeddings import CodeEmbedding

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())




class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(String, nullable=True)

    github_url = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")


class AnalysisState(Base):
    __tablename__ = "analysis_states"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer)

    status = Column(String, default="running")  
    # values: running | paused | completed

    current_step = Column(Integer, default=0)

    state_data = Column(JSON)   
    # stores full agent state (repo_structure, api_endpoints, etc.)

    user_context = Column(JSON, default=[])  
    # stores user inputs during analysis