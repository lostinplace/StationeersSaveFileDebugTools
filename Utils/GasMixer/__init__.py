
# https://physics.stackexchange.com/questions/217303/speed-of-spontaneous-mixing-of-different-gases





from collections import namedtuple
from math import sqrt, pi
from scipy.constants import Boltzmann, gas_constant, atomic_mass, Avogadro

co2_specific_heat_capacity_J_per_g = 203
co2_molar_mass = 44.0095 #g/mol
co2_atomic_mass = co2_molar_mass * atomic_mass
co2_thermal_speed_coefficient = sqrt(3*Boltzmann/co2_atomic_mass)


Gas = namedtuple('Gas', 'formula moles')
AtmosphericVolume = namedtuple('AtmosphericVolume', 'height width depth composition total_moles energy '
                                                    'mean_particle_radius total_molar_mass')
GasStats = namedtuple('GasStats', 'molar_mass atomic_mass specific_heat_capacity '
                                  'thermal_speed_coefficient particle_radius_in_nm, molar_radius_squared ')

CO2_Stats = GasStats(co2_molar_mass, co2_atomic_mass, co2_specific_heat_capacity_J_per_g,
                     co2_thermal_speed_coefficient, 0.33, 0.33**2 * Avogadro)


def get_molar_surface_area(particle_radius_in_nm):
    from scipy.constants import Avogadro
    nm_to_m_conversion = 10**-9


one_third_pi = pi/3


def volume_of_combined_cones(r1, r2, height):
    cofactor = one_third_pi * height
    sum = r1 * r1 + r2 * r2
    return cofactor * sum


def combine_atmospheric_volumes(volume_a:AtmosphericVolume, volume_b:AtmosphericVolume, time_in_seconds):
    for gas in volume_a:
        gas_stats = CO2_Stats

        # get transiting particles a->b

        # what proportion of the volume's gas contents is this gas?
        gas_mass = gas_stats.molar_mass * gas.moles
        proportional_mass = gas_mass / volume_a.total_molar_mass
        gas_energy = volume_a.energy * proportional_mass

        # given the mass of this gas contents, and the energy applied to it, what is the temperature of the gas?
        # △T_k (0 to temperature in K) = mass * heat capacity/ joules
        # https://sciencing.com/calculate-joules-heat-8205329.html

        gas_temperature = gas_stats.specific_heat_capacity * gas_mass / gas_energy

        gas_temperature_root = sqrt(gas_temperature)

        RMS_thermal_speed = gas_stats.thermal_speed_coefficient * gas_temperature_root #m/s
        distance_traveled_in_t = RMS_thermal_speed * time_in_seconds
        max_proportion_of_volume_a_travelled = distance_traveled_in_t/volume_a.depth
        particles_affected = gas.moles * max_proportion_of_volume_a_travelled

        particles_transiting = particles_affected / 4

        # get probability of collision
        max_proportion_of_volume_b_travelled = distance_traveled_in_t/volume_b.depth





        print(particles_transiting)

    