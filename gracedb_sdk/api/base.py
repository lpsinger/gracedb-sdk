from os.path import join


class Resource:

    def __init__(self, parent=None):
        self.session = parent.session
        self.parent = parent

    @property
    def url(self):
        return join(self.parent.url, str(self.path))

    def create_or_update(self, key, **kwargs):
        if key is None:
            return self.session.post(self.url, **kwargs).json()
        else:
            self.session.put(join(self.url, str(key)), **kwargs)

    def create(self, **kwargs):
        return self.create_or_update(None, **kwargs)

    def update(self, key, **kwargs):
        return self.create_or_update(key, **kwargs)

    def get(self, **kwargs):
        return self.session.get(self.url, **kwargs).json()


class Deletable(Resource):

    def delete(self, key):
        self.session.delete(join(self.url, str(key)))


class HasChildResources(Resource):

    def __getitem__(self, key):
        return self.child_class(self, key)


class ChildResource(Resource):

    def __init__(self, parent, path):
        super().__init__(parent)
        self.path = path
