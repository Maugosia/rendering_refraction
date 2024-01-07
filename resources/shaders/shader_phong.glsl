#version 330

#if defined VERTEX_SHADER

//position and orientation of object-part
in vec3 in_position;
in vec3 in_normal;

//calculated directions will be passed to a fragment shader
out vec3 ambient;
out vec3 position;
out vec3 normal;
out vec3 light_direction;
out vec3 light_direction_reflected;
out vec3 viewing_direction;

//uniform - ambient color of body part
uniform vec3 color_body_part_phong;
//uniform - camera position
uniform vec3 viewing_phong;
//uniform - mvp matrice
uniform mat4 MVP_phong;

vec3 light_source;

void main() {
    gl_Position = MVP_phong * vec4(in_position, 1.0);

    //get basic color of object, that will be transmitted to fragment shader
    ambient = color_body_part_phong;

    //normal and position directions are passed to fragment shader without a change
    normal = in_normal;
    position = in_position;

    //set lightsource direction
    light_source = vec3(-15, 15, 3.0);

    //calculate normal vector representing light direction at this fragment
    light_direction = normalize(light_source - in_position);
    //calculate reflected light vector
    light_direction_reflected = reflect(light_direction, in_normal);
    //calculate direction at witch object is observed
    viewing_direction = normalize(viewing_phong - in_position);
}

#elif defined FRAGMENT_SHADER

out vec4 f_color;

in vec3 ambient;
in vec3 light_direction;
in vec3 position;
in vec3 normal;
in vec3 viewing_direction;
in vec3 light_direction_reflected;

uniform vec3 color_body_part;
uniform vec3 viewing;

//internal parameters
float Kd = 0.35;
float Ks = 0.65;
float n_power = 50;
float diffuse;
float specular;
vec3 color;

void main()
{
    //calculate diffuse component based on normal vector direction and direction of light
    diffuse = Kd * dot(normal, light_direction);
    //calculate specular component based on reflected light direction and direction of viewing
    specular = Ks * pow(dot(light_direction_reflected, viewing_direction), n_power);
    //combine components into one color for fragmaent
    color = vec3(ambient.x + diffuse + specular, ambient.y + diffuse + specular, ambient.z + diffuse + specular);

    f_color = vec4(color, 1.0);

}
#endif