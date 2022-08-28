import pandas as pd
import sqlite3 as sq


def load_cards_data() -> pd.DataFrame:
    df = pd.read_csv("data/Yugi_db_cleaned.csv")
    return df


def split_stats(row, secondary_stat: str):  # split ATK / DEF or LINK stats for analysis
    if row["Card type"] != "Monster" or row["ATK / {}".format(secondary_stat)] is None:
        return {"ATK": None, secondary_stat: None }
    stats = row["ATK / {}".format(secondary_stat)].split("/")
    return {
        "ATK": stats[0].strip() if "X" not in stats[0] else None,
        secondary_stat: stats[1].strip() if "X" not in stats[1] else None
    }


def transform_stats(df: pd.DataFrame) -> pd.DataFrame:
    df["ATK / DEF"].fillna("X / X", inplace=True)
    df["ATK / LINK"].fillna("X / X", inplace=True)

    secondary_stat = "DEF"

    df["ATK"] = df.apply(lambda row: split_stats(row, secondary_stat)["ATK"], axis=1)
    df["DEF"] = df.apply(lambda row: split_stats(row, secondary_stat)[secondary_stat], axis=1)

    secondary_stat = "LINK"

    df["ATK"] = df.apply(lambda row: split_stats(row, secondary_stat)["ATK"] if row["ATK"] is None else row["ATK"], axis=1)
    df["LINK"] = df.apply(lambda row: split_stats(row, secondary_stat)[secondary_stat], axis=1)

    df.drop("ATK / DEF", axis=1, inplace=True)
    df.drop("ATK / LINK", axis=1, inplace=True)

    return df


def insert_data_into_db(df: pd.DataFrame, db: str):
    conn = sq.connect('{}.sqlite'.format(db))
    df.to_sql("cards", conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    data = load_cards_data()
    transformed_data = transform_stats(data)

    insert_data_into_db(transformed_data, 'yugioh')
