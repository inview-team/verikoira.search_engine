from importlib import import_module

from .factory import RobotFactory

AVAILABLE_RESOURCES = ["patent"]

robot_factory = RobotFactory()


def register_available_resources():
    for resource in AVAILABLE_RESOURCES:
        robot_class_name = f"{resource.capitalize()}Robot"
        robot_class = getattr(
            import_module(f".{resource}", package=__name__),
            robot_class_name,
        )

        robot_factory.register_platform(resource, robot_class)


register_available_resources()
