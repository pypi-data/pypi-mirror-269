{% include "!autosummary/module.rst" %}

{% if attributes %}
{{ _("Module Attributes") | underline("-") }}

{% for item in attributes %}
.. autodata:: {{ item }}
{%- endfor %}
{% endif %}


{% if functions %}
{{ _("Functions") | underline("-") }}

{% for item in functions %}
.. autofunction:: {{ item }}
{%- endfor %}
{% endif %}


{% if classes %}
{{ _("Classes") | underline("-") }}

{% for item in classes %}
.. autoclass:: {{ item }}
   :show-inheritance:
   :special-members:
   :members:
   :undoc-members:
{%- endfor %}
{% endif %}


{% if exceptions %}
{{ _("Exceptions") | underline("-") }}

{% for item in exceptions %}
.. autoexception:: {{ item }}
   :show-inheritance:
   :special-members:
   :members:
   :undoc-members:
{%- endfor %}
{% endif %}
