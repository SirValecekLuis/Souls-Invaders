"""
TimeManager class

This class provides time management functionality for games, including:
* Tracking delta time and total time
* Limiting frame rate
* Calculating and updating current FPS
* Pausing and unpausing the game loop

Attributes:
    _target_fps: Target frame rate per second.
    _frame_time: Time duration of a single frame.
    _is_paused: Flag indicating whether the game is paused.
    _delta_time: Time elapsed since the last frame.
    _total_time: Total elapsed time since the start of the game.
    _last_time: Timestamp of the last frame.
    _accumulator: Accumulated time since the last frame.
    _fps_samples: A deque to store recent frame times for FPS calculation.
    _current_fps: Current calculated FPS.
    _fps_update_interval: Interval for updating the FPS calculation.
    _fps_last_update: Timestamp of the last FPS update.

Methods:
    update(): Updates the time manager's internal state, calculates delta time, and limits the frame rate.
    set_target_fps(): Sets the target frame rate.
    _pause(): Pauses the time manager.
    _unpause(): Resumes the time manager.
    toggle_pause(): Toggles the pause state of the time manager.
    get_delta_time(): Returns the delta time since the last frame.
    get_total_time(): Returns the total time elapsed since the start of the game in milliseconds.
    target_fps: Property to get the target frame rate.
"""

import time
from collections import deque

import pygame.time


class TimeManager:
    def __init__(self, target_fps: int = 144):
        """
        Initializes the TimeManager instance.

        Args:
            target_fps (int, optional): Target frame rate per second. Defaults to 60.
        """

        self.__target_fps = target_fps
        self.__frame_time = 1.0 / target_fps
        self.__is_paused = False
        self.__delta_time = 0
        self.__total_time = 0
        self.__last_time = time.perf_counter()
        self.__accumulator = 0

        self.__fps_samples = deque(maxlen=target_fps)
        self.__current_fps = 0
        self.__fps_update_interval = 0.25
        self.__fps_last_update = time.perf_counter()

    def update(self):
        """Updates the time manager's internal state, calculates delta time, and limits the frame rate."""

        current_time = time.perf_counter()
        frame_time = current_time - self.__last_time

        # FPS limiting
        self.__accumulator += frame_time
        if self.__accumulator < self.__frame_time:
            sleep_time = self.__frame_time - self.__accumulator
            pygame.time.wait(max(0, int(sleep_time * 1000)))
            self.__accumulator = 0

            current_time = time.perf_counter()
            frame_time = current_time - self.__last_time
        else:
            self.__accumulator = 0

        self.__last_time = current_time

        # FPS calculation
        if frame_time > 0:
            self.__fps_samples.append(1.0 / frame_time)

        if current_time - self.__fps_last_update >= self.__fps_update_interval:
            if len(self.__fps_samples) > 0:
                self.__current_fps = sum(self.__fps_samples) / len(self.__fps_samples)
            self.__fps_last_update = current_time

        if not self.__is_paused:
            self.__delta_time = frame_time
            self.__total_time += frame_time
        else:
            self.__delta_time = 0

    def set_target_fps(self, fps: int):
        """Sets the target frame rate.

        Args:
            fps: The new target frame rate.
        """

        self.__target_fps = fps
        self.__frame_time = 1.0 / fps

    def _pause(self):
        """Pauses the time manager."""

        self.__is_paused = True

    def _unpause(self):
        """Resumes the time manager."""

        self.__is_paused = False
        self.__last_time = time.perf_counter()

    def toggle_pause(self):
        """Toggles the pause state of the time manager."""

        if self.__is_paused:
            self._unpause()
        else:
            self._pause()

    def get_delta_time(self) -> float:
        """Returns the delta time since the last frame.

        Returns:
            float: Delta time in seconds.
        """

        return self.__delta_time

    def get_total_time(self) -> float:
        """Returns the total time elapsed since the start of the game in milliseconds.

        Returns:
            float: Total time in milliseconds.
        """

        return self.__total_time * 1000

    @property
    def target_fps(self) -> int:
        """Returns the target frame rate.

        Returns:
            int: Target frame rate.
        """

        return self.__target_fps

    def get_fps(self) -> float:
        """Returns the current frame rate.

        Returns:
            float: Current frame rate.
        """

        return round(self.__current_fps, 1)
