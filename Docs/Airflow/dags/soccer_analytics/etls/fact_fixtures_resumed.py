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
    WITH RANK_CTE AS (
        select rank() over(partition by fixture_id, league_id order by created_at desc) rnk,
        *
        from usr_landing.fixtures
    )

    SELECT 
        CAST(fixture_id AS INT) fixture_id
        ,CAST(fixture_date AS TIMESTAMP) - INTERVAL '3' HOUR AS fixture_date
        ,COALESCE(CAST(fixture_venue_id AS INT), -1) AS fixture_venue_id
        ,CAST(league_id AS INT) league_id
        ,league_season
        ,league_round
        ,CASE 
            WHEN teams_home_winner = 'true' THEN 'HOME'
            WHEN teams_away_winner = 'true' THEN 'AWAY'
            WHEN teams_home_winner IS NULL AND teams_away_winner IS NULL AND GOALS_HOME IS NULL AND GOALS_AWAY IS NULL THEN 'NOT PLAYED'
        ELSE 'DRAW' END game_winner
        ,teams_home_id
        ,COALESCE(CAST(goals_home AS INT)) AS goals_home
        ,teams_away_id
        ,COALESCE(CAST(goals_away AS INT)) AS goals_away
        ,CURRENT_TIMESTAMP AT TIME ZONE 'UTC+3' AS created_at
        ,CURRENT_TIMESTAMP AT TIME ZONE 'UTC+3' AS updated_at
    FROM RANK_CTE
    WHERE rnk = 1;
"""

conn = pg.connect(args['url_conn'])
cur = conn.cursor()

cur.execute(query_round)
results = cur.fetchall()
print(results)


merge_statement = """
MERGE INTO dimension.fact_fixtures_resumed AS dim
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