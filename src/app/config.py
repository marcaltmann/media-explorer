from dataclasses import dataclass, field
import os
from pathlib import Path


from ._utils import get_env


@dataclass
class DatabaseSettings:
    ECHO: bool = field(default_factory=get_env("DATABASE_ECHO", False))
    """Enable SQLAlchemy engine logs."""
    URL: str = field(
        default_factory=get_env("DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")
    )
    """SQLAlchemy Database URL."""


@dataclass
class S3Settings:
    S3_ACCESS_KEY_ID: str = field(default_factory=get_env("S3_ACCESS_KEY_ID", ""))
    """The public key id."""
    S3_SECRET_ACCESS_KEY: str = field(
        default_factory=get_env("S3_SECRET_ACCESS_KEY", "")
    )
    """The secret key."""
    S3_ENDPOINT_URL: str = field(default_factory=get_env("S3_ENDPOINT_URL", ""))
    """Endpoint URL including region."""
    S3_REGION_NAME: str = field(default_factory=get_env("S3_REGION_NAME", ""))
    """Region name, e.g. eu-west-1"""
    S3_BUCKET_NAME: str = field(default_factory=get_env("S3_BUCKET_NAME", ""))
    """The bucket name."""


@dataclass
class Settings:
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    s3: S3Settings = field(default_factory=S3Settings)

    @classmethod
    def from_env(cls, dotenv_filename: str = ".env") -> Settings:
        env_file = Path(f"{os.curdir}/{dotenv_filename}")
        if env_file.is_file():
            from dotenv import load_dotenv

            print(
                f"[yellow]Loading environment configuration from {dotenv_filename}[/]"
            )

            load_dotenv(env_file, override=True)
        return Settings()
