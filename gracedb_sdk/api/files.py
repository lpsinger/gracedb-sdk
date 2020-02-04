from .base import Resource, ResourceMapping


class File(Resource):

    def get(self):
        return self.session.get(self.url, stream=True).raw


class Files(ResourceMapping):

    path = 'files/'
    mapped_class = File
