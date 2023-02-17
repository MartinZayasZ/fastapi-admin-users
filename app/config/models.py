from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    created_by = Column(Integer)
    updated_by = Column(Integer)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_by = Column(Integer)
    updated_by = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    users = relationship("User", back_populates="role")
    permission_role = relationship("PermissionRole", back_populates="role")

class PermissionRole(Base):
    __tablename__ = "permissions_roles"

    id = Column(Integer, primary_key=True, index=True)

    permission_id = Column(Integer, ForeignKey("permissions.id"))
    permission = relationship("Permission", back_populates="permission_role")

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="permission_role")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    action = Column(String)

    permission_role = relationship("PermissionRole", back_populates="permission")
