"""init

Revision ID: 0001_init
Revises:
Create Date: 2026-04-25
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'role') THEN
                CREATE TYPE role AS ENUM ('admin', 'user', 'guest');
            END IF;
        END
        $$;
        """
    )
    role_enum = sa.Enum('admin', 'user', 'guest', name='role', create_type=False)

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', role_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)

    op.create_table(
        'invites',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(64), nullable=False),
        sa.Column('role', role_enum, nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('created_by_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_invites_code', 'invites', ['code'], unique=True)

    op.create_table(
        'tracks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('artist', sa.String(255), nullable=True),
        sa.Column('album', sa.String(255), nullable=True),
        sa.Column('genre', sa.String(255), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('cover_path', sa.String(500), nullable=True),
        sa.Column('original_filename', sa.String(255), nullable=False),
        sa.Column('mime_type', sa.String(100), nullable=False),
        sa.Column('format', sa.String(20), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('source_type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_tracks_owner_id', 'tracks', ['owner_id'])

    op.create_table('playlists', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('title', sa.String(255), nullable=False), sa.Column('description', sa.Text(), nullable=True), sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_table('playlist_tracks', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('playlist_id', sa.Integer(), sa.ForeignKey('playlists.id'), nullable=False), sa.Column('track_id', sa.Integer(), sa.ForeignKey('tracks.id'), nullable=False), sa.Column('position', sa.Integer(), nullable=False))
    op.create_table('share_links', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('token', sa.String(64), nullable=False), sa.Column('target_type', sa.String(20), nullable=False), sa.Column('target_id', sa.Integer(), nullable=False), sa.Column('allow_stream', sa.Boolean(), nullable=False), sa.Column('allow_download', sa.Boolean(), nullable=False), sa.Column('expires_at', sa.DateTime(), nullable=True), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('is_active', sa.Boolean(), nullable=False))
    op.create_index('ix_share_links_token', 'share_links', ['token'], unique=True)
    op.create_table('friend_storages', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('title', sa.String(255), nullable=False), sa.Column('base_url', sa.String(255), nullable=False), sa.Column('access_token', sa.String(255), nullable=True), sa.Column('status', sa.String(20), nullable=False), sa.Column('last_ping_ms', sa.Float(), nullable=True), sa.Column('last_speed_mbps', sa.Float(), nullable=True), sa.Column('last_checked_at', sa.DateTime(), nullable=True), sa.Column('last_error', sa.Text(), nullable=True), sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_table('remote_tracks_cache', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('friend_storage_id', sa.Integer(), sa.ForeignKey('friend_storages.id'), nullable=False), sa.Column('remote_track_id', sa.Integer(), nullable=False), sa.Column('title', sa.String(255), nullable=False), sa.Column('artist', sa.String(255), nullable=True), sa.Column('album', sa.String(255), nullable=True), sa.Column('duration_seconds', sa.Integer(), nullable=True), sa.Column('format', sa.String(20), nullable=True), sa.Column('size_bytes', sa.Integer(), nullable=True), sa.Column('can_stream', sa.Boolean(), nullable=False), sa.Column('can_download', sa.Boolean(), nullable=False), sa.Column('cached_at', sa.DateTime(), nullable=False))
    op.create_table('download_history', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('track_id', sa.Integer(), nullable=True), sa.Column('remote_track_id', sa.Integer(), nullable=True), sa.Column('friend_storage_id', sa.Integer(), nullable=True), sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_table('play_history', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('track_id', sa.Integer(), nullable=True), sa.Column('remote_track_id', sa.Integer(), nullable=True), sa.Column('friend_storage_id', sa.Integer(), nullable=True), sa.Column('played_at', sa.DateTime(), nullable=False))
    op.create_table('sync_rooms', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('title', sa.String(255), nullable=False), sa.Column('current_track_id', sa.Integer(), nullable=True), sa.Column('current_remote_track_id', sa.Integer(), nullable=True), sa.Column('position_seconds', sa.Float(), nullable=False), sa.Column('is_playing', sa.Boolean(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_table('settings', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False), sa.Column('theme', sa.String(20), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.create_unique_constraint('uq_settings_user_id', 'settings', ['user_id'])


def downgrade() -> None:
    for table in ['settings', 'sync_rooms', 'play_history', 'download_history', 'remote_tracks_cache', 'friend_storages', 'share_links', 'playlist_tracks', 'playlists', 'tracks', 'invites', 'users']:
        op.drop_table(table)
    op.execute('DROP TYPE IF EXISTS role')
