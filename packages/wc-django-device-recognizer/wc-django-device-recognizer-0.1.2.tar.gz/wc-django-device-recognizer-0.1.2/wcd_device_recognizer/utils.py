from typing import Iterable, List, Sequence, Tuple, Type, TypeVar
from operator import attrgetter

from django.db import models


M = TypeVar('M', bound=models.Model)


def stringify_version(version: tuple) -> str:
    return '.'.join([str(v) for v in version])


def to_list(items: Iterable) -> list:
    if isinstance(items, list):
        return items

    return list(items)


def model_bulk_get_or_create(
    model: Type[M], items: Sequence[Tuple[dict, dict]],
    internal_id_name: str = '_internal_lookup_id',
) -> List[M]:
    if len(items) == 0:
        return []

    id_map = {i + 1: value for i, value in enumerate(items)}
    q = models.Q()
    whens = []
    getid = attrgetter(internal_id_name)

    for id, (filters, _) in id_map.items():
        condition = models.Q(**filters)
        q |= condition
        whens.append(models.When(condition, then=models.Value(id)))

    existing = list(
        model.objects
        .filter(q)
        .annotate(**{internal_id_name: models.Case(
            *whens, default=None, output_field=models.IntegerField(),
        )})
    )
    diff = list(id_map.keys() - {getid(x) for x in existing})

    if len(diff) == 0:
        return existing

    blanks = (
        model(**{**id_map[id][0], **id_map[id][1]})
        for id in diff
    )
    created = model.objects.bulk_create(blanks)

    for i, x in enumerate(created):
        setattr(x, internal_id_name, diff[i])

    return sorted(existing + created, key=getid)
