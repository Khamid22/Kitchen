from typing import Optional, Union, Any, AsyncGenerator, List, Dict, Tuple
from asyncio import get_event_loop

from pymysql import err as mysql_errors
from contextlib import suppress

from aiomysql import Pool, create_pool
from aiomysql.cursors import DictCursor


class MySQLStorage:
    def __init__(self, database: str, host: str = 'localhost', port: int = 3306, user: str = 'root',
                 password: Optional[str] = None, create_pool: bool = True):

        self.pool: Optional[Pool] = None
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.database = database

        if create_pool:
            loop = get_event_loop()
            loop.run_until_complete(self.acquire_pool())
        super().__init__()

    def __del__(self):
        self.pool.close()

    async def acquire_pool(self):
        if isinstance(self.pool, Pool):
            with suppress(Exception):
                self.pool.close()

        self.pool = await create_pool(host=self.host, port=self.port, user=self.user,
                                      password=self.password, db=self.database)

    @staticmethod
    def _verify_args(args: Optional[Union[Tuple[Union[Any, Dict[str, Any]], ...], Any]]):
        if args is None:
            args = tuple()
        if not isinstance(args, (tuple, dict)):
            args = (args,)
        return args

    async def apply(self, query: str, args: Optional[Union[Tuple[Any, ...], Dict[str, Any], Any]] = None) -> int:
        args = self._verify_args(args)
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, args)
                    await conn.commit()
                    return True
                except mysql_errors.Error as e:
                    await conn.rollback()
                    return False

    async def select(self, query: str, args: Optional[Union[Tuple[Any, ...], Dict[str, Any], Any]] = None) -> \
            AsyncGenerator[Dict[str, Any], None]:
        args = self._verify_args(args)
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, args)
                    await conn.commit()
                    while True:
                        item = await cursor.fetchone()
                        if item:
                            yield item
                        else:
                            break
                except mysql_errors.Error:
                    pass

    async def get(self, query: str, args: Optional[Union[Tuple[Any, ...], Dict[str, Any], Any]] = None,
                  fetch_all: bool = False) -> Union[bool, List[Dict[str, Any]], Dict[str, Any]]:
        args = self._verify_args(args)
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, args)
                    await conn.commit()

                    if fetch_all:
                        return await cursor.fetchall()
                    else:
                        result = await cursor.fetchone()
                        return result if result else dict()
                except mysql_errors.Error as e:
                    return False

    async def check(self, query: str, args: Optional[Union[Tuple[Any, ...], Dict[str, Any], Any]] = None) -> int:
        args = self._verify_args(args)
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cursor:
                try:
                    await cursor.execute(query, args)
                    await conn.commit()

                    return cursor.rowcount
                except mysql_errors.Error:
                    return 0

    async def check_user(self, telegram_id):
        check = bool(await self.check("select telegram_id from users where telegram_id =%s", telegram_id))
        return check

    async def delete_user(self, telegram_id):
        await self.apply("delete from users where telegram_id = %s", telegram_id)

    async def user_data(self, telegram_id):
        user_data = await self.get('select * from users where telegram_id = %s', telegram_id)
        return user_data

    async def admin_data(self, admin_id):
        admin_data = await self.get('select * from admins where admin_id = %s', admin_id)
        return admin_data