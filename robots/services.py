import json
from robots.models import Robot
from django.core import serializers
from robots.validators import RobotSchema
from datetime import datetime


def save_robot(data):
    RobotSchema(**data)
    serial = f"{data['model']}-{data['version']}"
    robot = Robot(
                serial=serial,
                model=data['model'],
                version=data['version'],
                created=datetime.strptime(data['created'], "%Y-%m-%d %H:%M:%S"),
            )
    robot.save()
    return robot


def serialize_obj(object):
    serialized_obj = serializers.serialize('json', [object, ])
    serialized = serialized_obj.strip("[]")
    to_json = json.loads(serialized)
    return to_json['fields']
