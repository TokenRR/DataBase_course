"""Drop

Revision ID: c6d219f055c1
Revises: ba09343fb2cf
Create Date: 2023-05-07 10:23:29.357777

"""

from alembic import op
import sqlalchemy as sa
import time


# revision identifiers, used by Alembic.
revision = 'c6d219f055c1'
down_revision = 'ba09343fb2cf'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('zno')
    print('Finish. Good luck')
    time.sleep(120)


def downgrade():
    pass
