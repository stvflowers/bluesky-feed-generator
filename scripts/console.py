
# Use these commands to check the database and troubleshoot


from peewee import SqliteDatabase
from playhouse.reflection import generate_models, print_model, print_table_sql


db = SqliteDatabase('feed_database.db')
models = generate_models(db)
list(models.items())

globals().update(models)

print_model(post)

for p in post.select().order_by(post.indexed_at.desc()).limit(5):
        print(p.cid, p.indexed_at)