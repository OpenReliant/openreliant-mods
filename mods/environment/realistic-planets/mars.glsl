// Realistic Planets (planets.luau): Mars and its dust (haze.glsl): grains about 1.5 micrometres
// across, mixed through the lower air, which scatter strongly forward and absorb blue light, so the
// haze is tan. The mod's README gives the sources of the numbers.

#include "haze.glsl"

const RealisticPlanetsHaze marsHaze = RealisticPlanetsHaze(
    // Mars's equatorial radius, km, and its polar radius as a share of it (IAU).
    3396.2, 0.99411, 3396.2,
    // The dust's optical depth outside the dust storms, at the blue, green and red channels'
    // wavelengths, and the air's scale height, through which the dust is mixed.
    vec3(0.48, 0.49, 0.50),
    vec3(11.1),
    // No detached layer.
    vec3(0.0), 0.0, 1.0,
    // Its albedo, which falls toward blue, and the forward lobe and the nearly even one that the
    // sky's brightness by angle gives, with none of Rayleigh's, as the thin air scatters little.
    vec3(0.81, 0.90, 0.96),
    vec3(0.889), vec3(0.094), vec3(0.743), vec3(0.257),
    // No cloud tops: the dust's forward light is all in the haze.
    0.0, 0.6,
    // The phase angle of the texture's brightness, Hubble's of 2003; blue, green and red to the
    // texture's channels, at the texture's brightness, 0.39 of Mars's true brightness; and the
    // share of the haze's light that blooms.
    5.0,
    mat3(0.0, 0.0, 0.39, 0.0, 0.39, 0.0, 0.39, 0.0, 0.0),
    0.25);

void surface(inout Surface s, vec4 parameters, float time) {
    realisticPlanetsHaze(s, parameters, marsHaze);
}
