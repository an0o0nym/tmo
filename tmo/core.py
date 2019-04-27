import json
import os
import string

from itertools import chain
from tmo import exceptions as tmo_exceptions
from tmo import filters as tmo_filters


ATTRIB_SEPARATOR = '#'
FILTER_SEPARATOR = '@'


class TMOFormatter(string.Formatter):
    """Templated Message Output Formatter"""
    connector_word = ' and '
    separator_char = ', '

    def get_filters(self, key):
        """Retrieves filter function from key"""
        if FILTER_SEPARATOR not in key:
            return key, None
        key, filter_fn = key.split(FILTER_SEPARATOR)
        return key, eval('tmo_filters.%s' % filter_fn)

    def get_value(self, key, args, kwargs):
        """
        Substitutes multi-value arguments
        for single parameter in templated string.
        """
        connector_word = kwargs.get('connector_word') or self.connector_word
        separator_char = kwargs.get('separator_char') or self.separator_char

        key, filter_fn = self.get_filters(key)
        val = super().get_value(key, args, kwargs)

        if not isinstance(val, (list, tuple)):
            return filter_fn(val) if filter_fn else val

        if filter_fn:
            val = list(map(filter_fn, val))

        v_head, v_tail = val[:-2], val[-2:]
        v_tail = [connector_word.join(v_tail)]
        return separator_char.join(v_head + v_tail)


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
            # automatically switch to a plural template if appropriate; if there isn't one, we'll
            # just revert to the original template_id
            plurals = sorted('%ss' % k for k, v in kwargs.items() if isinstance(v, list) and len(v) > 1)
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


def gettext(template_id, connector_word=None, separator_char=None, **kwargs):
    """
    Wrapper around TMOEngine gettext method. Allows to specify:
        - separator_char - a CHARACTER joining all elements of
          multi-value argument, except last two elements.
        - connector_word - a WORD joining last two elements
          of multi-value argument.

    """
    kwargs = {
        'connector_word': connector_word,
        'separator_char': separator_char,
        **kwargs
    }
    return tmo_engine.gettext(template_id, **kwargs)


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATES_PATH = os.path.join(BASE_DIR, 'fixtures', 'templates.json')

    tmo_engine.load_templates(TEMPLATES_PATH)

    print(gettext('fav_obj', objs=['test', 'python', 'others']))