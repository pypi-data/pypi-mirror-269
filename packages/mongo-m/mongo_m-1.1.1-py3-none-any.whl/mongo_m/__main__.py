import sys, asyncio
from dotenv import load_dotenv
from pathlib import Path
from .core import create_file_ini, get_config
from .repository.collections.models import Query
from .services.migration import (
    FileMigration, get_collections, connect_to_mongo, get_database,
    add_fields, delete_fields
)

load_dotenv()
PATH = Path(__file__).parent.resolve()


async def update_migration(client):
    collections_migration = FileMigration.get_migration()
    db = get_database(client)
    for collection in get_collections(client):
        if collection.name in collections_migration:
            fields = set(collections_migration[collection.name].keys())
            #Симметрическая разность множеств
            disjunctive = fields ^ collection.fields
            if "_id" in disjunctive:
                disjunctive.remove("_id")
            delete = Query()
            add = Query()
            for field in disjunctive:
                if field in fields:
                    add.query.append({field: {"$exists": False}})
                    add.fields[field] = collections_migration[collection.name][field]
                    add.empty = False
                if field not in fields and collection.fields:
                    delete.query.append({field: {"$exists": True}})
                    delete.fields[field] = ""
                    delete.empty = False
            add_fields(db, collection.name, add)
            delete_fields(db, collection.name, delete)


async def create_migration():
    config = get_config()
    module_path = config.get("MONGO", "module_path")
    migration_file = await FileMigration.make_migration(module_path)
    FileMigration.update_migration_file(migration_file)


async def main():
    FileMigration.create_migration_catalog()
    params = tuple(sys.argv[1:])
    # module_path = "app/src/app/schemes"
    # module_path = "utils/schemas/db_schemas_q_service"
    client = None
    try:
        if params[0] == "--create-migration":
            await create_migration()
        elif params[0] == "--update-migration":
            client = connect_to_mongo()
            await update_migration(client)
        elif params[0] == "--init":
            create_file_ini()
    except Exception as e:
        print(e)
    finally:
        if client != None:
            client.close()
    # for collection in db_collections:
    #     if collection.name == "text_queue":
    #         for field in collection.fields:
    #             print(collection.name, field.name, field.type)
    # find_collection = list(filter(lambda x: x.name in {"customer_request"}, db_collections))
    # query = {
    #     "$or": [{field.name: {"$exists": False}} for field in find_collection[0].fields]
    # }
    # set_field = {field.name for field in find_collection[0].fields}
    # get_collection = db.get_collection("customer_request").find(query)
    # for item in get_collection:
    #     fields = set_field ^ set(item.keys())
    #     update_fields = {"$set": {field: None for field in fields}}
    #     db.get_collection("customer_request").update_many(
    #         query, update_fields
    #     )

if __name__ == "__main__":
    asyncio.run(main())