from datetime import datetime
import os
from superset.utils.date_parser import get_since_until
from dotenv import load_dotenv

load_dotenv()


def get_analysis_period_boundaries(time_range=None):
    print("Time range:", time_range)
    if time_range!='No filter':
        print("#############################################")
        return get_since_until(time_range=time_range)
    
    print("No filter applied !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return (
        datetime(1900, 1, 1),
        datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    )

def get_growth_analysis_periods_boundaries(time_range=None):

    if time_range == 'No filter':
        time_range = 'Last month' # Replace by 'Last month'
        print(f"No period selected as current period, so automatically applied'{time_range}' as current period")
    
    current_period_start, current_period_end = get_analysis_period_boundaries(time_range=time_range)

    analysis_period_duration = current_period_end - current_period_start

    previous_period_end = current_period_start
    previous_period_start = previous_period_end - analysis_period_duration
    # print(analysis_period_duration)

    return previous_period_start, previous_period_end, current_period_start, current_period_end

SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY")
FEATURE_FLAGS = {'ENABLE_TEMPLATE_PROCESSING':True}

JINJA_CONTEXT_ADDONS = {
    'get_analysis_period_boundaries':get_analysis_period_boundaries,
    'get_growth_analysis_periods_boundaries':get_growth_analysis_periods_boundaries
    }



