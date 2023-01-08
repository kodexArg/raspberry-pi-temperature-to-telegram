import os
from datetime import datetime, timedelta
import dotenv
from loguru import logger
from sqlalchemy import create_engine
import pandas as pd

dotenv.load_dotenv()


def get_mariadb_data() -> pd.DataFrame:
    conn_str = f"mariadb+mariadbconnector://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}/rpi"
    engine = create_engine(conn_str)
    df = pd.read_sql(
        sql="SELECT time, temp, humi FROM temphumi ORDER BY time DESC LIMIT 90000",
        con=engine,
        # index_col="time",
    )
    return df


def resample_by_time(df: pd.DataFrame, hours: int = 24, tu: str = "30min") -> pd.DataFrame:
    dtnow = datetime.now()
    dtini = dtnow - timedelta(hours=hours)

    # Filtering by date range
    rdf = df[(df['time'] > dtini)]

    # Setting timestamp as index
    rdf.index = rdf['time']

    # Grouping by time interval (!!!)
    logger.debug(f'\nBEFORE\n{rdf}')
    rdf = rdf.resample(tu)['temp', 'humi'].agg(['min', 'mean', 'max'])
    logger.debug(f'\nAFTER\n\n{rdf}')
    return rdf


def plotting_df(df: pd.DataFrame):
    ax = df.plot(x="time", y="temp", kind="scatter", legend=True)

    ax.set_xlabel(None)
    ax.set_ylabel(None)

    ax.figure.savefig("demo.png")


if __name__ == "__main__":
    logger.info("Creating database connection and retreiving data...")
    df = get_mariadb_data()
    logger.info(f"{len(df.index)} rows loaded.")

    hours = 24
    tu = "1H"
    logger.info(f"Filtering by time ({hours} hours) and grouping by time unit ('{tu}')")
    df = resample_by_time(df)
    # logger.debug(f"\nResult:\n{df}")
