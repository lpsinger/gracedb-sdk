from .base import HasChildResource, Resource


class File(Resource):

    def get(self):
        return self.session.get(self.url, stream=True).raw


class Files(HasChildResource):

    path = 'files/'
    child_class = File
