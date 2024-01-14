import moderngl_window as mglw
import moderngl
from pathlib import Path
from pyrr import Matrix44, Matrix33
from pyrr import Vector3
from math import pi


class WindowSkybox(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (900, 600)
    resource_dir = (Path(__file__).parent / 'resources').resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initialize camera position
        self.vector_viewer = Vector3([0.0, 0.0, 0.0])
        self.vector_lookat = Vector3([1.0, 0.0, 0.0])

        # SKYBOX initialization
        self.program_skybox = self.load_program(path="shaders/shader_skybox.glsl")
        self.obj_skybox = self.load_scene('models/skybox.obj')
        self.vao_skybox = self.obj_skybox.root_nodes[0].mesh.vao.instance(self.program_skybox)
        self.texture_skybox = self.load_texture_cube(pos_x='textures/front.jpg',
                                                     pos_y='textures/top.jpg',
                                                     pos_z='textures/left.jpg',
                                                     neg_x='textures/back.jpg',
                                                     neg_y='textures/bottom.jpg',
                                                     neg_z='textures/right.jpg')
        self.sampler_skybox = self.ctx.sampler(texture=self.texture_skybox)

        # PHONG initialization
        self.program_phong = self.load_program(path="shaders/shader_phong.glsl")
        self.obj_phong = self.load_scene('models/sphere.obj')
        self.vao_phong = self.obj_phong.root_nodes[0].mesh.vao.instance(self.program_phong)

        # LOCALIZATION initialization
        self.program_loc = self.load_program(path="shaders/shader_location.glsl")
        self.obj_loc = self.load_scene('models/sphere.obj')
        self.vao_loc = self.obj_loc.root_nodes[0].mesh.vao.instance(self.program_loc)

        # REFRACTION ball initialization
        self.program_glass = self.load_program(path="shaders/shader_glass.glsl")
        self.obj_glass = self.load_scene('models/sphere.obj')
        self.vao_glass = self.obj_glass.root_nodes[0].mesh.vao.instance(self.program_glass)

        self.init_shaders_variables()

    def init_shaders_variables(self):

        # initialize skybox variables
        self.uniform_MVP_skybox = self.program_skybox['MVP']
        self.program_skybox["u_cubemap"].write(self.texture_skybox.read(face=0))

        # initialize phong ball variables
        self.uniform_MVP_phong = self.program_phong['MVP_phong']
        self.uniform_color_fragments_phong = self.program_phong['color_body_part_phong']
        self.uniform_viewing_position_phong = self.program_phong['viewing_phong']

        # initialize localization ball
        self.uniform_MVP_loc = self.program_loc['MVP']

        # initialize glass ball variables
        self.uniform_MVP_glass = self.program_glass['MVP']
        self.uniform_model_mat_glass = self.program_glass['u_modelMatrix']
        self.uniform_normal_mat_glass = self.program_glass['u_normalMatrix']
        self.uniform_camera_pos_glass = self.program_glass['u_camera']
        self.program_glass["u_cubemap"].write(self.texture_skybox.read(face=0))

    def render(self, time, frametime):
        # Prepare context
        self.sampler_skybox.use(location=0)
        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Define camera projection
        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (self.vector_viewer.x, self.vector_viewer.y, self.vector_viewer.z),  # where camera is standing
            (self.vector_lookat.x, self.vector_lookat.y, self.vector_lookat.z),  # where camera is looking
            (0.0, 1.0, 0.0),                                                     # orientation of camera
        )

        # skybox render
        model = Matrix44.from_translation((0, 0, 0))
        model = model * Matrix44.from_x_rotation(0)
        model = model * Matrix44.from_scale((200.0, 200.0, 200.0))
        MVP = projection * lookat * model
        self.uniform_MVP_skybox.write(MVP.astype('f4'))
        self.vao_skybox.render()

        # Phong ball render
        color = Vector3([0.9, 0.25, 0.25])
        self.uniform_color_fragments_phong.write(color.astype('f4'))
        model = Matrix44.from_translation((10, 0, -3))
        model = model * Matrix44.from_x_rotation(0)
        model = model * Matrix44.from_scale((1.0, 1.0, 1.0))
        MVP = projection * lookat * model
        self.uniform_MVP_phong.write(MVP.astype('f4'))
        self.uniform_viewing_position_phong.write((self.vector_viewer.astype('f4')))
        self.vao_phong.render()

        # Location ball render
        model = Matrix44.from_translation((10, 0, 3))
        model = model * Matrix44.from_x_rotation(0)
        model = model * Matrix44.from_scale((1, 1, 1))
        MVP = projection * lookat * model
        self.uniform_MVP_loc.write(MVP.astype('f4'))
        self.vao_loc.render()

        #  glass render
        model = Matrix44.from_translation((10, 0, 0))
        model = model * Matrix44.from_x_rotation(0)
        self.uniform_normal_mat_glass.write(Matrix33.from_matrix44(model).astype('f4'))
        model = model * Matrix44.from_scale((1, 1, 1))
        MVP = projection * lookat * model
        self.uniform_MVP_glass.write(MVP.astype('f4'))
        self.uniform_model_mat_glass.write(model.astype('f4'))
        self.uniform_camera_pos_glass.write(self.vector_viewer.astype('f4'))
        self.vao_glass.render()

    def mouse_position_event(self, x, y, dx, dy):
        print("Mouse position:", x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        print("Mouse drag:", x, y, dx, dy)
        rot_matrix = Matrix44.from_y_rotation(-dx / 300)

        diff = self.vector_lookat - self.vector_viewer

        if self.vector_lookat[0] < 0:
            rot_up_matrix_1 = Matrix44.from_z_rotation(+dy / 600)
        else:
            rot_up_matrix_1 = Matrix44.from_z_rotation(-dy / 600)
        if self.vector_lookat[2] < 0:
            rot_up_matrix_2 = Matrix44.from_x_rotation(-dy / 600)
        else:
            rot_up_matrix_2 = Matrix44.from_x_rotation(dy / 600)

        new_diff = rot_up_matrix_2 * rot_up_matrix_1 * rot_matrix * diff
        self.vector_lookat = self.vector_viewer + new_diff

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        diff = self.vector_lookat - self.vector_viewer
        self.vector_viewer = self.vector_viewer + diff*y_offset/2
        self.vector_lookat = self.vector_lookat + diff*y_offset/2
        print("Mouse wheel:", x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))


if __name__ == "__main__":
    mglw.run_window_config(WindowSkybox)
