from models.role import RoleModel, ROLE_USER, ROLE_ADMIN, ROLE_SUPER_ADMIN
from database import get_db

DB = next(get_db())

roles = [ROLE_USER, ROLE_ADMIN, ROLE_SUPER_ADMIN]


def seed():
    for role in roles:
        db_role = RoleModel(name=role)
        DB.add(db_role)
        DB.commit()
