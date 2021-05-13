from functools import partial
from operator import attrgetter

from yaml.parser import ParserError

from . import conversion as conv
from .generators import DataGenerator


def parse_file(reader, writer, args):
    idx = 1

    for row in reader:
        if idx == 1:
            generator, new_values = get_line_generator(row, args.config, args.generic)
        else:
            try:
                new_values = generator(row)
            except Exception as e:
                raise ParserError(
                    f"Cannot generate a new line for the line: {row}.\r\nError: {e}"
                )
        writer(new_values)

        if args.head and idx > args.head:
            break
        idx += 1


def get_line_generator(field_names, config, generic):
    config_fields = config and config.get("fields", {}) or {}
    fields = [Field(name, config_fields.get(name), generic) for name in field_names]
    values = [field.dest_name for field in fields if field.omit is False]
    return Generator(fields), values


class Generator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, values):
        return [
            field.get_value(value)
            for field, value in zip(self.fields, values)
            if field.omit is False
        ]

    def __repr__(self):
        return f"Generator({', '.join(repr(f) for f in self.fields)})"


class Field:
    def __init__(self, name, config=None, generic=None):
        self.name = name
        self.dest_name = name
        self.conversions = []
        self.generator = None
        self._parse_config(config, generic)

    def __repr__(self):
        return f"Field({self.__dict__})"

    def _parse_config(self, config=None, generic=None):
        self.omit = bool(config) and config.get("omit", False)

        if config is None:
            return

        self.dest_name = config.get("rename", self.dest_name)

        for conversion in config.get("conversions", []):
            self._add_conversion(conversion)

        self._add_generator(config.get("generator", None), generic)

    def _add_generator(self, meta, generic):
        if meta is None:
            return

        getter = attrgetter(meta["provider"])
        provider = getter(generic)
        kwargs = meta.get("kwargs", {})
        self.generator = DataGenerator(provider=provider, **kwargs)

    def _add_conversion(self, meta):
        conversion = getattr(conv, meta["fn"])
        kwargs = meta.get("kwargs", {})
        if kwargs:
            conversion = partial(
                conversion,
                **kwargs,
            )
        self.conversions.append(conversion)

    def get_value(self, value):
        for conversion in self.conversions:
            value = conversion(value)

        if self.generator:
            value = self.generator(value)

        return value
