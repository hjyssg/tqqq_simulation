import os

# List of simple script files to delete relative to this script's directory
SIMPLE_SCRIPTS = [
    'Analysis_Script/After_Election.py',
    'Analysis_Script/After_NVDA_Earning.py',
    'Analysis_Script/After_bad_week.py',
    'Analysis_Script/Before_Election.py',
    'Analysis_Script/Quadruple_Witching_Day_Analysis.py',
    'Analysis_Script/buy_on_last_day_or_first_day.py',
    'Analysis_Script/chill_up_trend.py',
    'Analysis_Script/crazy_rise.py',
    'Analysis_Script/day_that_cpi_release.py',
    'Analysis_Script/find_good_uptrend.py',
    'Analysis_Script/find_most_dramatic_day.py',
    'Analysis_Script/find_quiet_days.py',
    'Analysis_Script/first_last_week.py',
    'Analysis_Script/how_common_is_correction.py',
    'Analysis_Script/invest_at_random_time.py',
    'Analysis_Script/nasdaq100_summer_returns_analysis.py',
    'Analysis_Script/really_bad_day.py',
    'Analysis_Script/really_bad_week.py',
    'Analysis_Script/statisitc_CAGR.py',
    'Analysis_Script/statistic_by_month.py',
    'Analysis_Script/statistic_specific_month.py',
    'Analysis_Script/strong_trend_vs_40_days_later.py',
    'Analysis_Script/three_years_growth.py',
    'Analysis_Script/top_rally_day.py',
    'Analysis_Script/week_that_cpi_release.py',
    'Analysis_Script/when_japan_crash.py',
    'Analysis_Script/when_japan_crash_how_spx_do.py',
]


def delete_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for rel_path in SIMPLE_SCRIPTS:
        file_path = os.path.join(base_dir, rel_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'Removed {file_path}')
        else:
            print(f'Skipped {file_path} (not found)')


if __name__ == '__main__':
    delete_files()
