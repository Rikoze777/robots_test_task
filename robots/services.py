import json
from robots.models import Robot
from django.core import serializers
from robots.validators import RobotSchema
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count


def save_robot(data):
    RobotSchema(**data)
    serial = f"{data['model']}-{data['version']}"
    robot = Robot(
                serial=serial,
                model=data['model'],
                version=data['version'],
                created=datetime.strptime(data['created'],
                                          "%Y-%m-%d %H:%M:%S"),
            )
    robot.save()
    return robot


def serialize_obj(object):
    serialized_obj = serializers.serialize('json', [object, ])
    serialized = serialized_obj.strip("[]")
    to_json = json.loads(serialized)
    return to_json['fields']


def fetch_robots():
    week_robots = {}
    end_date = timezone.now()
    start_date = end_date - timedelta(7)
    queryset = Robot.objects.filter(created__range=(start_date, end_date)
                                    ).values('model', 'version').annotate(
                                    count=Count('created')
                                    )

    for item in queryset:
        model = item['model']
        version = item['version']
        count = item['count']

        if model not in week_robots:
            week_robots[model] = {}

        if version not in week_robots[model]:
            week_robots[model][version] = 0

        week_robots[model][version] += count

    return week_robots
