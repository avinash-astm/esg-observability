from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server
from collector.metrics import (
    collect_temperature,
    collect_humidity,
    collect_pressure,
    collect_monsoon_efficiency_metrics,
    collect_water_stewardship_metrics,
    collect_grid_carbon_metrics,
    collect_governance_metrics,
)
import time
import sys


def main():
    try:
        prometheus_reader = PrometheusMetricReader()
        meter_provider = MeterProvider(metric_readers=[prometheus_reader])
        metrics.set_meter_provider(meter_provider)

        try:
            start_http_server(8000)
            print("Prometheus metrics available at http://localhost:8000/metrics")
        except OSError as exc:
            print(f"Failed to start Prometheus HTTP server on port 8000: {exc}")
            raise

        meter = metrics.get_meter("iot-observability")

        temperature_gauge = meter.create_gauge("temperature", description="Current temperature in Celsius")
        humidity_gauge = meter.create_gauge("humidity", description="Current humidity in percentage")
        pressure_gauge = meter.create_gauge("pressure", description="Current pressure in hPa")

        pue_gauge = meter.create_gauge("pue", description="Power Usage Effectiveness")
        season_window_active_gauge = meter.create_gauge("season_window_active", description="Active seasonal window")
        ppue_gauge = meter.create_gauge("ppue", description="Cooling PUE")
        it_load_gauge = meter.create_gauge("it_load", description="IT load fraction")
        efficiency_error_budget_burn_rate_gauge = meter.create_gauge(
            "efficiency_error_budget_burn_rate",
            description="Efficiency error budget burn rate",
        )

        wue_gauge = meter.create_gauge("wue", description="Water Usage Effectiveness")
        rainwater_harvested_liters_gauge = meter.create_gauge(
            "rainwater_harvested_liters",
            description="Rainwater harvested in liters",
        )
        water_source_mix_gauge = meter.create_gauge(
            "water_source_mix",
            description="Water source mix share",
        )
        tanker_dependency_ratio_gauge = meter.create_gauge(
            "tanker_dependency_ratio",
            description="Tanker dependency ratio",
        )

        cue_gauge = meter.create_gauge("cue", description="Carbon Usage Effectiveness")
        re_fraction_gauge = meter.create_gauge("re_fraction", description="Renewable Energy fraction")
        dg_runtime_ratio_gauge = meter.create_gauge(
            "dg_runtime_ratio",
            description="Diesel generator runtime ratio",
        )
        carbon_aware_workload_heatmap_gauge = meter.create_gauge(
            "carbon_aware_workload_heatmap",
            description="Carbon-aware workload score for green windows",
        )

        brsr_core_kpi_completeness_ratio_gauge = meter.create_gauge(
            "brsr_core_kpi_completeness_ratio",
            description="BRSR Core KPI completeness ratio",
        )
        worker_hours_wbgt_above_32_gauge = meter.create_gauge(
            "worker_hours_wbgt_above_32",
            description="Worker hours above 32°C WBGT",
        )
        data_localisation_pct_gauge = meter.create_gauge(
            "data_localisation_pct",
            description="Data localisation percentage within Indian borders",
        )
        upcoming_filing_deadline_seconds_gauge = meter.create_gauge(
            "upcoming_filing_deadline_seconds",
            description="Seconds until upcoming regulatory filing deadlines",
        )

        while True:
            try:
                temperature = collect_temperature()
                humidity = collect_humidity()
                pressure = collect_pressure()

                monsoon_metrics = collect_monsoon_efficiency_metrics()
                water_metrics = collect_water_stewardship_metrics()
                carbon_metrics = collect_grid_carbon_metrics()
                governance_metrics = collect_governance_metrics()

                temperature_gauge.set(temperature)
                humidity_gauge.set(humidity)
                pressure_gauge.set(pressure)

                pue_gauge.set(monsoon_metrics['pue'])
                season_window_active_gauge.set(
                    1,
                    {
                        'season': monsoon_metrics['season'],
                        'status': 'active',
                    },
                )
                ppue_gauge.set(monsoon_metrics['ppue'])
                it_load_gauge.set(monsoon_metrics['it_load'])
                efficiency_error_budget_burn_rate_gauge.set(
                    monsoon_metrics['efficiency_error_budget_burn_rate']
                )

                wue_gauge.set(water_metrics['evaporative_wue'], {'system': 'evaporative'})
                wue_gauge.set(water_metrics['closed_loop_wue'], {'system': 'closed-loop'})
                rainwater_harvested_liters_gauge.set(
                    water_metrics['rainwater_harvested_liters']
                )
                for source, share in water_metrics['water_source_mix'].items():
                    water_source_mix_gauge.set(share, {'source': source})
                tanker_dependency_ratio_gauge.set(
                    water_metrics['tanker_dependency_ratio']
                )

                cue_gauge.set(carbon_metrics['cue'])
                re_fraction_gauge.set(carbon_metrics['re_fraction'])
                dg_runtime_ratio_gauge.set(carbon_metrics['dg_runtime_ratio'])
                for window, score in carbon_metrics['carbon_aware_workload_heatmap'].items():
                    carbon_aware_workload_heatmap_gauge.set(score, {'window': window})

                brsr_core_kpi_completeness_ratio_gauge.set(
                    governance_metrics['brsr_core_kpi_completeness_ratio']
                )
                worker_hours_wbgt_above_32_gauge.set(
                    governance_metrics['worker_hours_wbgt_above_32']
                )
                data_localisation_pct_gauge.set(
                    governance_metrics['data_localisation_pct']
                )
                for regulator, seconds in governance_metrics['upcoming_filing_deadline_seconds'].items():
                    upcoming_filing_deadline_seconds_gauge.set(
                        seconds,
                        {'regulator': regulator},
                    )

                print(
                    f"Collected: Temp={temperature:.2f}C, Hum={humidity:.2f}%, Press={pressure:.2f}hPa, "
                    f"PUE={monsoon_metrics['pue']:.3f}, season={monsoon_metrics['season']}, "
                    f"WUE_evap={water_metrics['evaporative_wue']:.3f}, RE={carbon_metrics['re_fraction']:.3f}, "
                    f"BRSR={governance_metrics['brsr_core_kpi_completeness_ratio']:.3f}"
                )

            except Exception as e:
                print(f"Error collecting or recording metrics: {e}")

            time.sleep(10)

    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error initializing the application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
