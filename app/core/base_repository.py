import abc

from app.utils.class_helpers import auto_repr


class BaseRepository(metaclass=abc.ABCMeta):

    @staticmethod
    def map_to_model(row, model_cls, many=False):
        return model_cls.from_row(row=row, many=many)

    __repr__ = auto_repr
