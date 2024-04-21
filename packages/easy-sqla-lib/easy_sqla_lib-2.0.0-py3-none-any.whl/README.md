# Description

Easy-sqla-lib is a Python library intended to make beautiful SQLAlchemy query syntax.

SQLAlchemy is an awesome and powerful ORM which mades interaction with database very painless. However powerful, sometime mean complex to use.
That's why the plugin has been built.

It add extra capabilities to sqla Base model in order to make query effortlessly more simple and readable.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install easy-sqla-lib
```

## Usage
### 1. Setup 

setup.py
```python
from easy_sqla.db.settings import DBSettings
from easy_sqla.db.settings import DriverEnum
from easy_sqla.manager import Manager


db_settings = DBSettings(
    driver=DriverEnum.POSTGRESQL,
    host="your_host",
    password="password",
    port="5432",
    username="user",
    name="my_db",
    auto_commit=True  # By default True

)

# Or if you want sqlite database
db_settings = DBSettings(
    driver=DriverEnum.SQLITE,
    sqlite_db_path="my/path/db.sqlite3"

)

```

Now we're going to create all of ours model from the base_model

### 2. Defining models 
models.py
```python
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from tests.base_model import base_model


class Item(base_model):
    __tablename__ = "item"
    item_id = Column(Integer, primary_key=True)
    content = Column(String)

    file = relationship("File")


class File(base_model):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    item = Column(ForeignKey(Item.item_id))

    user = relationship("User")


class User(base_model):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    last_login = Column(Datetime)
    description = Column(String(255))
    file = Column(ForeignKey(File.id))

    def __repr__(self):
        return f"User(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

```
Note that, models above are nested by only ForeignKey. It's only for demonstration purposes
But the lib will work on relation as well.

### 3. - Make search query
#### 3.1 Simple filter
service.py
```python
from models import User


# Get all user
User.all()

# Get user when id is greater than 10

User.filter(id__gt=10)

# Filter by some word in the description
User.filter(description__contains="my word")

# Get users which connected between two datetime
User.filter(last_login__between=["yyyy/MM/dd", "yyyy/MM/dd",])

# You can also search through a relationship 
# Get all user who have a file which path start by "/var/www"
User.filter(file__path__startswith="/var/www")

# No matter the depth of the relationships, you can go through
User.filter(file__item__content__contains="my_tag")

```
**N.B:** You can use almost all operator available originally by sqlalchemy. Complete list below

Sometime you would want to add more clause into your query with and/or term. The right is there for that

#### 3.1  Nested filter
```python
# When you want only use and, you don't need any extra. You build your query in kwargs

User.filter(my_field="value", my_another_field="value2", ...)

# If you want use or
from easy_sqla.db.operator import Or

User.filter(Or(my_field="value", my_field2="value2"))
# will produce following sql query: select * ...... where my_field='value' or my_field2='value2'

```

### 4. Creating object 
### 4.1 Simple object
You can create object by calling create. It take a kwargs that correspond to the defined attrs on the model

```python

User.create(first_name="hello", last_name="world", ...)
```

### 4.1 Object with relation
You can create object that has reference to another model by just passing to foreign_key attr, the value of his primary_key
```python

User.create(first_name="hello", last_name="world", file=1)

# It support also composite primary keys. You need to import CompositePK from db.selector module
from easy_sqla.db.selector import CompositePK
User.create(..., file=CompositePK(pk_1="...", pk_2="..."))
```
Behind the scene, easy_sqla will construct the query to do so.
But we're not done yet. Sometime you may want to create the related object along with the current.
You can achieve that by passing a dict to the foreign_key

```python

User.create(
    first_name="hello", 
    last_name="world", 
    file={"content": "..."}
)
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
