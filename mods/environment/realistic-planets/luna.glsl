// Realistic Planets (planets.luau): the Moon lit by McEwen's lunar-Lambert law, fitted to the
// Moon's photometry at every phase angle, as USGS's ISIS uses it. The texture holds
// the ground's albedo, and its normal map, made from LOLA's heights, holds its relief, so that the
// craters and mountains show along the terminator, and fade out toward the full Moon, as they do.
//
// The law mixes Lommel and Seeliger's law, 2 mu0 / (mu0 + mu), which lights a dusty surface evenly
// to its edge at full Moon, with Lambert's, mu0, by a share L of the phase angle in degrees, where
// mu0 and mu are the cosines of the sun's and the view's angles from the normal:
// L = 1 - 0.019 phase + 0.000242 phase^2 - 0.00000146 phase^3 (A. S. McEwen, 1996). Past about 103
// degrees L would turn negative and darken the crescent away, so it's held at 0 there, Lambert's
// law.

// The coefficients of L, by the phase angle in degrees and its square and cube.
const vec3 lunaLambertShare = vec3(-0.019, 0.000242, -0.00000146);

void surface(inout Surface s, vec4 parameters, float time) {
    if (dot(s.normal, s.normal) < 0.5) return;
    float mu0 = max(dot(s.normal, s.toSun), 0.0);
    float mu = max(dot(s.normal, s.toEye), 0.0);
    float phase = degrees(acos(clamp(dot(s.toSun, s.toEye), -1.0, 1.0)));
    float share = max(1.0 + dot(lunaLambertShare, vec3(phase, phase * phase, phase * phase * phase)), 0.0);
    s.sunlight = vec3(mu0 > 0.0 ? 2.0 * share * mu0 / (mu0 + mu) + (1.0 - share) * mu0 : 0.0);
}
