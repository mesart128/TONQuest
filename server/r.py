import asyncio
from database.initial_data import populate_database

asyncio.run(populate_database())