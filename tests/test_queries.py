from unittest import TestCase

from django.db import reset_queries

from everbug.utils.queries import wrap_queries

from tests.stub.models import AltEntity, Entity


def run_queries(multi_db=False, multi_query=False):

    def run(db_model=None, multi=False):
        list(db_model.objects.all())
        if multi:
            list(db_model.objects.all()[:5])

    reset_queries()
    run(Entity, multi_query)
    if multi_db:
        run(AltEntity, multi_query)


class TestQueries(TestCase):

    def test_without_queries(self):
        reset_queries()
        self.assertEqual(None, wrap_queries())

    def test_alias_single_db(self):
        run_queries()
        self.assertCountEqual(['default'], wrap_queries())

    def test_alias_multi_db(self):
        run_queries(multi_db=True)
        self.assertCountEqual(['default', 'alternate'], wrap_queries())

    def test_fields_single_db(self):
        run_queries()
        query = wrap_queries()['default'][0]
        self.assertCountEqual(['time', 'explain', 'sql'], query)

    def test_fields_multi_db(self):
        run_queries(multi_db=True)
        db_queries = wrap_queries()
        for query in (db_queries['default'], db_queries['alternate']):
            self.assertCountEqual(['time', 'explain', 'sql'], query[0])

    def test_fields_multiquery_single_db(self):
        run_queries(multi_query=True)
        queries = wrap_queries()['default']
        for query in queries:
            self.assertCountEqual(['time', 'explain', 'sql'], query)

    def test_fields_multiquery_multi_db(self):
        run_queries(multi_db=True, multi_query=True)
        db_queries = wrap_queries()
        for queries in (db_queries['default'], db_queries['alternate']):
            for query in queries:
                self.assertCountEqual(['time', 'explain', 'sql'], query)
