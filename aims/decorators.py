from parsley.decorators import update_widget_attrs

def parsleyfy(klass):
    "A decorator to add {prefix}-* attributes to your form.fields"
    old_init = klass.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        prefix = getattr(getattr(self, 'Meta', None), 'data-parsley_namespace', 'data-parsley')
        for _, field in self.fields.items():
            update_widget_attrs(field, prefix)
        extras = getattr(getattr(self, 'Meta', None), 'parsley_extras', {})
        for field_name, data in extras.items():
            for key, value in data.items():
                if field_name not in self.fields:
                    continue
                attrs = self.fields[field_name].widget.attrs
                if key == 'equalto':
                    # Use HTML id for {prefix}-equalto
                    value = '#' + self[value].id_for_label
                if isinstance(value, bool):
                    value = "true" if value else "false"
                attrs["{prefix}-%s".format(prefix=prefix) % key] = value
    klass.__init__ = new_init

    return klass