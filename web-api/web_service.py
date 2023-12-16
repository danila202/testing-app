from databases import Database
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncio
from models import LogCreated, EntryLog

DATABASE_URL="postgresql+asyncpg://danila:danila_python@database/db_web_api"

def get_database():
    database = Database(DATABASE_URL)
    return database

app = FastAPI()

@app.post('/api/data')
async def create_log(entry_log: LogCreated, db: Database = Depends(get_database)):
    parts_log = entry_log.log.split()
    ip, method, uri, status_code = parts_log
    query = EntryLog.__table__.insert().values(ip=ip, method=method, uri=uri, status_code=int(status_code))
    await db.execute(query)

@app.get('/api/data')
async def get_data_from_db(db: Database = Depends(get_database)):
    query = EntryLog.__table__.select()
    entries = await db.fetch_all(query)

    if entries:
        entry = entries[-1]
        return {
            "Id": entry.id,
            "created": entry.created,
            "log": {
                "ip": entry.ip,
                "method": entry.method,
                "uri": entry.uri,
                "status_code": entry.status_code
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)