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
    SELECT
        CAST(league_id AS INT) league_id,
        CAST(league_season AS INT) league_season,
        CAST(REPLACE(league_round, 'Regular Season - ', '') AS INT) league_round,
        CAST(MIN(fixture_date) AS TIMESTAMP ) - INTERVAL '3' HOUR start_round_date,
        CAST(MAX(fixture_date) AS TIMESTAMP ) - INTERVAL '3' HOUR end_round_date,
        COUNT(CASE WHEN fixture_status_short = 'FT' THEN 1 END) QTD_FT_MATCHES,
        COUNT(CASE WHEN fixture_status_short != 'FT' THEN 1 END) QTD_UNPLAYED_MATCHES,
        CURRENT_TIMESTAMP AT TIME ZONE 'UTC+3' created_at,
        CURRENT_TIMESTAMP AT TIME ZONE 'UTC+3' updated_at
    FROM usr_landing.fixtures 
    WHERE 
        league_season = '{season}'
    AND league_id = '{league_id}'
    GROUP BY 
        league_id,
        league_season,
        league_round
    ORDER BY 
        league_season, 
        league_round
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_round)
results = cur.fetchall()
print(results)



merge_statement = """
MERGE INTO dimension.dim_rounds AS dim
USING (
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    ) 
) AS aux (
    league_id,
    league_season,
    league_round,
    start_round_date,
    end_round_date,
    qtd_ft_matches,
    qtd_unplayed_matches,
    created_at,
    updated_at
) ON (dim.league_id = aux.league_id
  and dim.league_season = aux.league_season
  and dim.league_round = aux.league_round)
WHEN MATCHED THEN
    UPDATE SET start_round_date = aux.start_round_date,
               end_round_date = aux.end_round_date,
               qtd_ft_matches = aux.qtd_ft_matches,
               qtd_unplayed_matches = aux.qtd_unplayed_matches,
               updated_at = aux.updated_at
WHEN NOT MATCHED THEN
    INSERT (league_id, league_season, league_round, start_round_date, end_round_date, qtd_ft_matches, qtd_unplayed_matches, created_at, updated_at)
    VALUES (aux.league_id, aux.league_season, aux.league_round, aux.start_round_date, aux.end_round_date, aux.qtd_ft_matches, aux.qtd_unplayed_matches, aux.created_at, aux.updated_at)
"""

cur.executemany(merge_statement, results)
conn.commit()
conn.close()