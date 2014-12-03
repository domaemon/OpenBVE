#!/usr/bin/env python

import sys
import getopt
import re

replace_dict = {
    "using Tao.OpenGl;": "using OpenTK.Graphics.OpenGL;",
    "Gl.glAlphaFunc": "GL.AlphaFunc",
    "Gl.glClearColor": "GL.ClearColor",
    "Gl.glColor3f": "GL.Color3",
    "Gl.glColor4d": "GL.Color4",
    "Gl.glColor4f": "GL.Color4",
    "Gl.glDeleteLists": "GL.DeleteLists",
    "Gl.glDeleteTextures": "GL.DeleteTextures",
    "Gl.glEnd": "GL.End",
    "Gl.glGenLists": "GL.GenLists",
    "Gl.glGenTextures": "GL.GenTextures",
    "Gl.glGetError": "GL.GetError",
    "Gl.glLoadIdentity": "GL.LoadIdentity",
    "Gl.glNormal3f": "GL.Normal3",
    "Gl.glOrtho": "GL.Ortho",
    "Gl.glPopMatrix": "GL.PopMatrix",
    "Gl.glPushMatrix": "GL.PushMatrix",
    "Gl.glTexCoord2d": "GL.TexCoord2",
    "Gl.glTexCoord2f": "GL.TexCoord2",
    "Gl.glVertex2d": "GL.Vertex2",
    "Gl.glVertex2f": "GL.Vertex2",
    "Gl.glVertex3f": "GL.Vertex3",
    "Gl.glTranslated": "GL.Translate",
    "Gl.glCallList": "GL.CallList",
    "Gl.glNewList": "GL.NewList",

    "Gl.glDepthMask\(Gl.GL_FALSE\);": "GL.DepthMask(false);",
    "Gl.glDepthMask\(Gl.GL_TRUE\);": "GL.DepthMask(true);",

    "Gl.glClear\(Gl.GL_DEPTH_BUFFER_BIT\);": "GL.Clear(ClearBufferMask.DepthBufferBit);",
    "Gl.glClear\(Gl.GL_COLOR_BUFFER_BIT \| Gl.GL_DEPTH_BUFFER_BIT\);": "GL.Clear(ClearBufferMask.ColorBufferBit | ClearBufferMask.DepthBufferBit);",
    "Gl.glBegin\(Gl.GL_POLYGON\);":       "GL.Begin(PrimitiveType.Polygon);",
    "Gl.glBegin\(Gl.GL_QUADS\);":         "GL.Begin(PrimitiveType.Quads);",
    "Gl.glBegin\(Gl.GL_QUAD_STRIP\);":    "GL.Begin(PrimitiveType.QuadStrip);",
    "Gl.glBegin\(Gl.GL_TRIANGLES\);":     "GL.Begin(PrimitiveType.Triangles);",
    "Gl.glBegin\(Gl.GL_TRIANGLE_STRIP\);":"GL.Begin(PrimitiveType.TriangleStrip);",

    "Gl.glCullFace\(Gl.GL_BACK\);": "GL.CullFace(CullFaceMode.Back);",
    "Gl.glCullFace\(Gl.GL_FRONT\);": "GL.CullFace(CullFaceMode.Front);",
    "Gl.glDepthFunc\(Gl.GL_LEQUAL\);": "GL.DepthFunc(DepthFunction.Lequal);",
    "Gl.glShadeModel\(Gl.GL_SMOOTH\);": "GL.ShadeModel(ShadingModel.Smooth);",

    "Gl.glDisable\(Gl.GL_ALPHA_TEST\);":    "GL.Disable(EnableCap.AlphaTest);",
    "Gl.glDisable\(Gl.GL_BLEND\);":         "GL.Disable(EnableCap.Blend);",
    "Gl.glDisable\(Gl.GL_COLOR_MATERIAL\);":"GL.Disable(EnableCap.ColorMaterial);",
    "Gl.glDisable\(Gl.GL_CULL_FACE\);":     "GL.Disable(EnableCap.CullFace);",
    "Gl.glDisable\(Gl.GL_DITHER\);":        "GL.Disable(EnableCap.Dither);",
    "Gl.glDisable\(Gl.GL_DEPTH_TEST\);":    "GL.Disable(EnableCap.DepthTest);",
    "Gl.glDisable\(Gl.GL_FOG\);":           "GL.Disable(EnableCap.Fog);",
    "Gl.glDisable\(Gl.GL_LIGHT0\);":        "GL.Disable(EnableCap.Light0);",
    "Gl.glDisable\(Gl.GL_LIGHTING\);":      "GL.Disable(EnableCap.Lighting);",
    "Gl.glDisable\(Gl.GL_TEXTURE_2D\);":    "GL.Disable(EnableCap.Texture2D);",

    "Gl.glEnable\(Gl.GL_ALPHA_TEST\);":    "GL.Enable(EnableCap.AlphaTest);",
    "Gl.glEnable\(Gl.GL_BLEND\);":         "GL.Enable(EnableCap.Blend);",
    "Gl.glEnable\(Gl.GL_COLOR_MATERIAL\);":"GL.Enable(EnableCap.ColorMaterial);",
    "Gl.glEnable\(Gl.GL_CULL_FACE\);":     "GL.Enable(EnableCap.CullFace);",
    "Gl.glEnable\(Gl.GL_DITHER\);":        "GL.Enable(EnableCap.Dither);",
    "Gl.glEnable\(Gl.GL_DEPTH_TEST\);":    "GL.Enable(EnableCap.DepthTest);",
    "Gl.glEnable\(Gl.GL_FOG\);":           "GL.Enable(EnableCap.Fog);",
    "Gl.glEnable\(Gl.GL_LIGHT0\);":        "GL.Enable(EnableCap.Light0);",
    "Gl.glEnable\(Gl.GL_LIGHTING\);":      "GL.Enable(EnableCap.Lighting);",
    "Gl.glEnable\(Gl.GL_TEXTURE_2D\);":    "GL.Enable(EnableCap.Texture2D);",

    "Gl.glMatrixMode\(Gl.GL_MODELVIEW\);": "GL.MatrixMode(MatrixMode.Modelview);",
    "Gl.glMatrixMode\(Gl.GL_PROJECTION\);": "GL.MatrixMode (MatrixMode.Projection);",

    "Gl.glBlendFunc\(Gl.GL_ZERO\, Gl.GL_ONE_MINUS_SRC_COLOR\);": "GL.BlendFunc(BlendingFactorSrc.Zero, BlendingFactorDest.OneMinusSrcColor);",
    "Gl.glBlendFunc\(Gl.GL_SRC_ALPHA\, Gl.GL_ONE\);": "GL.BlendFunc(BlendingFactorSrc.SrcAlpha, BlendingFactorDest.One);",
    "Gl.glBlendFunc\(Gl.GL_SRC_ALPHA\, Gl.GL_ONE_MINUS_SRC_ALPHA\);": "GL.BlendFunc(BlendingFactorSrc.SrcAlpha, BlendingFactorDest.OneMinusSrcAlpha);",
    
    "Gl.glBindTexture\(Gl.GL_TEXTURE_2D\,": "GL.BindTexture(TextureTarget.Texture2D,",

    "SetAlphaFunc\(Gl.GL_LESS\,":    "SetAlphaFunc((int)AlphaFunction.Less,",
    "SetAlphaFunc\(Gl.GL_GREATER\,": "SetAlphaFunc((int)AlphaFunction.Greater,",
    "SetAlphaFunc\(Gl.GL_EQUAL\,":   "SetAlphaFunc((int)AlphaFunction.Equal,",
}

def process_job(input_file, output_file):
    for line in open(input_file).readlines():
        for key in replace_dict:
            match = re.search("(.*)" + key + "(.*)", line) # E.g.
            if (match):
                print match.group(1) + replace_dict[key] + match.group(2)
                break
        if (not match):
            print line.rstrip()


def usage():
    print("Usage:")
    print("  %s -i input.cs -o output.cs " % sys.argv[0])
    print("")

def main():
    # parse command line options
    if len(sys.argv) != 5:
        usage()
        sys.exit()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["input=", "output="])
    except getopt.error, msg:
        # print help information and exit:
        usage()
        sys.exit()

    for o, a in opts:
        if o in ("-i", "--input"):
            input_file = a
        elif o in ("-o", "--output"):
            output_file = a
        else:
            usage()
            sys.exit()

    result = process_job(input_file, output_file)

    return result

if __name__ == '__main__':
    main()
