from itertools import groupby

__all__ = ("ContextBuilder",)


class ContextBuilder:
    def get_group_key(self):
        return lambda x: x

    def group_objects(self, objects, sort=True):
        grouping_key = self.get_group_key()

        if sort:
            objects = sorted(objects, key=grouping_key)

        for key, group in groupby(objects, key=grouping_key):
            yield group

    def _build_context(self, group):
        raise NotImplementedError()

    def build_context(self, objects):
        for group in self.group_objects(objects):
            yield self._build_context(group)
