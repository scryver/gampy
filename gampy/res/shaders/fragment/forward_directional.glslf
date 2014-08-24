#version 120

#include "forward_fragment.glslh"

uniform DirectionalLight R_directionalLight;

vec4 CalcLightingEffect(vec3 normal, vec3 worldPosition)
{
    return CalcDirectionalLight(R_directionalLight, normal, worldPosition);
}

#include "fragment_main.glslh"