--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cities; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE cities (
    country_id character varying(10) NOT NULL,
    city_id character varying(15) NOT NULL,
    city_name character varying(100),
    country_name character varying(100),
    lat real,
    lng real
);


ALTER TABLE public.cities OWNER TO postgres;

--
-- Name: last_check; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE last_check (
    insertion_time integer,
    last_check_time integer
);


ALTER TABLE public.last_check OWNER TO postgres;

--
-- Name: stream; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE stream (
    id integer NOT NULL,
    is_post boolean NOT NULL,
    user_id character varying(15) NOT NULL,
    post_id character varying(15) NOT NULL,
    tags character varying(30) NOT NULL,
    text text NOT NULL,
    creation_time integer NOT NULL
);


ALTER TABLE public.stream OWNER TO postgres;

--
-- Name: stream_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE stream_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stream_id_seq OWNER TO postgres;

--
-- Name: stream_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE stream_id_seq OWNED BY stream.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace:
--

CREATE TABLE users (
    user_id character varying(15) NOT NULL,
    country_id character varying(15) NOT NULL,
    city_id character varying(15) NOT NULL,
    city_name character varying(100),
    country_name character varying(100)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY stream ALTER COLUMN id SET DEFAULT nextval('stream_id_seq'::regclass);


--
-- Name: cities_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY cities
    ADD CONSTRAINT cities_pk PRIMARY KEY (country_id, city_id);


--
-- Name: stream_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY stream
    ADD CONSTRAINT stream_pk PRIMARY KEY (id);


--
-- Name: users_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pk PRIMARY KEY (user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
GRANT USAGE ON SCHEMA public TO vkstream;


--
-- Name: cities; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE cities FROM PUBLIC;
REVOKE ALL ON TABLE cities FROM postgres;
GRANT ALL ON TABLE cities TO postgres;
GRANT ALL ON TABLE cities TO vkstream;


--
-- Name: last_check; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE last_check FROM PUBLIC;
REVOKE ALL ON TABLE last_check FROM postgres;
GRANT ALL ON TABLE last_check TO postgres;
GRANT ALL ON TABLE last_check TO vkstream;


--
-- Name: stream; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE stream FROM PUBLIC;
REVOKE ALL ON TABLE stream FROM postgres;
GRANT ALL ON TABLE stream TO postgres;
GRANT ALL ON TABLE stream TO vkstream;


--
-- Name: stream_id_seq; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON SEQUENCE stream_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE stream_id_seq FROM postgres;
GRANT ALL ON SEQUENCE stream_id_seq TO postgres;
GRANT ALL ON SEQUENCE stream_id_seq TO vkstream;


--
-- Name: users; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM postgres;
GRANT ALL ON TABLE users TO postgres;
GRANT ALL ON TABLE users TO vkstream;


--
-- PostgreSQL database dump complete
--
