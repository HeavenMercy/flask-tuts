# SQL-Alchemy

- create a database
```py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# or

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
```

- create a model:
```py
from datetime import datetime

mymodel_foreign = db.Table('relation',
    db.Column('member1', db.Integer, db.ForeignKey('mymodel.id')),
    db.Column('member2', db.Integer, db.ForeignKey('foreign.id'))
)

class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) # for primary key

    string_field = db.Column(db.String(25), nullable=False)
    datetime_field = db.Column(db.DateTime, default=datetime.utcnow)

    foreign_id = db.Column(db.Integer, db.ForeignKey('foreign.id')) # for a many-to-one relationship

    foreign = db.relationship('foreign', backref='mymodel') # to have a collection of related 'foreign' in a many-to-one relationship
    foreign = db.relationship('foreign', secondary=mymodel_foreign, backref='mymodels') # to have a collection of related 'foreigns' in a many-to-many relationship

    def __repr__(self) -> str:
        return f'<MyModel {self.id}>'
```

- to create the database structure/file/...: `db.create_all() # in a python shell`

- CRUD:
```py
db.session.add(my_model) # add a model object in the database
db.session.add_all([my_model, another_model])

MyModel.query.count() # counts rows

# MyModel.query.get(id)
MyModel.query.get_or_404(id) # get a model by its id (or redirects to a 404 page)

my_model = MyModel.query.filter(MyModel.id == id).first() # get the first model object
MyModel.query.order_by(MyModel.datetime_field.desc()).all()

MyModel.query.filter(MyModel.id == id).delete() # delete model objects

db.session.commit() # apply changes
db.session.rollback() # revert changes
```
