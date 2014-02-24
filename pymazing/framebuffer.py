"""
Software framebuffer built on top of OpenGL textured quad.

:copyright: © 2014 Mikko Ronkainen <firstname@mikkoronkainen.com>
:license: MIT License, see the LICENSE file.
"""

import numpy as np
import OpenGL.GL as gl


class FrameBuffer:
    def __init__(self):
        self.pixel_data = None
        self.depth_data = None
        self.width = 0
        self.height = 0
        self.depth_clear_value = np.finfo(np.float32).min
        self.textureId = gl.glGenTextures(1)
        self.use_smoothing = False

        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.textureId)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

        self.set_smoothing(True)

    def resize(self, width, height):
        self.width = width
        self.height = height

        self.pixel_data = np.empty(self.width * self.height, np.uint32)
        self.depth_data = np.empty(self.width * self.height, np.float32)

        self.clear()

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_INT_8_8_8_8_REV, self.pixel_data)

    def clear(self):
        self.pixel_data.fill(0)
        self.depth_data.fill(self.depth_clear_value)

    def set_smoothing(self, state):
        self.use_smoothing = state

        if self.use_smoothing:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        else:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)


    def render(self):
        gl.glTexSubImage2D(gl.GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, gl.GL_RGBA, gl.GL_UNSIGNED_INT_8_8_8_8_REV, self.pixel_data)

        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0.0, 0.0)
        gl.glVertex3f(-1.0, -1.0, 0.0)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex3f(1.0, -1.0, 0.0)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex3f(1.0, 1.0, 0.0)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex3f(-1.0, 1.0, 0.0)
        gl.glEnd()
