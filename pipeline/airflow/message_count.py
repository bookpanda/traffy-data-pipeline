from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

from pipeline.stream import get_count


class MessageCountSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, threshold, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threshold = threshold

    def poke(self, context):
        current_count = get_count()
        return current_count >= self.threshold
