#version 120

#include "sampling.glslh"

varying vec2 texCoord0;
varying vec3 worldPosition0;
varying mat3 tbnMatrix;

uniform vec3 R_ambient;
uniform vec3 C_eyePosition;
uniform sampler2D diffuse;
uniform sampler2D dispMap;

uniform float dispMapScale;
uniform float dispMapBias;

void main()
{
    vec3 directionToEye = normalize(C_eyePosition - worldPosition0);
    vec2 texCoords = CalcParallaxTexCoords(dispMap, tbnMatrix, directionToEye, texCoord0, dispMapScale, dispMapBias);

    gl_FragColor = texture2D(diffuse, texCoords.xy) * vec4(R_ambient, 1);
}
