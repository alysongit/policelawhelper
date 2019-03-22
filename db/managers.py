# @Time    : 2018/8/1 12:03
# @Author  : Niyoufa
from bson import ObjectId
from mptt import managers


class TreeManager(managers.TreeManager):
    def gen_objectid(self, oid=None):
        if oid:
            ObjectId(oid)
            object_id = oid
        else:
            object_id = str(ObjectId())
        return object_id

    def create(self, **kwargs):
        id = kwargs.get("id")
        if not id:
            id = self.gen_objectid(kwargs.get("id"))

        kwargs.update(dict(
            id=id,
        ))
        return super(TreeManager, self).create(**kwargs)

    def tree(self, objs):
        tree = []
        for obj in objs:
            tree.append(obj.name)
            children = obj.children.all()
            if len(children) > 0:
                tree.append(self.tree(obj.children.all()))
        return tree

    def bulk_create(self, objs, batch_size=None):
        return super(TreeManager, self).bulk_create(objs, batch_size=batch_size)