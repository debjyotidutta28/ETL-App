from manager.models import Databases

def start_migrations():
    print("starting mgrations")

    dbs=[]
    databases = Databases.query.all()
    for database in databases:
        print(f"Attempt to connect to {database.name} from {database.db_type}")

        try:
            print(database.id, database.name)
            db_connection = connect_to_database(database)
            dbs.append({
                        "database_name": database.name,
                        "connection": db_connection
                        })
        except:
            print("error building connection to database")
            continue

    
    return dbs
        
def connect_to_database(db):
    if(db.type=="mongodb"):
        return connect_mongodb(db)
    
def connect_mongodb(db):
    from pymongo import MongoClient
    mongodb_connection_string = db.uri
    db_client = MongoClient(mongodb_connection_string)
    db_client.admin.command('ismaster')
