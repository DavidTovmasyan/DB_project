"""add_index_to_person_name

Revision ID: 9e71130c13f4
Revises: c1678e40299a
Create Date: 2023-12-17 00:56:10.272555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e71130c13f4'
down_revision: Union[str, None] = 'c1678e40299a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Use the appropriate table name
table_name = "person"
column_name = "name"

def upgrade():
    op.create_index(op.f("ix_{}_{}".format(table_name, column_name)), table_name, [column_name])

def downgrade():
    op.drop_index(op.f("ix_{}_{}".format(table_name, column_name)), table_name)
