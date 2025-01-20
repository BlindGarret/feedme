from fastapi.datastructures import FormData


def patch_instance(instance, form_data: FormData):
    for key, value in form_data.items():
        if hasattr(instance, key):
            if instance.__dict__[key] != value:
                setattr(instance, key, value)
    return instance
