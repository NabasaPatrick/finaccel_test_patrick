"""m_limit tabel created

Revision ID: 98accd7a236b
Revises: 89a722795a26
Create Date: 2023-02-17 05:09:29.961081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98accd7a236b'
down_revision = '89a722795a26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('m_limit',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('identity_id', sa.String(), nullable=True),
    sa.Column('createdat', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updatedat', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('m_limit')
    # ### end Alembic commands ###
