"""empty message

Revision ID: b514bd128fb0
Revises: a55668af36e2
Create Date: 2023-04-11 14:39:42.465348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b514bd128fb0'
down_revision = 'a55668af36e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name='fk_posts_author_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dislikes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='fk_dislikes_post_id'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_dislikes_user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='fk_likes_post_id'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_likes_user_id'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))
        batch_op.drop_constraint('fk_profiles_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_profiles_user_id', 'user', ['user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_constraint('fk_profiles_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_profiles_user_id', 'user', ['user_id'], ['id'])
        batch_op.drop_column('last_seen')
        batch_op.drop_column('bio')

    op.drop_table('likes')
    op.drop_table('dislikes')
    op.drop_table('posts')
    # ### end Alembic commands ###
