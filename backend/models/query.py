from sqlalchemy.sql.schema import Table

from . import database


async def get_or_create(
    query_clause: str, query_values: dict, table: Table, insert_values: dict
):
    """取得或建立"""
    result = await database.fetch_one(query=query_clause, values=query_values)
    if result:
        # get
        return result

    query = table.insert()
    return await database.execute(query=query, values=insert_values)

