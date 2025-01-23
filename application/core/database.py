from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/applications_db"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database initialized successfully")
    except OperationalError as e:
        print(f"Failed to initialize the database: {e}")
        raise
