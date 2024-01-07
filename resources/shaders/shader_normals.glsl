#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
out vec3 normal;

uniform mat4 MVP;

void main() {
    gl_Position = MVP * vec4(in_position, 1.0);

    normal = in_normal;
}

#elif defined FRAGMENT_SHADER

out vec4 f_color;
in vec3 normal;

vec3 color;

void main()
{
    color = (1.0 + vec3(normal.z, normal.y, -normal.x))*0.5;

    f_color = vec4(color, 1.0);

}
#endif