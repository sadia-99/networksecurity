from pymongo import MongoClient
uri = "mongodb+srv://sadianaitkaoudjt_db_user:<db_password>@cluster0.3a1y21m.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)