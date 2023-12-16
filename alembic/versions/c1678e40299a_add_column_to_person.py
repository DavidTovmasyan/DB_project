"""add_column_to_person

Revision ID: c1678e40299a
Revises: 
Create Date: 2023-12-17 00:51:06.884137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1678e40299a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Use the appropriate table name
table_name = "person"

# Define the new column
new_column = sa.Column("email", sa.String(length=255), nullable=True)

def upgrade():
    op.add_column(table_name, new_column)

def downgrade():
    op.drop_column(table_name, "email")
