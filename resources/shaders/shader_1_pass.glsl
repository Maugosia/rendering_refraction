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

in vec3 normal;

out vec3 outNormal;

void main()
{
    outNormal = normal;
}
#endif