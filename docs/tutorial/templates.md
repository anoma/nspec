---
icon: material/dice-1
template: templates/machine.md
machine_name: xxxx
purpose: yyyy
---

# Using Templates

All the templates are stored in the `overrides/templates` directory. 

{% block purpose %}
{{ super() }}
XXXXXXXXXX

{% endblock %}