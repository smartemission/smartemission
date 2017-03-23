--
-- PostgreSQL database dump
--


TRUNCATE TABLE observation RESTART IDENTITY CASCADE;

TRUNCATE TABLE sensor RESTART IDENTITY CASCADE;

TRUNCATE TABLE thing RESTART IDENTITY CASCADE;

TRUNCATE TABLE thing_location RESTART IDENTITY CASCADE;

TRUNCATE TABLE data_stream RESTART IDENTITY CASCADE;

TRUNCATE TABLE feature_of_interest RESTART IDENTITY CASCADE;

TRUNCATE TABLE observed_property RESTART IDENTITY CASCADE;

TRUNCATE TABLE location RESTART IDENTITY CASCADE;

TRUNCATE TABLE historical_location RESTART IDENTITY CASCADE;


DROP TABLE IF EXISTS observation CASCADE;

DROP TABLE IF EXISTS sensor CASCADE;

DROP TABLE IF EXISTS thing CASCADE;

DROP TABLE IF EXISTS thing_location CASCADE;

DROP TABLE IF EXISTS data_stream CASCADE;

DROP TABLE IF EXISTS feature_of_interest CASCADE;

DROP TABLE IF EXISTS observed_property CASCADE;

DROP TABLE IF EXISTS location CASCADE;

DROP TABLE IF EXISTS historical_location CASCADE;

--
-- Name: sensor; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE sensor (
    id bigint NOT NULL,
    navigation_link bytea,
    description character varying(255) NOT NULL,
    encoding_type character varying(255) NOT NULL,
    metadata character varying(255) NOT NULL
);

--
-- Name: thing; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE thing (
    thing_id bigint NOT NULL,
    navigation_link bytea,
    description character varying(255) NOT NULL,
    properties text
);

--
-- Name: thing_location; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE thing_location (
    location_id bigint NOT NULL,
    thing_id bigint NOT NULL
);

--
-- Name: data_stream; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE data_stream (
    datastream_id bigint NOT NULL,
    navigation_link bytea,
    description character varying(255) NOT NULL,
    observation_type character varying(255) NOT NULL,
    observed_area bytea,
    phenomenon_time_end timestamp without time zone,
    phenomenon_time_start timestamp without time zone,
    result_time_end timestamp without time zone,
    result_time_start timestamp without time zone,
    unit_of_measurement text NOT NULL,
    observed_property bigint,
    sensor bigint,
    thing bigint
);

--
-- Name: feature_of_interest; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE feature_of_interest (
    id bigint NOT NULL,
    navigation_link bytea,
    description text NOT NULL,
    encoding_type character varying(255) NOT NULL,
    feature text NOT NULL,
    feature_geometry geometry
);

--
-- Name: observation; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE observation (
    obs_id bigint NOT NULL,
    navigation_link bytea,
    parameters character varying(4096),
    phenomenon_time_end timestamp without time zone,
    phenomenon_time_start timestamp without time zone,
    result character varying(255) NOT NULL,
    result_quality character varying(255),
    result_time timestamp without time zone,
    valid_time_end timestamp without time zone,
    valid_time_start timestamp without time zone,
    data_stream bigint,
    feature_of_interest bigint
);


--
-- Name: observed_property; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE observed_property (
    obs_property_id bigint NOT NULL,
    navigation_link bytea,
    definition character varying(255) NOT NULL,
    description character varying(512) NOT NULL,
    name character varying(255) NOT NULL
);


--
-- Name: location; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE location (
    location_id bigint NOT NULL,
    navigation_link bytea,
    description character varying(255) NOT NULL,
    encoding_type character varying(255) NOT NULL,
    location text NOT NULL,
    location_geometry geometry
);

--
-- Name: historical_location; Type: TABLE; Schema: public; Owner: postgres
--
CREATE TABLE historical_location (
    hist_loc_id bigint NOT NULL,
    navigation_link bytea,
    "time" timestamp without time zone,
    location_id bigint,
    thing_id bigint
);




--
-- Name: data_stream_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stream
    ADD CONSTRAINT data_stream_pkey PRIMARY KEY (datastream_id);


--
-- Name: feature_of_interest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY feature_of_interest
    ADD CONSTRAINT feature_of_interest_pkey PRIMARY KEY (id);


--
-- Name: historical_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY historical_location
    ADD CONSTRAINT historical_location_pkey PRIMARY KEY (hist_loc_id);


--
-- Name: location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY location
    ADD CONSTRAINT location_pkey PRIMARY KEY (location_id);


--
-- Name: observation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT observation_pkey PRIMARY KEY (obs_id);


--
-- Name: observed_property_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY observed_property
    ADD CONSTRAINT observed_property_pkey PRIMARY KEY (obs_property_id);


--
-- Name: sensor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sensor
    ADD CONSTRAINT sensor_pkey PRIMARY KEY (id);


--
-- Name: spatial_ref_sys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY spatial_ref_sys
    ADD CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid);


--
-- Name: thing_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY thing_location
    ADD CONSTRAINT thing_location_pkey PRIMARY KEY (location_id, thing_id);


--
-- Name: thing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY thing
    ADD CONSTRAINT thing_pkey PRIMARY KEY (thing_id);


--
-- Name: feature_geometry_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX feature_geometry_index ON feature_of_interest USING btree (feature_geometry);


--
-- Name: location_geometry_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX location_geometry_index ON location USING btree (location_geometry);


--
-- Name: main_index; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_index ON observation USING btree (data_stream, phenomenon_time_start);


--
-- Name: geometry_columns_delete; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE geometry_columns_delete AS
    ON DELETE TO geometry_columns DO INSTEAD NOTHING;


--
-- Name: geometry_columns_insert; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE geometry_columns_insert AS
    ON INSERT TO geometry_columns DO INSTEAD NOTHING;


--
-- Name: geometry_columns_update; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE geometry_columns_update AS
    ON UPDATE TO geometry_columns DO INSTEAD NOTHING;


--
-- Name: fk_24503697b5204eb3aa38e3e25e0; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stream
    ADD CONSTRAINT fk_24503697b5204eb3aa38e3e25e0 FOREIGN KEY (thing) REFERENCES thing(thing_id);


--
-- Name: fk_252b1d1c4a0e4fb1b2a1c6341f4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stream
    ADD CONSTRAINT fk_252b1d1c4a0e4fb1b2a1c6341f4 FOREIGN KEY (observed_property) REFERENCES observed_property(obs_property_id);


--
-- Name: fk_25b18fcc20f24c09b7e348dde63; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT fk_25b18fcc20f24c09b7e348dde63 FOREIGN KEY (data_stream) REFERENCES data_stream(datastream_id);


--
-- Name: fk_2f7959378a974036b7cd2415d76; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY data_stream
    ADD CONSTRAINT fk_2f7959378a974036b7cd2415d76 FOREIGN KEY (sensor) REFERENCES sensor(id);


--
-- Name: fk_32fc1638323b4bd18b7f1a32987; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY historical_location
    ADD CONSTRAINT fk_32fc1638323b4bd18b7f1a32987 FOREIGN KEY (location_id) REFERENCES location(location_id);


--
-- Name: fk_45ab9e1262bc4925a77268735ce; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT fk_45ab9e1262bc4925a77268735ce FOREIGN KEY (feature_of_interest) REFERENCES feature_of_interest(id);


--
-- Name: fk_5b74addb295d44ad8bff4067a86; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY thing_location
    ADD CONSTRAINT fk_5b74addb295d44ad8bff4067a86 FOREIGN KEY (thing_id) REFERENCES thing(thing_id);


--
-- Name: fk_82ec59a5ffee4e848334a4e3e34; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY historical_location
    ADD CONSTRAINT fk_82ec59a5ffee4e848334a4e3e34 FOREIGN KEY (thing_id) REFERENCES thing(thing_id);


--
-- Name: fk_ac229b7a4ef04e879162eab3f05; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY thing_location
    ADD CONSTRAINT fk_ac229b7a4ef04e879162eab3f05 FOREIGN KEY (location_id) REFERENCES location(location_id);

