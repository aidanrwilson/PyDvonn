#!/usr/bin/python3
"""
PyDVONN Program Structure Testbed
"""

import argparse
import logging
import time

import coloredlogs

import pyglet
from pyglet.gl import *  # Config, Context, ObjectSpace, current_context
from pyglet.window import NoSuchConfigException, Window, get_platform

# import os
# import sys

"""
=========
Constants
=========
"""


"""
Logging Constants
-----------------
"""
LOG_DATE_FORMAT = '%H:%M:%S'  # '%D%Y-%m-%d %H:%M:%S'
LOG_FIELD_STYLES = {
    'asctime':     {'color': 'white'},
    'hostname':    {'color': 'magenta'},
    'levelname':   {'color': 'black',
                    'bold':  True},
    'name':        {'color': 'blue'},
    'programname': {'color': 'cyan'}
}
LOG_FORMAT = '%(asctime)s.%(msecs)03d - %(name)s[%(process)d] - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'
LOG_LEVEL_STYLES = {
    'critical': {'color': 'red',
                 'bold':  True},
    'debug':    {'color': 'white'},
    'error':    {'color': 'red'},
    'info':     {'color': 'white'},
    'notice':   {'color': 'magenta'},
    'spam':     {'color': 'green',
                 'faint': True},
    'success':  {'color': 'green',
                 'bold':  True},
    'verbose':  {'color': 'blue'},
    'warning':  {'color': 'yellow'}
}

coloredlogs.install(
    datefmt=LOG_DATE_FORMAT,
    field_styles=LOG_FIELD_STYLES,
    fmt=LOG_FORMAT,
    level='DEBUG',
    level_styles=LOG_LEVEL_STYLES
)


"""
Pyglet Constants
----------------
"""

"""
### Pyglet Context Configuration Constants ###

Transparency channel size (2D bit depth)
Choose ALPHA_SIZE = 0 for no transparency (RGB),
       ALPHA_SIZE = 8 for transparency (RGBA).
"""
ALPHA_SIZE = 8

"""
Multisampling Parameters
    Choose SAMPLE_BUFFERS = 1 for multisampling,
           SAMPLE_BUFFERS = 0 for no multisampling.
    I'll use multisampling if supported by user hardware.
    If using multisampling, choose SAMPLES = 2 or 4.
"""
SAMPLE_BUFFERS = 1
SAMPLES = 4

DOUBLE_BUFFER = True
DEPTH_SIZE = 0
STENCIL_SIZE = 0
ACCUM_CHANNEL_SIZE = 0
AUX_BUFFERS = 0


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_RESIZABLE = True
WINDOW_CAPTION = 'PyDVONN'


def get_dvonn_config(alpha_size=ALPHA_SIZE, double_buffer=DOUBLE_BUFFER, sample_buffers=SAMPLE_BUFFERS, samples=SAMPLES,
                     depth_size=DEPTH_SIZE, stencil_size=STENCIL_SIZE, accum_channel_size=ACCUM_CHANNEL_SIZE, aux_buffers=AUX_BUFFERS):
    """
    Get DVONN game GL Config based on input parameters and platform capabilities.
    """

    platform = get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()

    template = Config(
        alpha_size=alpha_size,
        double_buffer=double_buffer,
        sample_buffers=sample_buffers,
        samples=samples,
        depth_size=depth_size,
        stencil_size=stencil_size,
        accum_red_size=accum_channel_size,
        accum_blue_size=accum_channel_size,
        accum_green_size=accum_channel_size,
        accum_alpha_size=accum_channel_size if alpha_size else 0,
        aux_buffers=aux_buffers
    )

    matching_configs = screen.get_matching_configs(template)
    if not matching_configs:
        raise NoSuchConfigException("Error in DvonnConfig __init__: No GL Config found matching all specifications")

    for config in screen.get_matching_configs(template):
        logging.info("GL Config matched all specifications:\n%s\n", config)
    logging.info("Choosing the best out of these Config options")
    config = screen.get_best_config(template)
    return config


class DvonnWindow(Window):
    """
    DVONN game Window based on input parameters.
    """

    def __init__(self, dvonn_config, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=WINDOW_RESIZABLE):
        super(DvonnWindow, self).__init__(width=width, height=height, resizable=resizable, caption=WINDOW_CAPTION, config=dvonn_config)
        # Manual correction of the stupidity that is inconsistent and incorrect use of resizable vs. resizeable
        # Constructor uses "resizable", class member variable is "resizeable", access method uses "resizeable", documentation of member variable "resizeable" uses the spelling "resizable" in the literal one line description one line away
        # The correct spelling is resizable, but at least if you spell it incorrectly, do it consistently dammit...
        self.resizeable = self.resizable

    def on_draw(self):
        logging.debug("ON_DRAW CALL")
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glBegin(GL_TRIANGLES)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height)
        glEnd()

    def on_resize(self, width, height):
        logging.debug("ON_RESIZE CALL")
        super(DvonnWindow, self).on_resize(width, height)


STANDARD_BOARD_WIDTH = 11
STANDARD_BOARD_HEIGHT = 5

# class Board():
#     def __init__(self, width=STANDARD_BOARD_WIDTH, height=STANDARD_BOARD_HEIGHT):
#         self.possible_fields = []
#         for i in range()


class FieldClass():
    def __init__(self, name, stack=None):
        self.name = name
        self.stack = stack
        if stack is None:
            self.valid = False


class StackClass():
    def __init__(self, height, control, order):
        self.height = height
        self.control = control
        self.order = order


class StackClassSlots():
    __slots__ = ('height', 'control', 'order')

    def __init__(self, height, control, order):
        self.height = height
        self.control = control
        self.order = order


class StackSubdictBase(dict):
    def __init__(self, height, control, order):
        super(StackSubdictBase, self).__init__(height=height, control=control, order=order)


class StackSubdictAttr(dict):
    __slots__ = ()

    def __init__(self, height, control, order):
        super(StackSubdictAttr, self).__init__(height=height, control=control, order=order)

    def __getattr__(self, attrname):
        logging.debug("Calling __getattr__(%s)", attrname)
        try:
            return dict.__getitem__(self, attrname)
        except KeyError as key_err:
            raise AttributeError(key_err)

    def __setattr__(self, attrname, attrval):
        logging.debug("Calling __getattr__(%s)", attrname)
        dict.__setitem__(self, attrname, attrval)

    # def __delattr__(self, attrname):
    #     logging.debug("Calling __getattr__(%s)", attrname)
    #     try:
    #         dict.__delitem__(self, attrname)
    #     except KeyError as key_err:
    #         raise AttributeError(key_err)


def start_game():
    """
    Start DVONN game.
    """

    config = get_dvonn_config()

    logging.info("Window GL Context Values Available, Given User-Specified Options:")
    logging.info("-> buffer_size: %s (%s, %s, %s, %s)", config.buffer_size,
                 config.red_size, config.green_size, config.blue_size, config.alpha_size)
    logging.info("-> stereo: %s", config.stereo)
    logging.info("-> double_buffer: %s", config.double_buffer)
    logging.info("-> sample_buffers: %s", config.sample_buffers)
    logging.info("-> samples: %s", config.samples)
    logging.info("-> depth_size: %s", config.depth_size)
    logging.info("-> stencil_size: %s", config.stencil_size)
    logging.info("-> accum_size: (%s, %s, %s, %s)", config.accum_red_size,
                 config.accum_blue_size, config.accum_green_size, config.accum_alpha_size)
    logging.info("-> aux_buffers: %s", config.aux_buffers)
    logging.info("-> major_version: %s", config.major_version)
    logging.info("-> minor_version: %s", config.minor_version)
    logging.info("-> forward_compatible: %s", config.forward_compatible)

    window = DvonnWindow(config)
    print(dir(window))

    logging.info("Created DvonnWindow with Following Initial Values:")
    logging.info("-> (width, height): (%s, %s)", window.width, window.height)
    logging.info("-> caption: %s", window.caption)
    # logging.info("-> resizable: %s", window.resizable)
    logging.info("-> style: %s", window.style)

    pyglet.app.run()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()

    ### ADD WHATEVER ARGS ###

    ARGS = PARSER.parse_args()

    ### DO WHATEVER WITH ARGUMENTS ###

    start_game()
