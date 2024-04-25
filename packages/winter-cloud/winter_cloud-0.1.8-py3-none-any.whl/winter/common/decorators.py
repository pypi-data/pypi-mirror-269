from sqlmodel import text


def select(sql_query: str):
    def decorator(method):
        async def wrapper(self, *args, **kwargs):
            raw_sql = text(sql_query)
            async with self.database():
                result = await self.database.session.execute(raw_sql, kwargs)
                return result.mappings().all()

        return wrapper

    return decorator
