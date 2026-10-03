-- Table: dimension.dim_countries

-- DROP TABLE IF EXISTS dimension.dim_countries;

CREATE TABLE IF NOT EXISTS dimension.dim_countries
(
    league_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    name character varying(100) COLLATE pg_catalog."default",
    type character varying(50) COLLATE pg_catalog."default",
    country_name character varying(100) COLLATE pg_catalog."default",
    league_logo character varying(500) COLLATE pg_catalog."default",
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    CONSTRAINT dim_countries_pkey PRIMARY KEY (league_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS dimension.dim_countries
    OWNER to postgres;