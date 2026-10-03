CREATE OR REFRESH STREAMING TABLE footballdb.default.bronze_leagues AS 
SELECT *,
_metadata.file_name,
_metadata.file_path,
_metadata.file_modification_time
FROM STREAM read_files(
"/Volumes/footballdb/default/jsonfiles/leagues/",
format => "json",
header => true,
schema => "STRUCT<country_code: STRING, country_flag: STRING, country_name: STRING, league_id: BIGINT, league_logo: STRING, league_name: STRING, league_type: STRING, season_coverage_fixtures_events: BOOLEAN, season_coverage_fixtures_lineups: BOOLEAN, season_coverage_fixtures_statistics_fixtures: BOOLEAN, season_coverage_fixtures_statistics_players: BOOLEAN, season_coverage_injuries: BOOLEAN, season_coverage_odds: BOOLEAN, season_coverage_players: BOOLEAN, season_coverage_predictions: BOOLEAN, season_coverage_stadings: BOOLEAN, season_coverage_top_assists: BOOLEAN, season_coverage_top_cards: BOOLEAN, season_coverage_top_scorers: BOOLEAN, season_current: BOOLEAN, season_end: STRING, season_start: STRING, season_year: BIGINT>",
rescuedDataColumn => "_rescued_data"
) ;
