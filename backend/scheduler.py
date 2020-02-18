from datetime import datetime, timedelta
import logging

import pandas as pd


data: pd.Series = pd.read_csv(
    "../data/renewData.csv",
    sep=";",
    parse_dates=["datelabel"],
    index_col="datelabel"
)


def schedule_task(earliest_start_time: datetime, deadline: datetime, prod_time: timedelta):
    """Returns the first datetime with the highest sum of green energy"""

    potential_start_times = get_potential_start_times(
        earliest_start_time,
        deadline - prod_time
    )
    renew_scores = {
        t: calc_renew_score(t, prod_time) for t in potential_start_times
    }
    res = max(renew_scores, key=renew_scores.get)
    logging.info(f"best renew score -> {res}: {renew_scores[res]}")
    return res


def get_potential_start_times(earliest_time: datetime, latest_time: datetime):
    num_of_points = (latest_time - earliest_time).total_seconds() / (60*15)
    return (earliest_time + timedelta(minutes=15*x) for x in range(int(num_of_points) + 1))


def calc_renew_score(start_time: datetime, prod_time: timedelta):
    vals = data[start_time:(start_time + prod_time)]
    return vals["%"].sum()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )

    a = schedule_task(
        datetime(year=2019, month=1, day=15, hour=10, minute=0),
        datetime(year=2019, month=1, day=15, hour=15, minute=0),
        timedelta(hours=2)
    )
    print(a)
