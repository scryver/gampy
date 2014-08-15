#version 330

in vec2 texCoord0;

out vec4 fragColor;

uniform vec3 color;
uniform sampler2D sampler;

void main()
{
    vec4 textureColor = texture(sampler, texCoord0.xy);
    vec4 baseColor = vec4(color, 1);

    if (textureColor != vec4(0, 0, 0, 1))
        baseColor *= textureColor;
        
    fragColor = baseColor;
}
