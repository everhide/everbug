from tests.stub.models import Entity


class DBRouter:

    def db_for_read(self, model):
        if model == Entity:
            return 'default'
        else:
            return 'alternate'
