from DB.DB import DB
import pandas

db = DB()
df = pandas.read_csv('books.csv', sep="|", low_memory=False)

print("Data loaded")

for j, i in df.iterrows():
    db.add_book(
        i["id"],
        i["url"],
        i["picture"],
        i["author"],
        i["name"],
        i["publisher"],
        i["series"],
        i["year"],
        i["ISBN"],
        i["description"],
        i["age"],
        i["lang"],
        i["litres_isbn"],
        i["genres_list"]
    )
