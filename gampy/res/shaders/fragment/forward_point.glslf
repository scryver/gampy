#version 120

#include "forward_fragment.glslh"

uniform PointLight R_pointLight;

vec4 CalcLightingEffect(vec3 normal, vec3 worldPosition)
{
    return CalcPointLight(R_pointLight, normal, worldPosition);
}

#include "fragment_main.glslh"