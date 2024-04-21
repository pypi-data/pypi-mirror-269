class Capture:

    # Parameters
    is_button_pressed = False
    drone_x = 0.0
    drone_y = 0.0
    drone_z = 0.0
    drone_angle = 0.0
    move_x = 0.0
    move_y = 0.0
    move_z = 0.0
    rotate = 0.0
    is_captured = False
    object_position = [-25, 17, -50]
    object_rotate = 360.0

    def __init__(self, object_position, object_rotate):
        self.is_button_pressed = False
        self.drone_x = 0.0
        self.drone_y = 0.0
        self.drone_z = 0.0
        self.drone_angle = 0.0
        self.move_x = 0.0
        self.move_y = 0.0
        self.move_z = 0.0
        self.rotate = 0.0
        self.is_captured = False
        self.object_position = object_position
        self.object_rotate = object_rotate

    def run(self, send_array):
        if self.is_button_pressed:
            if self.is_captured:
                self.move_x = (send_array[6] - self.drone_x) / 100
                self.move_y = (send_array[7] - self.drone_y) / 100
                self.move_z = (send_array[9] - self.drone_z) / 100
                self.rotate = send_array[8] - self.drone_angle
                send_array[10] = self.object_position[0] + self.move_x
                send_array[11] = self.object_position[1] + self.move_y
                send_array[12] = self.object_position[2] + self.move_z
                send_array[0] = self.object_rotate + self.rotate
            else:
                self.drone_x = send_array[6]
                self.drone_y = send_array[7]
                self.drone_z = send_array[9]
                self.drone_angle = send_array[8]
                self.is_captured = True
        else:
            self.object_rotate = send_array[0]
            self.object_position = [send_array[10], send_array[11], send_array[12]]
            self.is_captured = False
        return send_array