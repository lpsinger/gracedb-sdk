from .base import ChildResource, ResourceMap


class File(ChildResource):

    def get(self):
        return self.session.get(self.url, stream=True).raw


class Files(ResourceMap):

    path = 'files/'
    mapped_class = File
