"""empty message

Revision ID: 2769ad3acc6d
Revises: 
Create Date: 2022-11-03 20:11:01.801002

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2769ad3acc6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('category',
                    sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
                    sa.Column('name', sa.String(length=45))
                    )
    op.create_table('location',
                    sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
                    sa.Column('country', sa.String(length=45)),
                    sa.Column('city', sa.String(length=45))
                    )
    op.create_table('user',
                    sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
                    sa.Column('firstName', sa.String(length=45)),
                    sa.Column('lastName', sa.String(length=45)),
                    sa.Column('email', sa.String(length=45)),
                    sa.Column('password', sa.String(length=45)),
                    sa.Column('phone', sa.String(length=45)),
                    sa.Column('userStatus', sa.Enum('regular', 'premium')),
                    sa.Column('idlocation', sa.Integer, sa.ForeignKey('location.id'))
                    )
    op.create_table('publicad',
                    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('title', mysql.VARCHAR(length=45), nullable=True),
                    sa.Column('id_category', mysql.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('status', mysql.ENUM('active', 'closed', 'confirmed'), nullable=True),
                    sa.Column('publishingDate', mysql.DATETIME(), nullable=True),
                    sa.Column('about', mysql.VARCHAR(length=45), nullable=True),
                    sa.Column('photoUrl', mysql.VARCHAR(length=45), nullable=True),
                    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['id_category'], ['category.id'], name='publicad_ibfk_1'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='publicad_ibfk_2'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_0900_ai_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
    op.create_table('localad',
                    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('title', mysql.VARCHAR(length=45), nullable=True),
                    sa.Column('id_category', mysql.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('status', mysql.ENUM('active', 'closed', 'confirmed'), nullable=True),
                    sa.Column('publishingDate', mysql.DATETIME(), nullable=True),
                    sa.Column('about', mysql.VARCHAR(length=45), nullable=True),
                    sa.Column('photoUrl', mysql.VARCHAR(length=45), nullable=True),
                    sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('location_id', mysql.INTEGER(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['id_category'], ['category.id'], name='localad_ibfk_1'),
                    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name='localad_ibfk_3'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='localad_ibfk_2'),
                    sa.PrimaryKeyConstraint('id'),
                    mysql_collate='utf8mb4_0900_ai_ci',
                    mysql_default_charset='utf8mb4',
                    mysql_engine='InnoDB'
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('user')
    op.drop_table('localad')
    op.drop_table('publicad')
    op.drop_table('category')
    op.drop_table('location')
