#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

out vec3 normal;
out vec4 depthCoord;

uniform mat4 MVP;

void main() {
    gl_Position = MVP * vec4(in_position, 1.0);
    normal = in_normal;
    depthCoord = gl_Position;
}

#elif defined FRAGMENT_SHADER

uniform sampler2D depthMap;

in vec3 normal;
in vec4 depthCoord;

out vec4 fragColor;

void main()
{
    vec3 color = (1.0 + vec3(normal.z, normal.y, -normal.x))*0.5;
    float visibility = 1.0;
    if(texture(depthMap, depthCoord.xy).r > 0.9){
        visibility = 0.5;
    }
    fragColor = vec4(color, visibility);
}
#endif