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
import plotly.express as px
import plotly.graph_objects as go


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
    print(rdf)

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


def plotting_df(df: pd.DataFrame, hours: int, tu: str, filename: str = "chart_th.png") -> None:
    logger.info("Plotting...")
    ax = px.line(df, x="time", y="Avg C°", title="Temperature C°")
    ax.update_traces(connectgaps=True, showlegend=False)
    ax.update_yaxes(title=None)
    ax.update_xaxes(title=None)
    ax.update_layout(margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor="#e5ecf6")
    if __name__ == "__main__()":
        ax.show()
    ax.update_layout(autosize=False, width=500, height=800)
    ax.write_image(filename)
    return None


def draw_chart(hours: int = 96, tu: str = "1H", filename: str = "chart.png") -> bool:
    try:
        df = get_mariadb_data()
        df = resample_by_time(df, hours=96, tu="2H")
        plotting_df(df, hours, tu, filename)
    except:
        logger.error(
            f"""
            Somethng went wrong plotting the chart. The function receive these values:
            \n  hours: {hours}\n  time unit (tu): {tu}\n  Filename: {filename}
            """
        )
        return False
    return True


if __name__ == "__main__":
    draw_chart()
