from pynput import keyboard
from pynput.keyboard import Key
from pyparrot.DroneVisionGUI import DroneVisionGUI
import threading

ROTATION = 50.0
FLY_DURATION = 2.0
SLEEP_DURATION = 4.0
FLIP_SLEEP_DURATION = 6.0


class Demo:
    def __init__(self, mambo):
        self.mambo = mambo

    def execute(self):
        pass

    def takeoff(self):
        self.mambo.safe_takeoff(4)
        return self.mambo.sensors.flying_state != "emergency"

    def land(self):
        self.mambo.smart_sleep(SLEEP_DURATION)
        self.mambo.safe_land(4)


class DemoSquare(Demo):
    def __init__(self, mambo):
        super().__init__(mambo)

    @staticmethod
    def pint(mamboVision, args):
        print('created vision')

        mambo = args[0]

        mambo.smart_sleep(SLEEP_DURATION)
        mambo.turn_degrees(-90)
        mambo.smart_sleep(SLEEP_DURATION)
        mambo.fly_direct(roll=0, pitch=ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION)
        mambo.fly_direct(roll=0, pitch=-ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION / 10)

        mambo.smart_sleep(SLEEP_DURATION)
        mambo.turn_degrees(90)
        mambo.smart_sleep(SLEEP_DURATION)
        mambo.fly_direct(roll=0, pitch=ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION)
        mambo.fly_direct(roll=0, pitch=-ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION / 10)

        mambo.smart_sleep(SLEEP_DURATION)
        mambo.turn_degrees(90)
        mambo.smart_sleep(SLEEP_DURATION)
        mambo.fly_direct(roll=0, pitch=ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION)
        mambo.fly_direct(roll=0, pitch=-ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION / 10)

        mambo.smart_sleep(SLEEP_DURATION)
        mambo.turn_degrees(90)
        mambo.smart_sleep(SLEEP_DURATION)
        mambo.fly_direct(roll=0, pitch=ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION)
        mambo.fly_direct(roll=0, pitch=-ROTATION, yaw=0, vertical_movement=0,
                              duration=FLY_DURATION / 10)

        mambo.smart_sleep(SLEEP_DURATION)
        mambo.turn_degrees(180)

        mamboVision.close_video()
        mamboVision.close_exit()

        return True

    def execute(self):

        super().takeoff()

        mamboVision = DroneVisionGUI(self.mambo, is_bebop=False, buffer_size=200, user_code_to_run=DemoSquare.pint,
                                     user_args=(self.mambo,))
        mamboVision.open_video()
        print('opened video')

        super().land()

class DemoFlips(Demo):
    def __init__(self, mambo):
        super().__init__(mambo)

    def execute(self):
        if not super().takeoff():
            return False

        success = self.mambo.flip("right")
        if not success:
            super().land()
            return False
        self.mambo.smart_sleep(SLEEP_DURATION)

        success = self.mambo.flip("left")
        if not success:
            super().land()
            return False
        self.mambo.smart_sleep(SLEEP_DURATION)

        success = self.mambo.flip("front")
        if not success:
            super().land()
            return False
        self.mambo.smart_sleep(SLEEP_DURATION)

        success = self.mambo.flip("back")
        if not success:
            super().land()
            return False
        self.mambo.smart_sleep(SLEEP_DURATION)

        super().land()
        return True


class KeyboardEvent:
    def __init__(self, mod, key):
        self.__mod = mod
        self.__key = key

    def get_key(self):
        return self.__key

    def get_mod(self):
        return self.__mod


class KeyPressedEvent(KeyboardEvent):
    def __init__(self, key):
        super().__init__(1, key)


class KeyReleasedEvent(KeyboardEvent):
    def __init__(self, key):
        super().__init__(0, key)


eventQueue = []  # Queue()


def init_keyboard():
    with keyboard.Listener(
            on_release=on_key_release,
            on_press=on_key_pressed
    ) as listener:
        listener.join()


_exit = False


lock = threading.Lock()


keys = {}


def on_key_release(key):
    global keys
    keys[key] = False
    if _exit:
        return


def on_key_pressed(key):
    global keys
    keys[key] = True
    if _exit:
        return


class DemoKeyboard(Demo):
    def __init__(self, mambo):
        super().__init__(mambo)

    def execute(self):
        threading.Thread(target=init_keyboard).start()
        global _exit

        in_air = False
        print('Ready')
        while not _exit:
            pitch = 0
            roll = 0
            vertical_movement = 0
            if Key.space in keys and keys[Key.space]:
                if not in_air:
                    print('Zboara')
                    if not super().takeoff():
                        return False
                    in_air = True
                else:
                    print('Aterizeaza')
                    super().land()
                    in_air = False
            if Key.esc in keys and keys[Key.esc]:
                print('Iesire')
                _exit = True
                break
            if Key.up in keys and keys[Key.up]:
                pitch += ROTATION
            if Key.down in keys and keys[Key.down]:
                pitch -= ROTATION
            if Key.right in keys and keys[Key.right]:
                roll += ROTATION
            if Key.left in keys and keys[Key.left]:
                roll -= ROTATION
            if Key.left in keys and keys[Key.left]:
                roll -= ROTATION
            if Key.f3 in keys and keys[Key.f3]:
                vertical_movement += 40
            if Key.f4 in keys and keys[Key.f4]:
                vertical_movement -= 40
            if roll != 0 or pitch != 0 or vertical_movement != 0:
                self.mambo.fly_direct(roll=roll, pitch=pitch, yaw=0, vertical_movement=vertical_movement, duration=0.01)
            else:
                if Key.f1 in keys and keys[Key.f1]:
                    self.mambo.turn_degrees(45)
                elif Key.f2 in keys and keys[Key.f2]:
                    self.mambo.turn_degrees(-45)
                else:
                    if Key.f5 in keys and keys[Key.f5]:
                        self.mambo.flip('right')
                    elif Key.f6 in keys and keys[Key.f6]:
                        self.mambo.flip('left')
                    elif Key.f7 in keys and keys[Key.f7]:
                        self.mambo.flip('front')
                    elif Key.f8 in keys and keys[Key.f8]:
                        self.mambo.flip('back')

        super().land()
        return True
