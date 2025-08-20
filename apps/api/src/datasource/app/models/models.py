from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.dialects.postgresql import UUID
import uuid


# 用户角色关联表
user_role_association = Table(
    'user_role_association',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)

# 角色权限关联表
role_permission_association = Table(
    'role_permission_association',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    """用户模型"""
    __tablename__ = "user"
    
    # 基础字段继承自 SQLAlchemyBaseUserTableUUID
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    department = Column(String(100))
    position = Column(String(100))
    avatar = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    roles = relationship("Role", secondary=user_role_association, back_populates="users")
    datasources = relationship("Datasource", back_populates="creator")


class Role(Base):
    """角色模型"""
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    users = relationship("User", secondary=user_role_association, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission_association, back_populates="roles")


class Permission(Base):
    """权限模型"""
    __tablename__ = "permission"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    resource = Column(String(50), nullable=False)  # 资源名称，如 datasources, users
    action = Column(String(50), nullable=False)    # 操作名称，如 read, write, delete
    description = Column(String(200))
    parent_id = Column(Integer, ForeignKey("permission.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    roles = relationship("Role", secondary=role_permission_association, back_populates="permissions")
    children = relationship("Permission", backref="parent", remote_side=[id])


class Datasource(Base):
    """数据源模型"""
    __tablename__ = "datasource"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    type = Column(String(50), nullable=False)  # mysql, postgresql, mongodb, etc.
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    database = Column(String(100))
    username = Column(String(100))
    password = Column(String(255))  # 加密存储
    connection_params = Column(Text)  # JSON格式的额外连接参数
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # 创建者
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    creator = relationship("User", back_populates="datasources")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_sync_at = Column(DateTime(timezone=True))
    
    # 连接状态
    connection_status = Column(String(20), default="unknown")  # connected, failed, unknown
    last_test_at = Column(DateTime(timezone=True))
