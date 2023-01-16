# -*- coding: utf-8 -*-
"""Chart to PNG

Retrieve 'temphumi' database as DataFrame, group by time intervals.

chart_th get mariadb's data using Panda's method, so it uses environment variables to connect
to the database but this module wont use db.py on this project.

"""

import os
from datetime import datetime, timedelta
from loguru import logger
import dotenv

# from pandas import DataFrame, read_sql #Prolly a good idea to implement in raspberry pi....
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

    # Lower and upper bounds and set outliers to NaN in order to discard errors from adafruit_dht
    lb = rdf["temp"].quantile(0.01)
    ub = rdf["temp"].quantile(0.99)
    logger.debug(f"Handling temperature outliers values (Lower>{lb} & Upper<{ub})...")
    rdf = rdf[(rdf["temp"] > lb) & (rdf["temp"] < ub)]

    # Setting timestamp as index (DateTimeIndex)
    logger.debug("Setting 'time' field as index (DateTimeIndex)...")
    rdf.index = rdf["time"]

    # Grouping and naming aggregated columns
    logger.debug("Aggregate Mfig. Mean and Min values...")
    rdf = rdf.resample(tu)["temp", "humi"].agg(
        {"temp": [("Min C°", "min"), ("Avg C°", "mean"), ("Mfig.C°", "max")], "humi": [("Hum %", "mean")]}
    )

    # Flatten DataFrame
    logger.debug("Flattening DataFrame...")
    rdf.columns = rdf.columns.droplevel(0)

    logger.debug("Done! Ready to chart it...")
    return rdf


def plotting_df(df: pd.DataFrame, hours: int, tu: str, filename: str = "chart_th.png") -> None:
    logger.info("Plotting...")

    # Instead of go.Figure(), make_subplots create a figure with secondary axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Temperature
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Avg C°"],
        ),
        secondary_y=False,
    )

    # Humidity
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Hum %"],
        ),
        secondary_y=True,
    )

    fig.update_layout(autosize=False, width=500, height=800)  # todo: best resolution for mobil?
    fig.update_traces(connectgaps=True, showlegend=False)
    fig.update_yaxes(title="<b>Temperature</b> C°", secondary_y=False)
    fig.update_yaxes(title="<b>Humidity</b> %", secondary_y=True)
    fig.update_xaxes(title=None)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor="#e5ecf6", yaxis_range=[20, 40])

    if __name__ == "__main__":
        fig.show()

    fig.write_image(filename)

    logger.info("Done!")
    return None


def draw_chart(hours: int = 24, tu: str = "1H", filename: str = "chart_th.png") -> str:
    try:
        df = get_mariadb_data()
        df = resample_by_time(df, hours, tu)
        plotting_df(df, hours, tu, filename)

    except Exception as e:
        logger.error(
            f"""
            Somethng went wrong plotting the chart. The function receive these values:
            \n  hours: {hours}\n  time unit (tu): {tu}\n  Filename: {filename}
            
            Error:
            {e}
            """
        )
        raise e
        return False

    else:
        return filename


if __name__ == "__main__":
    draw_chart()
