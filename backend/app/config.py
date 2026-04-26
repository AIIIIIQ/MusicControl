from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'MusicControl'
    secret_key: str = 'change_me'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60 * 24

    database_url: str = 'postgresql+psycopg2://musiccontrol:musiccontrol@postgres:5432/musiccontrol'

    music_dir: str = '/storage/music'
    covers_dir: str = '/storage/covers'
    downloads_dir: str = '/storage/downloads'

    node_name: str = 'MusicControl Node'
    node_description: str = 'Personal distributed music storage node'
    node_access_token: str = 'dev_node_token'
    node_require_token: bool = False


settings = Settings()
