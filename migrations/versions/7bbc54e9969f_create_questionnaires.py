"""create questionnaires

Revision ID: 7bbc54e9969f
Revises: 77e220ed6498
Create Date: 2024-12-01 16:34:32.168628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bbc54e9969f'
down_revision = '77e220ed6498'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionnaires',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('label', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('value', sa.Integer(), nullable=False))
        batch_op.drop_column('option_text')
        batch_op.drop_column('option_value')

    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('label', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('questionnaire_id', sa.String(length=36), nullable=False))
        batch_op.create_foreign_key(None, 'questionnaires', ['questionnaire_id'], ['id'])
        batch_op.drop_column('question_type')
        batch_op.drop_column('question_text')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('question_text', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('question_type', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('questionnaire_id')
        batch_op.drop_column('label')

    with op.batch_alter_table('options', schema=None) as batch_op:
        batch_op.add_column(sa.Column('option_value', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('option_text', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
        batch_op.drop_column('value')
        batch_op.drop_column('label')

    op.drop_table('questionnaires')
    # ### end Alembic commands ###