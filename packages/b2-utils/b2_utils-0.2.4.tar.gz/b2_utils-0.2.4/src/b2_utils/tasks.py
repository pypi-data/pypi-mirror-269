import celery as _celery
from django.apps import apps as _apps

__all__ = [
    "TaskModel",
]


class TaskModel(_celery.Task):
    """Custom Celery task base class with support for object queries.

    This base class extends Celery's `Task` class and provides additional functionality for working with object queries.
    It allows you to define and pass object queries as part of the task's input arguments. These queries are used to
    retrieve objects and modify the task's behavior. `related_manager` is not required and it uses `objects` by default.

    Example::

        # Create a custom Celery task using TaskModel as the base class
        @app.task(bind=True, base=TaskModel)
        def my_custom_task(self, myobject: MyModel, **kwargs):
            pass

        # Call the task with object queries
        my_custom_task.apply_async(kwargs={
            "objects": {
                "myobject": {
                    "model": ("myapp", "MyModel"),
                    "related_manager": "available_objects",
                    "query": {
                        "filter": {
                            "kwargs": {
                                "field1__gte": 10,
                                "field2__icontains": "example",
                            },
                        },
                    },
                },
            },
        }
    """

    @staticmethod
    def _build_query(related_manager, query_dict: dict):
        queryset = related_manager.all()
        for method in query_dict:
            _args = query_dict[method].get("args", [])
            _kwargs = query_dict[method].get("kwargs", {})
            queryset = getattr(queryset, method)(*_args, **_kwargs)

        return queryset

    def before_start(self, task_id, args, kwargs):
        if objects := self.request.kwargs.pop("objects", None):
            self.request.kwargs.update(
                {
                    obj: self._build_query(
                        getattr(
                            _apps.get_model(*attrs["model"]),
                            attrs.get("related_manager", "objects"),
                        ),
                        attrs["query"],
                    )
                    for obj, attrs in objects.items()
                },
            )

        return super().before_start(task_id, args, kwargs)
