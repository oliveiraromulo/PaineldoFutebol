CREATE OR REFRESH STREAMING TABLE footballdb.default.silver_leagues
(
    CONSTRAINT valid_season_year EXPECT(season_year IS NOT NULL),
    CONSTRAINT valid_league_id EXPECT(league_id IS NOT NULL) ON VIOLATION DROP ROW
) AS 
SELECT 
ifnull(country_code, '') as country_code,
ifnull(country_flag, '') as country_flag,
ifnull(country_name, '') as country_name,
league_id,
ifnull(league_logo, '') as league_logo,
season_year,
file_modification_time as original_file_modification_time,
current_timestamp as insertion_date
FROM STREAM footballdb.default.bronze_leagues
;