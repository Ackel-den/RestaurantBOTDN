from sqlalchemy import BigInteger, String, ForeignKey, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    description: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column(String(16))
    user_id: Mapped[BigInteger] = mapped_column(ForeignKey("users.id"))


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    dish: Mapped[int] = mapped_column(ForeignKey("dishes.id"))
    name: Mapped[str] = mapped_column(String(16))
    weight: Mapped[float] = mapped_column()
    measure: Mapped[str] = mapped_column(String(3))


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        statement = text(
            """
            INSERT INTO CATEGORIES VALUES 
            (1, 'Завтрак'),
            (2, 'Обед'),
            (3, 'Ужин'),
            (4, 'Десерт') ON CONFLICT DO NOTHING;
            """
        )

        await session.execute(statement)
        await session.commit()