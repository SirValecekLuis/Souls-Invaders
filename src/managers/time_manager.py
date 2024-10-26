import time


class TimeManager:
    def __init__(self, target_fps: int = 60):
        self.__target_fps = target_fps
        self.__frame_time = 1.0 / target_fps
        self.__is_paused = False
        self.__delta_time = 0
        self.__total_time = 0
        self.__last_time = time.perf_counter()
        self.__accumulator = 0

    def update(self):
        current_time = time.perf_counter()
        frame_time = current_time - self.__last_time
        self.__last_time = current_time

        if not self.__is_paused:
            self.__delta_time = self.__frame_time
            self.__total_time += frame_time
        else:
            self.__delta_time = 0

        # FPS limiting
        self.__accumulator += frame_time
        if self.__accumulator < self.__frame_time:
            sleep_time = self.__frame_time - self.__accumulator
            time.sleep(max(0, sleep_time))
            self.__accumulator = 0
        else:
            self.__accumulator = 0

    def set_target_fps(self, fps: int):
        self.__target_fps = fps
        self.__frame_time = 1.0 / fps

    def _pause(self):
        self.__is_paused = True

    def _unpause(self):
        self.__is_paused = False
        self.__last_time = time.perf_counter()

    def toggle_pause(self):
        if self.__is_paused:
            self._unpause()
        else:
            self._pause()
        print(f"Game is paused: {self.__is_paused}")

    def get_delta_time(self):
        return self.__delta_time

    def get_total_time(self):
        return self.__total_time * 1000

    @property
    def target_fps(self):
        return self.__target_fps
