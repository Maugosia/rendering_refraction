#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
out vec3 ambient;
uniform mat4 MVP;

vec3 light_source;

void main() {
    gl_Position = MVP * vec4(in_position, 1.0);
    ambient = abs(in_position); //get basic color of object, that will be transmitted to fragment shader
}

#elif defined FRAGMENT_SHADER

out vec4 f_color;
in vec3 ambient;

vec3 color;

void main()
{
    f_color = vec4(ambient, 1.0);
}
#endif