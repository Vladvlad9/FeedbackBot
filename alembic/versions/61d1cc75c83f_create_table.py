"""create table

Revision ID: 61d1cc75c83f
Revises: 
Create Date: 2023-01-24 12:00:36.857163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61d1cc75c83f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('chat_id', sa.BigInteger(), nullable=False),
                    sa.Column('block', sa.Boolean(), nullable=False),
                    sa.Column('ban', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('bots_tg',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('bot_id', sa.BigInteger(), nullable=False),
                    sa.Column('bot_token', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('chats_bot',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('chat_id', sa.BigInteger(), nullable=False),
                    sa.Column('bot_id', sa.BigInteger(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('bots_tg')
    op.drop_table('chats_bot')
