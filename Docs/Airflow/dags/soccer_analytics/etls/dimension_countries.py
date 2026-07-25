import requests
import json
#import argparse
#import config
from datetime import date
import psycopg as pg # pyright: ignore[reportMissingImports]

file = open('/opt/airflow/dags/soccer_analytics/config.json')

args = json.load(file)

season = date.today().strftime("%Y")
league_id = '71'

query_round = f"""
    select distinct
         league_id
        ,league_name name
        ,league_type type
        ,country_name
        ,league_logo
        ,CURRENT_TIMESTAMP AT TIME ZONE 'UTC+3' AS created_at
        ,CURRENT_TIMESTAMP AT TIME ZONE 'UTC+3' AS updated_at
    from usr_landing.leagues
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_round)
results = cur.fetchall()

merge_statement = """
    MERGE INTO dimension.dim_countries AS dim
    USING (
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        ) 
    ) AS aux (
         league_id
        ,name
        ,type
        ,country_name
        ,league_logo
        ,created_at
        ,updated_at
    ) ON (dim.league_id = aux.league_id)
    WHEN MATCHED THEN
        UPDATE SET  name = aux.name
                    ,type = aux.type
                    ,country_name = aux.country_name
                    ,league_logo = aux.league_logo
                    ,updated_at = aux.updated_at
    WHEN NOT MATCHED THEN
        INSERT (league_id, name, type, country_name, league_logo, created_at, updated_at)
        VALUES (aux.league_id, aux.name, aux.type, aux.country_name, aux.league_logo, aux.created_at, aux.updated_at)
"""

cur.executemany(merge_statement, results)
conn.commit()
conn.close()