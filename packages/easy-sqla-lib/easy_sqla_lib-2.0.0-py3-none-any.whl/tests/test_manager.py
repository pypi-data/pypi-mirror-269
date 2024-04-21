from __future__ import annotations

import unittest
from unittest import TestCase

import pytest
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from tests.models import File, Email, House
from tests.models import Item
from tests.models import User


class TestManager(TestCase):

    def test_create_simple_object(self):
        create_payload = {"first_name": "soumaila", "last_name": "kouriba"}
        user = User.create(**create_payload)
        self.assertTrue(user.pks)

    def test_create_nested_object(self):
        create_payload = {
            "first_name": "soumaila",
            "last_name": "kouriba",
            "file": {"path": "/c/mnt", "item": {"content": "a content"}},
        }

        user = User.create(**create_payload)
        assert File.all()
        assert Item.all()
        assert user.file
        self.assertEqual(File.get(id=user.file).pks.get("id"), user.file)

    def test_get(self):
        self.assertTrue(isinstance(User.get(id=1), User))

    def test_it_raise_not_found_exception(self):
        with self.assertRaises(NoResultFound):
            User.get(id=-1)

    def test_it_raise_multiple_row_found_exception(self):
        with self.assertRaises(MultipleResultsFound):
            User.get(first_name="soumaila")

    def test_create_nested_with_foreign_key(self):
        assert User.create(first_name="tester", last_name="testit", file="1")

    def test_get_by_pks(self):
        user = User.create(first_name="tester", last_name="hello")
        assert User.get_by_pks(id=user.pks.get("id"))

    def test_get_by_pks_multiple(self):
        Email.create(address="test@exemple.fr", just_field="hel", user_id=1)
        assert Email.get_by_pks(address="test@exemple.fr", just_field="hel")

    def test_get_by_pks_one_of_multiple(self):
        Email.create(address="tester123@exemple.fr", just_field="testtest", user_id=1)

        with pytest.raises(ValueError):
            assert Email.get_by_pks(address="tester123@exemple.fr")

    def test_operator_name_dont_collide_with_dunder_method(self):
        assert (
            House.filter(name="Hello") == []
        )  # because __name__  exists in every object

    def tests_get_multiple_pk(self):
        Email.create(
            address="anothertester123@exemple.fr", just_field="another_text", user_id=1
        )
        assert (
            len(
                Email.get_by_pks(
                    address="anothertester123@exemple.fr", just_field="another_text"
                ).pks
            )
            > 1
        )

    def test_update_objects(self):
        user = User.create(first_name="tester", last_name="hello")
        user.update(dict(first_name="soumaila"))
        assert user.first_name == "soumaila"

    def test_delete_objects(self):
        User.create(first_name="tester", last_name="hello")
        User.create(first_name="tester-12", last_name="hello")
        User.delete(last_name="hello")
        assert User.filter(last_name="hello") == []


class TestQueryWithJoin(unittest.TestCase):
    def test_query_with_self_join(self):
        User.create(
            first_name="silver",
            last_name="rayley",
            parent_id={"id": 2000, "first_name": "roger", "last_name": "Gold D."},
        )

        User.create(first_name="Gabban", last_name="Copper", parent_id=2000)
        User.create(first_name="Shanks", last_name="fearland", parent_id=2000)

        # Get roger's children
        self.assertEqual(
            User.filter(child__parent__parent_id__first_name="roger"),
            User.get(first_name="roger").child,
        )

