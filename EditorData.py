from ReadApiGa import Param

class LevelInfo:
    def __init__(self):
        self.name = ""
        self.music = None
        self.script = None
        self.parallax = None

class ObjectsInfo:
    def __init__(self):
        self.objects = []

    def add(self, name:str, class_ref:str, params: list[Param]):
        self.objects.append({"name": name, "classs_ref": class_ref, "params": params})

    def name_dont_exist(self, name: str) -> bool:
        names = [obj["name"] for obj in self.objects]
        if not name in names:
            return True
        return False

class ObjectLayout:
    def __init__(self):
        pass

