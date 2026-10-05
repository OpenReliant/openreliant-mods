-- The Viper Mk II's records: a light, fast gunfighter. It outruns and outturns every fighter of the
-- game, carries light shields over a strong hull, and fires two kinetic guns that hit harder than
-- the Predator's lasers, with the energy to keep firing.

local records = require("openreliant.records")

local viper = records.ships["viper:viper"]
viper.max_speed = 420
viper.inertia = 0.78
viper.yaw_rate = 0.11
viper.yaw_inertia = 0.8
viper.pitch_rate = 0.11
viper.pitch_inertia = 0.8
viper.roll_rate = 0.18
viper.roll_inertia = 0.85
viper.shield_power = 8
viper.armor_class = 14
viper.afterburner_fuel = 160
viper.gun_energy = 200
viper.gun_recharge = 7

local kew = records.guns["viper:kew"]
kew.range = 280
kew.speed = 1800
kew.damage.shield = 10
kew.damage.hull = 13
kew.fire_rate = 9
kew.shot_energy = 2.5
