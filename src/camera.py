
class Camera():
    def __init__(self, pos, size, zoom):
        self.pos = pos
        self.size = size
        self.zoom = zoom

    def zoom(self, value):
        self.zoom *= value

        self.size[0] *= value
        self.size[1] *= value

    def draw_object(self, list_obj):

        for obj in list_obj:
            if obj.shape == 'circle':
                if self.pos[0] - obj.radius - self.size[0] / 2 < obj[0] < self.pos[0] + obj.radius + self.size[0] / 2\
                and self.pos[1] - obj.radius - self.size[1] / 2 < obj[1] < self.pos[1] + obj.radius + self.size[1] / 2:
                    loc_pos_in_camera = [obj[0] - self.pos[0] - self.size / 2, obj[1] - self.pos[1] - self.size / 2]

                    obj.draw(loc_pos_in_camera)

            if obj.shape == 'rect':
                if self.pos[0] - obj.size[0] - self.size[0] / 2 < obj[0] < self.pos[0] + obj.size[0] + self.size[0] / 2\
                and self.pos[1] - obj.size[1] - self.size[1] / 2 < obj[1] < self.pos[1] + obj.size[1] + self.size[1] / 2:
                    loc_pos_in_camera = [obj[0] - self.pos[0] - self.size / 2, obj[1] - self.pos[1] - self.size / 2]

                    obj.draw(loc_pos_in_camera)

