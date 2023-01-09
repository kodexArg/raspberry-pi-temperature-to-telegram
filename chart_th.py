# -*- coding: utf-8 -*-
"""
    Retrieve 'temphumi' database as DataFrame, group by time intervals and plot as PNG file
"""

import os
from datetime import datetime, timedelta
import dotenv
from loguru import logger
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# from pandas import DataFrame, read_sql #Prolly a good idea to implement in raspberry pi....

dotenv.load_dotenv()


def get_mariadb_data() -> pd.DataFrame:
    logger.info("Creating database connection and retreiving data...")
    conn_str = f"mariadb+mariadbconnector://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}/rpi"
    engine = create_engine(conn_str)
    df = pd.read_sql(
        sql="SELECT time, temp, humi FROM temphumi ORDER BY time DESC LIMIT 90000",
        con=engine,
    )
    logger.debug(f"{len(df.index)} rows loaded. Done!")
    return df


def resample_by_time(df: pd.DataFrame, hours: int = 24, tu: str = "1H") -> pd.DataFrame:
    logger.info(f"Filtering last {hours} hours and grouping by time unit ('{tu}')...")

    # Filtering by date range
    dtini = datetime.now() - timedelta(hours=hours)
    logger.debug(f"Filtering Dataframe by date > {dtini}")
    rdf = df[(df["time"] > dtini)]

    # Lower and upper bounds and set outliers to NaN (fix: changed to Mean)
    lb = rdf["temp"].quantile(0.01)
    ub = rdf["temp"].quantile(0.99)
    logger.debug(f"Handling temperature outliers values (Lower>{lb} & Upper<{ub})...")
    rdf = rdf[(rdf["temp"] > lb) & (rdf["temp"] < ub)]

    # Setting timestamp as index (DateTimeIndex)
    logger.debug("Setting 'time' as index...")
    rdf.index = rdf["time"]

    # Grouping and naming aggregated columns
    logger.debug("Resampling Dataframe and aggregate columns for Max, Mean and Min values...")
    rdf = rdf.resample(tu)["temp", "humi"].agg(
        {"temp": [("Min C°", "min"), ("Avg C°", "mean"), ("Max C°", "max")], "humi": [("Hum %", "mean")]}
    )

    # Flatten DataFrame
    logger.debug("Flattening DataFrame")
    rdf.columns = rdf.columns.droplevel(0)
    rdf.reset_index(inplace=True)

    logger.debug("Done!")
    return rdf


def plotting_df(df: pd.DataFrame, hours: int, tu: str) -> None:
    logger.info("Plotting...")
    
    #plt.figure(figsize=(5, 8))

    # sns.lineplot(df, x="time", y="Min C°", c="#B6E3E6")
    # sns.lineplot(df, x="time", y="Max C°", c="#B6E3E6")
    # plt.fill_between(df["time"], df["Min C°"], df["Max C°"], color="blue")
#    sns.set_palette("Set2")
    #sns.set_theme(style="darkgrid")
    ax = sns.lineplot(x=df['time'], y="Avg C°", data=df, err_style='bars')
    #ax.set_title(f"Avg Temperature | {tu}.")
    #ax.set_ylabel(None)
    #ax.set_xlabel(None)
    
    # plt.xticks(rotation=45)

    # plt.savefig("demo.png")
    plt.show()
    return None


if __name__ == "__main__":
    df = get_mariadb_data()
    df = resample_by_time(df, hours=24, tu="1H")
    plotting_df(df, hours=24, tu="1H")
