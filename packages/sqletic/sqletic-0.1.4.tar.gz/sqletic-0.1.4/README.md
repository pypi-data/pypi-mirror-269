# SQLetic

SQLetic is an SQL database engine in pure python iterating over list acting as table indexed by there name in a dictionary.

```python
    statement = """
select concat('In ', cities.name, ' city, the spoken language is ', corresponding_countries.language, ' where ', citizens.name, ' live.')
from cities
     inner join countries as corresponding_countries
           on (cities.country=corresponding_countries.name)
     inner join citizens
           on (cities.name=citizens.city)
    """

    database = {"cities":({"name": "Prague", "country": "Czechia"},
                          {"name": "Cesky Krumlov", "country": "Czechia"},
                          {"name":"Paris", "country": "France"}),
                "countries":({"name": "Czechia", "language": "Czech"},
                             {"name": "France", "language": "French"}),
                "citizens":({"name": "Pablo Picasso", "city": "Paris"},
                            {"name": "Alfons Mucha", "city": "Prague"},
                            {"name": "Egon Schiele", "city": "Cesky Krumlov"})}
    engine = Engine(database)
    engine.execute(statement)
    
    for entry in engine:
        print(entry)
```
