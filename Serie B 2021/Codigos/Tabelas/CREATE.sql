CREATE TABLE usr_landing.leagues(
league_id varchar(50) NULL,
league_name varchar(100) NULL,
league_type varchar(50) NULL,
league_logo varchar(500) NULL,
country_name varchar(100) NULL,
country_code varchar(10) NULL,
country_flag varchar(100) NULL,
season_year varchar(100) NULL,
season_start varchar(20) NULL,
season_end varchar(20) NULL,
season_current varchar(50) NULL,
season_coverage_fixtures_events varchar(100) NULL,
season_coverage_fixtures_lineups varchar(100) NULL,
season_coverage_fixtures_statistics_fixtures varchar(100) NULL,
season_coverage_fixtures_statistics_players varchar(100) NULL,
season_coverage_stadings varchar(100) NULL,
season_coverage_players varchar(100) NULL,
season_coverage_top_scorers varchar(100) NULL,
season_coverage_top_assists varchar(100) NULL,
season_coverage_top_cards varchar(100) NULL,
season_coverage_injuries varchar(100) NULL,
season_coverage_predictions varchar(100) NULL,
season_coverage_odds varchar(100) NULL
);


CREATE TABLE usr_landing.fixtures(
fixture_id varchar(150) NULL,
fixture_referee varchar(200) NULL,
fixture_timezone varchar(200) NULL,
fixture_date varchar(200) NULL,
fixture_timestamp varchar(150) NULL,
fixture_period_first varchar(150) NULL,
fixture_period_second varchar(150) NULL,
fixture_venue_id varchar(150) NULL,
fixture_venue_name varchar(50) NULL,
fixture_venue_city varchar(50) NULL,
fixture_status_long varchar(150) NULL,
fixture_status_short varchar(150) NULL,
fixture_status_elapsed varchar(150) NULL,
league_id varchar(150) NULL,
league_name varchar(200) NULL,
league_country varchar(200) NULL,
league_logo varchar(200) NULL,
league_flag varchar(150) NULL,
league_season varchar(150) NULL,
league_round varchar(200) NULL,
teams_home_id varchar(100) NULL,
teams_home_name varchar(100) NULL,
teams_home_logo varchar(200) NULL,
teams_home_winner varchar(150) NULL,
teams_away_id varchar(100) NULL,
teams_away_name varchar(100) NULL,
teams_away_logo varchar(200) NULL,
teams_away_winner varchar(150) NULL,
goals_home varchar(150) NULL,
goals_away varchar(150) NULL,
score_halftime_home varchar(150) NULL,
score_halftime_away varchar(150) NULL,
score_fulltime_home varchar(150) NULL,
score_fulltime_away varchar(150) NULL,
score_extratime_home varchar(150) NULL,
score_extratime_away varchar(150) NULL,
score_penalty_home varchar(150) NULL,
score_penalty_away varchar(150) NULL
);

CREATE TABLE usr_landing.teams (
team_id varchar(150) NULL,
team_country varchar(150) NULL,
team_name varchar(150) NULL,
team_founded varchar(150) NULL,
team_national varchar(150) NULL,
team_logo varchar(150) NULL,
venue_id varchar(150) NULL,
venue_name varchar(150) NULL,
venue_address varchar(150) NULL,
venue_city varchar(150) NULL,
venue_capacity varchar(150) NULL,
venue_surface varchar(150) NULL,
venue_image varchar(150) NULL
);