"""Database abstraction layer"""

from typing import List

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database import Worker, UserData, worker_table, roles_table


async def fetch_insert(engine, user: Worker) -> List[UserData]:
    """Splitable, ops are united in case of single session"""

    #get last q ad exec
    select_lasts_q = select(
        worker_table.c.name_surname_patronymic,
        worker_table.c.birth_date,
        roles_table.c.role_name
    ).join_from(worker_table, roles_table).order_by(
        desc(worker_table.c.updated_at))

    aio_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with aio_session() as session:
        res_last_joined = await session.execute(select_lasts_q)
        users_to_write = res_last_joined.all()[:5]

        session.add(user)

        await session.commit()

    return users_to_write
