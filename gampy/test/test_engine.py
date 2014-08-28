__author__ = 'michiel'

import unittest
from OpenGL.GL import *

class OpenGLTest(unittest.TestCase):
    def test_fbo( self ):
        """Test that we support framebuffer objects

        http://www.gamedev.net/reference/articles/article2331.asp
        """
        if not glGenFramebuffers:
            return False
        width = height = 128
        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        depthbuffer = glGenRenderbuffers(1 )
        glBindRenderbuffer(GL_RENDERBUFFER, depthbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)
        glFramebufferRenderbuffer(
            GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER,
            depthbuffer
        )
        img = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, img)
        # NOTE: these lines are *key*, without them you'll likely get an unsupported format error,
        # ie. GL_FRAMEBUFFER_UNSUPPORTED
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST);
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB8,
            width, height, 0, GL_RGB,
            GL_INT,
            None # no data transferred
        )
        glFramebufferTexture2D(
            GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,
            img,
            0 # mipmap level, normally 0
        )
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        assert status == GL_FRAMEBUFFER_COMPLETE, status
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glPushAttrib(GL_VIEWPORT_BIT) # viewport is shared with the main context
        try:
            glViewport(0,0,width, height)

            # rendering to the texture here...
            glColor3f( 1,0,0 )
            glNormal3f( 0,0,1 )
            glBegin( GL_QUADS )
            for v in [[0,0,0],[0,1,0],[1,1,0],[1,0,0]]:
                glColor3fv( v )
                glVertex3dv( v )
            glEnd()
        finally:
            glPopAttrib(); # restore viewport
        glBindFramebuffer(GL_FRAMEBUFFER, 0) # unbind

        glBindTexture(GL_TEXTURE_2D, img)

        glEnable( GL_TEXTURE_2D )

        # rendering with the texture here...
        glColor3f( 1,1,1 )
        glNormal3f( 0,0,1 )
        glDisable( GL_LIGHTING )
        glBegin( GL_QUADS )
        try:
            for v in [[0,0,0],[0,1,0],[1,1,0],[1,0,0]]:
                glTexCoord2fv( v[:2] )
                glVertex3dv( v )
        finally:
            glEnd()



if __name__ == '__main__':
    unittest.main()