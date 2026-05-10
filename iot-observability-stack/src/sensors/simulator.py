import datetime
import random


def simulate_sensor_data():
    temperature = random.uniform(20.0, 30.0)  # Simulate temperature in Celsius
    humidity = random.uniform(30.0, 70.0)      # Simulate humidity in percentage
    pressure = random.uniform(950.0, 1050.0)   # Simulate pressure in hPa

    return {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure
    }


def current_season():
    month = datetime.datetime.utcnow().month
    if 3 <= month <= 5:
        return 'pre-monsoon'
    if 6 <= month <= 9:
        return 'monsoon'
    return 'winter'


def simulate_monsoon_efficiency_metrics():
    season = current_season()
    base_pue = {
        'pre-monsoon': 1.25,
        'monsoon': 1.35,
        'winter': 1.15
    }[season]
    pue = round(min(max(random.gauss(base_pue, 0.05), 1.0), 1.8), 3)

    it_load = round(min(max(random.gauss(0.75, 0.12), 0.35), 1.0), 3)
    ppue = round(min(max(random.gauss(0.35, 0.05), 0.2), 0.6), 3)
    error_budget_burn_rate = round(min(max(random.random() * 1.0, 0.0), 1.0), 3)

    return {
        'season': season,
        'pue': pue,
        'it_load': it_load,
        'ppue': ppue,
        'efficiency_error_budget_burn_rate': error_budget_burn_rate
    }


def simulate_water_stewardship_metrics():
    evaporative_wue = round(min(max(random.gauss(0.75, 0.1), 0.4), 1.2), 3)
    closed_loop_wue = round(min(max(random.gauss(0.25, 0.05), 0.15), 0.45), 3)
    rainwater_harvested_liters = round(random.uniform(5000.0, 24000.0), 1)

    stp = random.uniform(70.0, 85.0)
    municipal = random.uniform(0.0, min(40.0, 100.0 - stp))
    groundwater = round(max(0.0, 100.0 - stp - municipal), 1)
    municipal = round(municipal, 1)
    stp = round(stp, 1)

    tanker_dependency_ratio = round(min(max(random.random() * 0.25, 0.0), 0.35), 3)

    return {
        'evaporative_wue': evaporative_wue,
        'closed_loop_wue': closed_loop_wue,
        'rainwater_harvested_liters': rainwater_harvested_liters,
        'water_source_mix': {
            'municipal': municipal,
            'stp_recycled': stp,
            'groundwater': groundwater
        },
        'tanker_dependency_ratio': tanker_dependency_ratio
    }


def simulate_grid_carbon_metrics():
    cue = round(min(max(random.gauss(0.48, 0.08), 0.25), 0.9), 3)
    re_fraction = round(min(max(random.gauss(0.52, 0.12), 0.2), 0.95), 3)
    dg_runtime_ratio = round(min(max(random.gauss(0.03, 0.02), 0.0), 0.12), 3)

    windows = {
        'early_morning': round(min(max(random.gauss(0.7, 0.15), 0.0), 1.0), 3),
        'daytime': round(min(max(random.gauss(0.45, 0.2), 0.0), 1.0), 3),
        'evening': round(min(max(random.gauss(0.55, 0.18), 0.0), 1.0), 3),
        'night': round(min(max(random.gauss(0.8, 0.1), 0.0), 1.0), 3)
    }

    return {
        'cue': cue,
        're_fraction': re_fraction,
        'dg_runtime_ratio': dg_runtime_ratio,
        'carbon_aware_workload_heatmap': windows
    }


def simulate_governance_metrics():
    brsr_ratio = round(min(max(random.gauss(0.85, 0.1), 0.5), 1.0), 3)
    worker_hours_wbgt = round(min(max(random.gauss(3.5, 2.0), 0.0), 12.0), 2)
    data_localisation_pct = round(min(max(random.gauss(92.0, 5.0), 70.0), 100.0), 1)

    now = datetime.datetime.utcnow()
    deadlines = {
        'BEE PAT': int((now + datetime.timedelta(days=random.randint(15, 90))).timestamp() - now.timestamp()),
        'CPCB emissions': int((now + datetime.timedelta(days=random.randint(7, 60))).timestamp() - now.timestamp()),
        'SPCB noise': int((now + datetime.timedelta(days=random.randint(10, 80))).timestamp() - now.timestamp())
    }

    return {
        'brsr_core_kpi_completeness_ratio': brsr_ratio,
        'worker_hours_wbgt_above_32': worker_hours_wbgt,
        'data_localisation_pct': data_localisation_pct,
        'upcoming_filing_deadline_seconds': deadlines
    }
