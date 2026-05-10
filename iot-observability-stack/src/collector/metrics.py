from sensors.simulator import (
    simulate_sensor_data,
    simulate_monsoon_efficiency_metrics,
    simulate_water_stewardship_metrics,
    simulate_grid_carbon_metrics,
    simulate_governance_metrics,
)


def collect_temperature():
    data = simulate_sensor_data()
    return data['temperature']


def collect_humidity():
    data = simulate_sensor_data()
    return data['humidity']


def collect_pressure():
    data = simulate_sensor_data()
    return data['pressure']


def collect_monsoon_efficiency_metrics():
    return simulate_monsoon_efficiency_metrics()


def collect_water_stewardship_metrics():
    return simulate_water_stewardship_metrics()


def collect_grid_carbon_metrics():
    return simulate_grid_carbon_metrics()


def collect_governance_metrics():
    return simulate_governance_metrics()
