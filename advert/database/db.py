import motor.motor_asyncio


DATABASE_URI = "mongodb://mongo:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
