#version 330 core

layout (location = 0) in vec2 in_position;

out vec2 fragPos;

uniform float aspect_ratio;

void main(){
    fragPos = in_position*vec2(1,aspect_ratio);
    gl_Position = vec4(in_position,0,1.0);
}