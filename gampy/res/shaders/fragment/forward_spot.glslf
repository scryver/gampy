#version 120

#include "forward_fragment.glslh"

uniform SpotLight R_spotLight;

vec4 CalcLightingEffect(vec3 normal, vec3 worldPosition)
{
    return CalcSpotLight(R_spotLight, normal, worldPosition);
}

#include "fragment_main.glslh"