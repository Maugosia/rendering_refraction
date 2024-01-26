import moderngl_window as mglw
import moderngl
from pathlib import Path
from pyrr import Matrix44
from pyrr import Vector3


# tu się fajnie dziedziczy
class WindowTest(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (640, 480)
    resource_dir = (Path(__file__).parent / 'resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.load_program(path="shaders/shader_normals.glsl")
        self.texture = self.ctx.texture(self.wnd.size, 4)
        self.obj = self.load_scene('models/sphere.obj')
        # self.obj = self.load_scene('models/bunny.obj')
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.program)

        self.program_phong = self.load_program(path="shaders/shader_phong.glsl")
        self.texture = self.ctx.texture(self.wnd.size, 4)
        self.obj_phong = self.load_scene('models/sphere.obj')
        # self.obj_phong = self.load_scene('models/bunny.obj')
        self.vao_phong = self.obj_phong.root_nodes[0].mesh.vao.instance(self.program_phong)

        self.program_loc = self.load_program(path="shaders/shader_location.glsl")
        self.texture = self.ctx.texture(self.wnd.size, 4)
        self.obj_loc = self.load_scene('models/sphere.obj')
        # self.obj_loc = self.load_scene('models/bunny.obj')
        self.vao_loc = self.obj_loc.root_nodes[0].mesh.vao.instance(self.program_loc)

        self.init_shaders_variables()

    def init_shaders_variables(self):
        self.uniform_MVP = self.program['MVP']

        self.uniform_MVP_phong = self.program_phong['MVP_phong']
        self.uniform_color_fragments_phong = self.program_phong['color_body_part_phong']
        self.uniform_viewing_position_phong = self.program_phong['viewing_phong']

        self.uniform_MVP_loc = self.program_loc['MVP']

    def render(self, time, frametime):
        # Prepare context
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Define position of viewer
        vector = Vector3([-5.0, -5.0, 5.0])
        self.uniform_viewing_position_phong.write((vector.astype('f4')))

        # Define camera projection
        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (vector.x, vector.y, vector.z),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        # Normal test
        model = Matrix44.from_translation((0, -0, 0))
        model = model * Matrix44.from_x_rotation(0)
        model = model * Matrix44.from_scale((1.0, 1.0, 1.0))
        MVP = projection * lookat * model
        self.uniform_MVP.write(MVP.astype('f4'))
        self.vao.render()

        # Phong test
        vector = Vector3([0.9, 0.25, 0.25])
        self.uniform_color_fragments_phong.write(vector.astype('f4'))
        model = Matrix44.from_translation((5, -3, 0))
        model = model * Matrix44.from_x_rotation(0)
        model = model * Matrix44.from_scale((1.0, 1.0, 1.0))
        MVP = projection * lookat * model
        self.uniform_MVP_phong.write(MVP.astype('f4'))
        self.vao_phong.render()

        # Location test
        model = Matrix44.from_translation((5, 3, 0))
        model = model * Matrix44.from_x_rotation(0)
        model = model * Matrix44.from_scale((0.5, 0.5, 0.5))
        MVP = projection * lookat * model
        self.uniform_MVP_loc.write(MVP.astype('f4'))
        self.vao_loc.render()


if __name__ == "__main__":
    mglw.run_window_config(WindowTest)