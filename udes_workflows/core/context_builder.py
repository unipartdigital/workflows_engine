__all__ = ("ContextBuilder",)


class ContextBuilder:
    def get_group_key(self):
        raise NotImplementedError()

    def group_objects(self, objects):
        for key, group in objects.groupby(self.get_group_key()):
            yield group

    def _build_context(self, group):
        raise NotImplementedError()

    def build_context(self, objects):
        for group in self.group_objects(objects):
            yield self._build_context(group)
