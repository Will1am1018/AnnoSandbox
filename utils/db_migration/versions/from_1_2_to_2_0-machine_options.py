


"""machine options

Revision ID: cd31654d187
Revises: 1583656cb935
Create Date: 2015-12-16 11:07:59.948819

"""

# revision identifiers, used by Alembic.
revision = "cd31654d187"
down_revision = "1583656cb935"

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column("machines", sa.Column("options", sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column("machines", "options")
