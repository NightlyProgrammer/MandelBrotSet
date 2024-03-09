import pygame
import moderngl as mgl
import numpy as np
from sys import exit
#use fragcoords for not converging pixels as uv for iamge
class App:
    def __init__(self,WINDOW_SIZE):
        self.SCREEN_SIZE = WINDOW_SIZE
        self.aspect_ratio = WINDOW_SIZE[1]/WINDOW_SIZE[0]
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION,3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION,3)
        pygame.display.set_mode(WINDOW_SIZE,pygame.DOUBLEBUF|pygame.OPENGL)
        self.ctx = mgl.create_context()
        self.clock = pygame.time.Clock()
        self.vbo = self.ctx.buffer(np.array([
            -1,1,    1,1,
            -1,-1,   1,-1,
        ],dtype="f4"))
        self.program = self.read_program("shaders","mandelbrot")
        self.vao = self.ctx.vertex_array(self.program,[(self.vbo,"2f","in_position")])
    
    """def convert_surface_to_texture(self,surf):
        texture = pygame.transform.flip(surf,flip_x=False,flip_y=True)#flip on y to convert to opengl coordinate system
        texture = self.ctx.texture(size=texture.get_size(),components=3,#3 color values(r,g,b)
                                   data=pygame.image.tostring(texture,'RGB'))
        return texture"""

    def read_program(self,path,name):
        vert_name,frag_name = name.split('|')[0],name.split('|')[-1]
        with open(f"{path}/{vert_name}.vert","r") as file:
            vert_file_data = file.read()
        with open(f"{path}/{frag_name}.frag","r") as file:
            frag_file_data = file.read()

        return self.ctx.program(vertex_shader=vert_file_data,fragment_shader=frag_file_data)
    
    def render(self):
        self.ctx.clear(0,0,0)
        self.vao.render(mode=mgl.TRIANGLE_STRIP)

    def destroy(self):
        self.vbo.release()
        self.program.release()
        self.vao.release()
        self.ctx.release()
        pygame.quit()
        exit()
    
    def offset_input(self,delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.offset[1] += self.speed*delta*self.zoom
        elif keys[pygame.K_s]:
            self.offset[1] -= self.speed*delta*self.zoom
        if keys[pygame.K_a]:
            self.offset[0] -= self.speed*delta*self.zoom
        elif keys[pygame.K_d]:
            self.offset[0] += self.speed*delta*self.zoom
        
        if keys[pygame.K_PLUS]:
            self.diverge_bound += 0.01*delta
        elif keys[pygame.K_MINUS]:
            self.diverge_bound -= 0.01*delta

    def run(self):
        self.zoom = 1
        self.offset = [0,0]
        self.speed = 0.1*3
        delta = 0
        self.diverge_bound = 2

        self.program["aspect_ratio"] = self.aspect_ratio
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.destroy()                

                elif event.type == pygame.MOUSEWHEEL:
                    self.zoom += event.y*delta*0.001*self.zoom

            self.offset_input(delta)
            self.program["zoom"] = self.zoom
            self.program["offset"] = ((self.offset[0])/self.SCREEN_SIZE[0],(self.offset[1])/self.SCREEN_SIZE[1])
            
            self.program["bound"] = self.diverge_bound**2
            
            self.render()
            pygame.display.flip()

            pygame.display.set_caption(f"FPS: {round(self.clock.get_fps())},ZOOM: {round(self.zoom,1)},Bound Number:{round(self.diverge_bound,1)},Offset{self.offset}")
            delta = self.clock.tick(30)
if __name__ == '__main__':
    app = App((1280,720))
    app.run()