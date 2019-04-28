import json
import string

from itertools import chain
from tmo import exceptions as tmo_exceptions
from tmo import filters as tmo_filters


ATTRIB_SEPARATOR = '#'
FILTER_SEPARATOR = '@'


class TMOFormatter(string.Formatter):
    """Templated Message Output Formatter"""

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth,
                 auto_arg_index=0):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in \
                self.parse(format_string):

            # output the literal text
            if literal_text:
                result.append(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #  the formatting

                # handle arg indexing when empty field_names are given.
                if field_name == '':
                    if auto_arg_index is False:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    field_name = str(auto_arg_index)
                    auto_arg_index += 1
                elif field_name.isdigit():
                    if auto_arg_index:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    # disable auto arg incrementing, if it gets
                    # used later on, then an exception will be raised
                    auto_arg_index = False

                # given the field_name, find the object it references
                #  and the argument it came from
                field_name, filter_fns = self.get_filters(field_name)
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)

                # do any conversion on the resulting object
                obj = self.convert_field(obj, conversion)

                # expand the format spec, if needed
                format_spec, auto_arg_index = self._vformat(
                    format_spec, args, kwargs,
                    used_args, recursion_depth-1,
                    auto_arg_index=auto_arg_index)

                # format the object and append to the result
                result.append(self.format_field(obj, format_spec, filter_fns))

        return ''.join(result), auto_arg_index

    def format_field(self, value, format_spec, filter_fns):
        return self.filter_value(value, format_spec, filter_fns)

    def get_filters(self, key):
        """Retrieves filter function from key in order."""
        if 'join' not in key:
            # Use join with default params if not specified in template
            key += '@join()'

        key, *filter_fns = key.split(FILTER_SEPARATOR)
        return key, [eval('tmo_filters.%s' % filter_fn)
                     for filter_fn in filter_fns]

    def filter_value(self, value, format_spec, filter_fns):
        if not filter_fns:
            return value

        filter_fns.sort(key=lambda s: s.__name__.startswith('join'),
                        reverse=True)
        join_fn, *filter_fns = filter_fns

        if not isinstance(value, (list, tuple)):
            value = [value]

        results = []
        for val in value:
            val = super().format_field(val, format_spec)
            for fn in filter_fns:
                val = fn(val)
            results.append(val)
        return join_fn(results)


tmo_formatter = TMOFormatter()


class TMOEngine:
    """Templated Message Output Engine"""

    def __init__(self, formatter=None):
        self.formatter = formatter
        self.templates = None

    def load_templates(self, abs_fpath):
        """Load new template file."""
        with open(abs_fpath) as f:
            self.templates = json.load(f)

    def load_formatter(self, formatter):
        """Load new string formatter."""
        if not issubclass(formatter.__class__, string.Formatter):
            raise tmo_exceptions.FormatterInvalid
        self.formatter = formatter

    def gettext(self, template_id, **kwargs):
        """Substitutes values for the parameters in templated string."""
        if self.templates is None:
            raise tmo_exceptions.TemplatesNotInitialized
        if self.formatter is None:
            raise tmo_exceptions.TemplatesNotInitialized

        if ATTRIB_SEPARATOR not in template_id:
            # automatically switch to a plural template if appropriate;
            # if there isn't one, we'll just revert to the original template_id
            plurals = sorted('%ss' % k for k, v in kwargs.items()
                             if isinstance(v, (list, tuple)) and len(v) > 1)
            template_id = ATTRIB_SEPARATOR.join(chain([template_id], plurals))

        try:
            template = self.templates[template_id]
        except KeyError:
            if ATTRIB_SEPARATOR not in template_id:
                raise
            # Fallback to base template
            template = self.templates[template_id.split(ATTRIB_SEPARATOR)[0]]

        return self.formatter.format(template, **kwargs)


tmo_engine = TMOEngine(tmo_formatter)


def gettext(template_id, **kwargs):
    """Wrapper around TMOEngine gettext method."""
    return tmo_engine.gettext(template_id, **kwargs)
