Templated Message Output
---

Python module for nice formatting of multi-value arguments in string templates.

HOWTO
---
1. Add `tmo` parent directory to `PYTHONPATH`
1. Load templates & start using `tmo`'s `gettext` function:

   ```
   from tmo.core import tmo_engine, gettext
   
   tmo_engine.load_templates(TEMPLATES_ABSOLUTE_PATH)
   
   print(gettext(string_template_id, args, kw_arg1='arg1', kw_arg2='arg2'))
   ```
