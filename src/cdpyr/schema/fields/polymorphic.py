import typing

from marshmallow import class_registry, fields, types, utils
from marshmallow.base import SchemaABC
from marshmallow.exceptions import StringNotCollectionError, ValidationError
from marshmallow.utils import is_collection, missing as missing_


class Polymorphic(fields.Field):
    default_error_messages = {"type": "Invalid type."}

    def __init__(
            self,
            candidates: typing.Iterable[
                typing.Tuple[object, typing.Union[SchemaABC, type, str]]],
            *,
            default: typing.Any = missing_,
            only: types.StrSequenceOrSet = None,
            exclude: types.StrSequenceOrSet = (),
            many: bool = False,
            unknown: str = None,
            **kwargs
    ):
        # Raise error if only or exclude is passed as string, not list of
        # strings
        if only is not None and not is_collection(only):
            raise StringNotCollectionError(
                    '"only" should be a collection of strings.')
        if exclude is not None and not is_collection(exclude):
            raise StringNotCollectionError(
                    '"exclude" should be a collection of strings.'
            )
        self.candidates = candidates
        self.only = only
        self.exclude = exclude
        self.many = many
        self.unknown = unknown
        self._schemas = None  # Cached Schema instance
        super().__init__(default=default, **kwargs)
    @property
    def schemas(self):
        if not self._schemas:
            self._schemas = []
            for candidate, schema in self.candidates:
                # Inherit context from parent.
                context = getattr(self.parent, "context", {})
                if isinstance(schema, SchemaABC):
                    schema.many = False
                    schema.context.update(context)
                    # Respect only and exclude passed from parent and
                    # re-initialize fields
                    set_class = schema.set_class
                    if self.only is not None:
                        if schema.only is not None:
                            original = schema.only
                        else:  # only=None -> all fields
                            original = schema.fields.keys()
                        schema.only = set_class(self.only).intersection(
                                original)
                    if self.exclude:
                        original = schema.exclude
                        schema.exclude = set_class(self.exclude).union(
                                original)
                    # ensure sub-schemas won't convert into `lists`
                    schema.many = False
                    schema._init_fields()
                    self._schemas.append((candidate, schema))
                else:
                    if isinstance(schema, type) and issubclass(schema,
                                                               SchemaABC):
                        schema_class = schema
                    elif not isinstance(schema, (str, bytes)):
                        raise ValueError(
                                "Polymorphic fields must be passed a "
                                "Schema, not {}.".format(schema.__class__)
                        )
                    elif schema == "self":
                        ret = self
                        while not isinstance(ret, SchemaABC):
                            ret = ret.parent
                        schema_class = ret.__class__
                    else:
                        schema_class = class_registry.get_class(schema)
                    self._schemas.append((candidate, schema_class(
                            many=False,
                            only=self.only,
                            exclude=self.exclude,
                            context=context,
                            load_only=self._nested_normalized_option(
                                    "load_only"),
                            dump_only=self._nested_normalized_option(
                                    "dump_only"),
                    )))
        return self._schemas

    def _nested_normalized_option(self, option_name: str) -> typing.List[str]:
        nested_field = "%s." % self.name
        return [
                field.split(nested_field, 1)[1]
                for field in getattr(self.root, option_name, set())
                if field.startswith(nested_field)
        ]

    def _serialize(self, nested_obj, attr, obj, many=False, **kwargs):
        # load up the schema first. this allows a registryerror to be raised
        # if an invalid schema name was passed
        schemas = self.schemas
        if nested_obj is None:
            return None
        many = self.many or many
        if not many:
            nested_obj = [nested_obj]
        # always create a list of serialized objects
        result = []

        # match all objects against a schema candidate
        obj_schemas = [
                [schema for base, schema in schemas if isinstance(obj, base)]
                for
                obj in nested_obj]

        # loop over each object
        for obj, schema in zip(nested_obj, obj_schemas):
            # try to get the matching schema - it will fail if there object
            # could not be resolved to a supported class
            try:
                schema = schema[0]
                value = schema.dump(obj, many=schema.many)
            except IndexError:
                value = None
            # append the result to the list
            result.append(value)

        # return many or one object?
        return result if many else result[0]

    def _test_collection(self, value, many=False):
        many = any(
                schema.many for _, schema in self.schemas) or self.many or many
        if many and not utils.is_collection(value):
            raise self.make_error("type", input=value,
                                  type=value.__class__.__name__)

    def _load(self, value, data, partial=None, many=False):
        many = self.many or many
        if not many:
            value = [value]

        # Loop over each object and append it
        results = [self._load_value(obj, data, partial=partial) for obj in
                   value]

        # return many or one object?
        return results if many else results[0]

    def _load_value(self, value, data, partial=None):
        # No valid data found for this object
        valid_data = None

        # loop over each candidate and try it
        for candidate, schema in self.schemas:
            try:
                valid_data = schema.load(value, unknown=self.unknown,
                                         partial=partial, many=schema.many)
            except ValidationError as error:
                pass
        # return whatever we have
        return valid_data

    def _deserialize(self, value, attr, data, partial=None, many=False,
                     **kwargs):
        self._test_collection(value, many=many)
        return self._load(value, data, partial=partial, many=many)
