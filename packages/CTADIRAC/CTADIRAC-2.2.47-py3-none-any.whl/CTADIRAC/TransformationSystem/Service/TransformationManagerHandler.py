from DIRAC.TransformationSystem.Service.TransformationManagerHandler import (
    TransformationManagerHandler as TManagerBase,
)


class TransformationManagerHandlerMixin:
    types_get_tasks_by_file_status = [int, str]

    @classmethod
    def export_get_tasks_by_file_status(self, trans_id, file_status):
        return self.transformationDB.get_tasks_by_file_status(trans_id, file_status)


class TransformationManagerHandler(TransformationManagerHandlerMixin, TManagerBase):
    pass
