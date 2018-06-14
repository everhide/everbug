from django.db import connections
from django.db.utils import OperationalError


def wrap_queries():
    """ Wraps queries with their explains
    For example: {alias: [list of queries with explains], ...}
    List of queries like: [{'time': ..., 'explain': ..., 'sql': ...}, ...]
    :return: (None or dict)
    """

    def query_explain(connection, raw_sql):
        if connection.vendor == 'sqlite':
            sql = "EXPLAIN QUERY PLAN %s" % raw_sql
        elif connection.vendor == 'postgresql':
            sql = "EXPLAIN ANALYZE %s" % raw_sql
        elif connection.vendor == 'oracle':
            sql = "EXPLAIN PLAN FOR %s" % raw_sql
        else:
            sql = "EXPLAIN %s" % raw_sql
        try:
            with connections[connection.alias].cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except OperationalError:
            return []

    active_connections = [c for c in connections.all() if c.queries]
    if not active_connections:
        return None

    queries = {connection.alias: [] for connection in active_connections}
    for connection in active_connections:
        for query in connection.queries:
            explain = {'explain': query_explain(connection, query['sql'])}
            queries[connection.alias].append(dict(query, **explain))
    return queries
