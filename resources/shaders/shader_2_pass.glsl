#version 330

//#if defined VERTEX_SHADER
//
//in vec3 in_position;
//in vec3 in_normal;
//
//out vec3 normal;
//out vec4 depthCoord;
//
//uniform mat4 MVP;
//
//void main() {
//    gl_Position = MVP * vec4(in_position, 1.0);
//    normal = in_normal;
//    depthCoord = gl_Position;
//}
//
//#elif defined FRAGMENT_SHADER
//
//uniform sampler2D depthMap;
//
//in vec3 normal;
//in vec4 depthCoord;
//
//out vec4 fragColor;
//
//void main()
//{
//    vec3 color = (1.0 + vec3(normal.z, normal.y, -normal.x))*0.5;
//    float visibility = 1.0;
//    if(texture(depthMap, depthCoord.xy).r > 0.9){
//        visibility = 0.5;
//    }
//    fragColor = vec4(color, visibility);
//}
//#endif
#if defined VERTEX_SHADER


in vec3 in_normal;
out vec3 normal;
out vec4 depthCoord;

uniform mat4 MVP;

// Indices of refraction
const float Air = 1.0;
const float Glass = 1.51714;

// Air to glass ratio of the indices of refraction (Eta)
const float Eta = Air / Glass;

// see http://en.wikipedia.org/wiki/Refractive_index Reflectivity
const float R0 = ((Air - Glass) * (Air - Glass)) / ((Air + Glass) * (Air + Glass));

//uniform mat4 MVP;
uniform mat4 u_modelMatrix;
//uniform mat3 u_normalMatrix;
uniform vec4 u_camera;

in vec4 in_position;
//in vec3 in_normal;

out vec3 v_reflection;
out vec3 v_refraction;
out float v_fresnel;

void main() {

    vec4 vertex = u_modelMatrix*vec4(in_position);
    gl_Position  = MVP * vec4(in_position);
    vec3 incident = normalize(vec3(vertex-u_camera));
    normal = in_normal;
    depthCoord = gl_Position;
    v_refraction = refract(incident, normal, Eta);
	v_reflection = reflect(incident, normal);
}

#elif defined FRAGMENT_SHADER

uniform sampler2D depthMap;
uniform sampler2D nearbyGeometryMap;
uniform samplerCube environmentMap;

in vec3 in_normal;
in vec4 in_depthCoord;

out vec4 fragColor;
out vec3 v_reflection;
out vec3 v_refraction;
out float v_fresnel;

void main()
{
    float depthValue = texture(depthMap, in_depthCoord.xy).r;
    vec3 nearbyGeometryInfo = texture(nearbyGeometryMap, in_depthCoord.xy).rgb;

    if (nearbyGeometryInfo == vec3(0.0)) {
        vec3 T2Vec = normalize(vec3(0.0, 0.0, 1.0));
        vec3 PgeomColor = texture(environmentMap, T2Vec).rgb;
        fragColor = vec4(PgeomColor, 1.0);
    } else {

        vec3 T2Vec = normalize(vec3(0.0, 0.0, 1.0));
        vec3 normalVector = normalize(in_normal);  // normal passed from the vertex shader
        float refractiveIndex = 1.5;

        vec4 refractionColor = texture(environmentMap, normalize(v_refraction));
        vec4 reflectionColor = texture(environmentMap, normalize(v_reflection));
        fragColor = mix(refractionColor, reflectionColor, v_fresnel);
        fragColor = refractionColor;
    }
}
#endif
