from physics import Body

active_objs = []

class Entity:
    def __init__(self, *components, x=0, y=0):
        self.components = []
        for c in components:
            self.add(c)
        self.x = x
        self.y = y
        active_objs.append(self)

    def update(self, *args):
        for c in self.components:
            if hasattr(c, "update"):
                c.update(*args)   # call component update

    def draw(self, screen):
        for c in self.components:
            if hasattr(c, "draw"):
                c.draw(screen)

    def add(self, component):
        self.components.append(component)
        component.entity = self

    def remove(self, kind):
        c = self.get(kind)
        if c is not None:
            c.entity = None
            self.components.remove(c)

    def has(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return True
        return False

    def get(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return c
        return None
    
    def get_draw_depth(self):
        body = self.get(Body)
        if body is not None:
            return self.y + body.hitbox.y + body.hitbox.height
        return self.y