#version 330

#if defined VERTEX_SHADER

uniform mat4 MVP;
//uniform mat4 u_modelMatrix;

in vec4 in_position;

out vec3 v_ray;

void main(void)
{
	v_ray = normalize(in_position.xyz);
	gl_Position = MVP*in_position;
}

#elif defined FRAGMENT_SHADER


uniform samplerCube u_cubemap;
in vec3 v_ray;
out vec4 fragColor;

void main(void)
{
	fragColor = texture(u_cubemap, v_ray);
}

#endif