import motor.motor_asyncio


DATABASE_URI = "mongodb://127.0.0.1:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
