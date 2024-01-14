#version 330

#if defined VERTEX_SHADER

// Indices of refraction
const float Air = 1.0;
const float Glass = 1.51714;

// Air to glass ratio of the indices of refraction (Eta)
const float Eta = Air / Glass;

// see http://en.wikipedia.org/wiki/Refractive_index Reflectivity
const float R0 = ((Air - Glass) * (Air - Glass)) / ((Air + Glass) * (Air + Glass));

uniform mat4 MVP;
uniform mat4 u_modelMatrix;
uniform mat3 u_normalMatrix;
uniform vec4 u_camera;

in vec4 in_position;
in vec3 in_normal;

out vec3 v_reflection;
out vec3 v_refraction;
out float v_fresnel;

void main(void)
{
	// We calculate in world space.
	vec4 vertex = u_modelMatrix*vec4(in_position);
	gl_Position = MVP*vec4(in_position);
	vec3 incident = normalize(vec3(vertex-u_camera));

	// Assume incoming normal is normalized.
	vec3 normal = u_normalMatrix*in_normal;
	v_refraction = refract(incident, normal, Eta);
	v_reflection = reflect(incident, normal);

	// see http://en.wikipedia.org/wiki/Schlick%27s_approximation
	v_fresnel = R0 + (1.0 - R0) * pow((1.0 - dot(-incident, normal)), 5.0);


}

#elif defined FRAGMENT_SHADER

uniform samplerCube u_cubemap;

in vec3 v_refraction;
in vec3 v_reflection;
in float v_fresnel;

out vec4 fragColor;

void main(void)
{
	vec4 refractionColor = texture(u_cubemap, normalize(v_refraction));
	vec4 reflectionColor = texture(u_cubemap, normalize(v_reflection));
	fragColor = mix(refractionColor, reflectionColor, v_fresnel);
	fragColor = refractionColor;

}

#endif