#version 330 core

layout (location=0) out vec4 fragColor;

in vec2 fragPos;

uniform float zoom;
uniform vec2 offset;
uniform float bound;

vec3 colors[6] = vec3[6](
    vec3(0,0,1),
    vec3(1,0,1),
    vec3(1,0,0),
    vec3(1,1,0),
    vec3(0,1,0),
    vec3(0,1,1)
);

vec3 colorize2(float f){
    int i = int(f);
    float k = f-i;
    return colors[i]*(1-k)+colors[i+1]*k;
}

vec2 square_complex_num(vec2 num){
    return vec2(num.x*num.x-num.y*num.y,2*num.x*num.y);
}

vec3 render_mandelbrot(vec2 c,int iterations){
    vec2 z = vec2(0,0);
    for(int i=0;i<iterations;i++){
        z = square_complex_num(z)+c;
        if(z.x*z.x+z.y*z.y>bound){
            return colorize2(float(i)/float(iterations)*6);
        }
    }
    return vec3(0,0,0);
}
void main(){
    vec3 color = render_mandelbrot(fragPos*zoom+offset,int(max(20*1/zoom,20)));
    fragColor = vec4(color,1.0);
}