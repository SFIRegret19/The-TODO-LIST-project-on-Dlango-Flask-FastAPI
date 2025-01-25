"""Add User table

Revision ID: c0bcf4568653
Revises: a14c3005d871
Create Date: 2025-01-25 23:22:22.860812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0bcf4568653'
down_revision: Union[str, None] = 'a14c3005d871'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаем временную таблицу с правильной структурой
    op.create_table(
        "users_tmp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # Копируем данные из старой таблицы
    op.execute("INSERT INTO users_tmp (id, username, created_at) SELECT id, username, created_at FROM users")

    # Удаляем старую таблицу
    op.drop_table("users")

    # Переименовываем временную таблицу в оригинальное название
    op.rename_table("users_tmp", "users")
    # ### end Alembic commands ###


def downgrade():
    # Восстановление обратной миграции
    op.create_table(
        "users_tmp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),  # Без ограничения NOT NULL
    )

    # Копируем данные обратно
    op.execute("INSERT INTO users_tmp (id, username, created_at) SELECT id, username, created_at FROM users")

    # Удаляем измененную таблицу
    op.drop_table("users")

    # Переименовываем временную таблицу в оригинальное название
    op.rename_table("users_tmp", "users")
    # ### end Alembic commands ###
