from __future__ import annotations

from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import sqlalchemy
from sqlalchemy.exc import NoResultFound
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import declarative_base

from easy_sqla.context import DBContext
from easy_sqla.db.operators import And
from easy_sqla.db.operators import Or
from easy_sqla.db.query import BaseQueryBuilder
from easy_sqla.db.selector import CompositePK
from easy_sqla.db.settings import DBSettings
from easy_sqla.logger import logger as logging
from easy_sqla.utils import _lookup_model_foreign_key, get_model_attrs
from easy_sqla.utils import get_primary_key


class Manager:

    @property
    def pks(self):
        """
        We'll assume that there is just one primary key column inside a table.
        """
        pk_attrs = get_primary_key(self.__class__)
        return {v: getattr(self, v) for v in pk_attrs}

    @classmethod
    def set_db_context(cls, context: DBContext):
        cls.db_context = context

    @classmethod
    def get_simple_column(cls):
        """
        Simple mapper that return field of the model without relationship
        :return:
        """
        return [col.key for col in inspect(cls).mapper.column_attrs]

    @classmethod
    def as_base_model(cls, settings: DBSettings):
        cls.set_db_context(DBContext(settings))
        return declarative_base(cls=cls)

    def as_json(self):
        """
        Convert primary field of the object to json
        :return: dict
        """
        result = {}
        [
            result.update({col: getattr(self, col)})
            for col in self.get_class().get_simple_column()
        ]

        return result

    @classmethod
    def create(cls, **values):
        """
        A helper to create an object given some value
        :param values:
        :return: The instance of the cls
        """
        logging.info(
            f"Adding object {cls} to db",
            extra={
                "data": values,
            },
        )
        values = cls.get_foreign_model_creation_data(values)
        obj = cls(**values)
        logging.info(f"{cls} is being add to the DB", extra={"objects": [str(obj)]})

        with cls.db_context:
            cls.db_context.session.add(obj)

            if cls.db_context.settings.get("auto_commit"):
                cls.db_context.session.commit()

            logging.info(f"{obj} added with success")

            return obj

    @classmethod
    def get_foreign_model_creation_data(cls, data: dict):
        """
        Detect in a creation payload, which field are for the creation for a related model
        Ex:
            class Child(Base):
                first_name = ...
            class Parent(Base):
                name = ...
                birth = ...
                child = Column(INTEGER, ForeignKey(Child.id), ....)
            Parent.create(name=..., birth=..., child={'first_name': 'Jon Doe'})
        Should save object as it is if the field is a JSONField
        """
        for field_name, field_value in data.items():
            remote_field_model = _lookup_model_foreign_key(
                getattr(cls, field_name, None)
            )
            if remote_field_model:
                logging.info(
                    f"Remote field detected: {remote_field_model.__name__}. "
                    f"Creating a new {remote_field_model.__name__} object"
                )
                if field_value is None:
                    continue

                if isinstance(field_value, dict):
                    objekt = remote_field_model.create(**field_value)

                elif isinstance(field_value, CompositePK):
                    objekt = remote_field_model.get_by_pks(**field_value)

                else:
                    try:
                        target_col = None
                        for col in get_model_attrs(remote_field_model).get(
                            "simple_attrs", []
                        ):
                            fk_target_col = list(getattr(cls, field_name).foreign_keys)[
                                0
                            ].column

                            if col.columns[0].key == fk_target_col.key:
                                target_col = col.columns[0]
                                break

                        if target_col is not None:
                            target_col_type = target_col.type
                            try:
                                casted_value = target_col_type.process_result_value(
                                    value=field_value,
                                    dialect=cls.db_context.session.engine.dialect,
                                )

                            except (TypeError, AttributeError):
                                casted_value = target_col_type.python_type(field_value)
                        else:
                            casted_value = field_value

                        objekt = remote_field_model.get_by_pks(casted_value)
                    except (IndexError, KeyError) as exception:
                        logging.error(
                            f"Unable to find remote keys in order to fetch {cls} instance"
                        )
                        logging.exception(exception)
                        raise exception

                if objekt:
                    if len(objekt.pks) > 1:
                        raise ValueError(
                            "Create object with relation to another model "
                            "which have multiple primary key is  not supported yet."
                        )

                    data.update({field_name: list(objekt.pks.values())[0]})

                else:
                    raise sqlalchemy.exc.NoResultFound(
                        f"No {remote_field_model} row found with {field_value}"
                    )

        return data

    @classmethod
    def create_multiple(cls, data_collections: Union[List[Dict], Tuple[Dict]]) -> None:
        """
        Add the same time, multiple instance of the current model
        :param data_collections:
        :return:
        """
        if data_collections:
            obj_collections = list(map(lambda data: cls(**data), data_collections))

            with cls.db_context:
                cls.db_context.session.bulk_save_objects(obj_collections)
        else:
            logging.info("No data to add")

    @classmethod
    def all(cls):
        return cls.db_context.session.query(cls).all()

    @classmethod
    def get_by_pks(cls, *args, **kwargs):
        """
        Used to get unique row by name:value or only by value
        """

        pks = get_primary_key(cls)
        undefined_pks = set(pks.keys()).difference(kwargs.keys())

        if len(pks) > 1:
            if undefined_pks:
                raise ValueError(
                    f"While using this method, you should specify all pks to be sure at 100% to return only "
                    f"one row. Not defined {list(undefined_pks)}"
                )
        else:
            # update the kwargs to set the value of the pk field
            kwargs = {**kwargs, **dict(zip(pks.keys(), args))}
        return cls.get(**kwargs)

    @classmethod
    def get(cls, **conditions):
        """
        Return a single object from the db.
        Be aware. You'd better use this one to fetch data by only the primary key in order to be sure
        that the object is unique in database. Otherwise, an error will be thrown back
        :param conditions: dict with condition
        :return:
        """
        data = cls.filter(**conditions)
        if data:
            if len(data) > 1:
                raise sqlalchemy.exc.MultipleResultsFound(
                    "The conditions provided has returned multiple result. It's not allowed",
                )

            logging.debug(f"Found : {data[0]}")
        else:
            raise NoResultFound(
                f"No object {cls} found with {str(conditions)}"
            )

        return data[0]

    @classmethod
    def _filter(cls, bool_clause=None, **conditions):
        """
        Fire the filtering of query.py in db
        :param operator: the operator used for filtering
        :param conditions: Clause expression
        :return: SQLAlchemy query.py object
        """

        if not bool_clause or not isinstance(bool_clause, (Or, And)):
            bool_clause = And(**conditions)

        query_build = BaseQueryBuilder(cls, bool_clause, cls.db_context.session)
        query = query_build.make_filter()

        return query

    @classmethod
    def filter(cls, bool_clause=And, **conditions):
        """
        Dummy wrapper for filtering. For now use the default session of SQLAlchemy.
        :param bool_clause: operator to use by default when multiple kwargs are passed
        :param conditions:
        :return:
        """
        data = cls._filter(bool_clause, **conditions).all()
        logging.debug(
            f"{len(data)} {str(cls)} retrieved from database.",
            extra={
                "data_retrieved": list(map(str, data)),
            },
        )
        return data

    def get_class(self):
        """
        Return the class of the calling model
        :return:
        """
        return self.__class__

    @classmethod
    def delete(cls, delete_strategy="fetch", **filters) -> None:
        """
        Delete the current object from the database
        :return: None
        """
        with cls.db_context:
            cls._filter(**filters).delete(synchronize_session=delete_strategy)

    @classmethod
    def update(cls, update_payload, filter_none=True, update_strategy = "fetch", **filters):
        """
        :param filter_none: Remove None from field_to_update if true
        :return:
        """
        if filter_none:
            logging.debug(
                f"Filtering None values in filter to get {cls} object",
            )
            update_payload = {
                k: v for k, v in update_payload.items() if v is not None
            }
        with cls.db_context:
            cls._filter(**filters).update(update_payload, synchronize_session=update_strategy)
            cls.db_context.session.flush()
