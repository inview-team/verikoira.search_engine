from .robot import Robot


class RobotFactory:
    def __init__(self):
        self._robots = {}

    def register_platform(self, search_type: str, robot: Robot):
        self._robots[search_type] = robot

    def get_robot(self, search_type: str, **kwargs) -> Robot:
        bot = self._robots.get(search_type)
        if not bot:
            raise Exception(search_type, list(self._robots.keys()))
        return bot(**kwargs)
