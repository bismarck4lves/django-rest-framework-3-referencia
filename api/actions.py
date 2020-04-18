from rest_framework import serializers

class ActionSerializer:
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        meta = getattr(self, 'Meta', None)
        self.action_fields_map: dict = getattr(meta, 'action_fields_map', None)
        self._validate_action_fields_map(self.action_fields_map)

    def _validate_action_fields_map(self, action_fields_map: dict):
        print(action_fields_map)