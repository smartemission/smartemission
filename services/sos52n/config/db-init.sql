--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = sos52n1, pg_catalog;

ALTER TABLE IF EXISTS ONLY sos52n1.validproceduretime DROP CONSTRAINT IF EXISTS validprocprocdescformatfk;
ALTER TABLE IF EXISTS ONLY sos52n1.validproceduretime DROP CONSTRAINT IF EXISTS validproceduretimeprocedurefk;
ALTER TABLE IF EXISTS ONLY sos52n1.series DROP CONSTRAINT IF EXISTS seriesunitfk;
ALTER TABLE IF EXISTS ONLY sos52n1.series DROP CONSTRAINT IF EXISTS seriesprocedurefk;
ALTER TABLE IF EXISTS ONLY sos52n1.series DROP CONSTRAINT IF EXISTS seriesobpropfk;
ALTER TABLE IF EXISTS ONLY sos52n1.series DROP CONSTRAINT IF EXISTS seriesfeaturefk;
ALTER TABLE IF EXISTS ONLY sos52n1.resulttemplate DROP CONSTRAINT IF EXISTS resulttemplateprocedurefk;
ALTER TABLE IF EXISTS ONLY sos52n1.resulttemplate DROP CONSTRAINT IF EXISTS resulttemplateofferingidx;
ALTER TABLE IF EXISTS ONLY sos52n1.resulttemplate DROP CONSTRAINT IF EXISTS resulttemplateobspropfk;
ALTER TABLE IF EXISTS ONLY sos52n1.resulttemplate DROP CONSTRAINT IF EXISTS resulttemplatefeatureidx;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringhasrelatedfeature DROP CONSTRAINT IF EXISTS relatedfeatureofferingfk;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeature DROP CONSTRAINT IF EXISTS relatedfeaturefeaturefk;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeaturehasrole DROP CONSTRAINT IF EXISTS relatedfeatrelatedfeatrolefk;
ALTER TABLE IF EXISTS ONLY sos52n1.procedure DROP CONSTRAINT IF EXISTS procprocdescformatfk;
ALTER TABLE IF EXISTS ONLY sos52n1.sensorsystem DROP CONSTRAINT IF EXISTS procedureparenffk;
ALTER TABLE IF EXISTS ONLY sos52n1.sensorsystem DROP CONSTRAINT IF EXISTS procedurechildfk;
ALTER TABLE IF EXISTS ONLY sos52n1.procedure DROP CONSTRAINT IF EXISTS proccodespacenamefk;
ALTER TABLE IF EXISTS ONLY sos52n1.procedure DROP CONSTRAINT IF EXISTS proccodespaceidentifierfk;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringhasrelatedfeature DROP CONSTRAINT IF EXISTS offeringrelatedfeaturefk;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringallowedobservationtype DROP CONSTRAINT IF EXISTS offeringobservationtypefk;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringallowedfeaturetype DROP CONSTRAINT IF EXISTS offeringfeaturetypefk;
ALTER TABLE IF EXISTS ONLY sos52n1.offering DROP CONSTRAINT IF EXISTS offcodespacenamefk;
ALTER TABLE IF EXISTS ONLY sos52n1.offering DROP CONSTRAINT IF EXISTS offcodespaceidentifierfk;
ALTER TABLE IF EXISTS ONLY sos52n1.observableproperty DROP CONSTRAINT IF EXISTS obspropcodespacenamefk;
ALTER TABLE IF EXISTS ONLY sos52n1.observableproperty DROP CONSTRAINT IF EXISTS obspropcodespaceidentifierfk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationconstellation DROP CONSTRAINT IF EXISTS obsnconstprocedurefk;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS observationunitfk;
ALTER TABLE IF EXISTS ONLY sos52n1.textvalue DROP CONSTRAINT IF EXISTS observationtextvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.swedataarrayvalue DROP CONSTRAINT IF EXISTS observationswedataarrayvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS observationseriesfk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationhasoffering DROP CONSTRAINT IF EXISTS observationofferingfk;
ALTER TABLE IF EXISTS ONLY sos52n1.numericvalue DROP CONSTRAINT IF EXISTS observationnumericvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.geometryvalue DROP CONSTRAINT IF EXISTS observationgeometryvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.countvalue DROP CONSTRAINT IF EXISTS observationcountvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.categoryvalue DROP CONSTRAINT IF EXISTS observationcategoryvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.booleanvalue DROP CONSTRAINT IF EXISTS observationbooleanvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.blobvalue DROP CONSTRAINT IF EXISTS observationblobvaluefk;
ALTER TABLE IF EXISTS ONLY sos52n1.compositephenomenon DROP CONSTRAINT IF EXISTS observablepropertyparentfk;
ALTER TABLE IF EXISTS ONLY sos52n1.compositephenomenon DROP CONSTRAINT IF EXISTS observablepropertychildfk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationconstellation DROP CONSTRAINT IF EXISTS obsconstofferingfk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationconstellation DROP CONSTRAINT IF EXISTS obsconstobspropfk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationconstellation DROP CONSTRAINT IF EXISTS obsconstobservationiypefk;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS obscodespacenamefk;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS obscodespaceidentifierfk;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nprocedure DROP CONSTRAINT IF EXISTS i18nprocedureprocedurefk;
ALTER TABLE IF EXISTS ONLY sos52n1.i18noffering DROP CONSTRAINT IF EXISTS i18nofferingofferingfk;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nobservableproperty DROP CONSTRAINT IF EXISTS i18nobspropobspropfk;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nfeatureofinterest DROP CONSTRAINT IF EXISTS i18nfeaturefeaturefk;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringallowedobservationtype DROP CONSTRAINT IF EXISTS fk_lkljeohulvu7cr26pduyp5bd0;
ALTER TABLE IF EXISTS ONLY sos52n1.observationhasoffering DROP CONSTRAINT IF EXISTS fk_9ex7hawh3dbplkllmw5w3kvej;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeaturehasrole DROP CONSTRAINT IF EXISTS fk_6ynwkk91xe8p1uibmjt98sog3;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringallowedfeaturetype DROP CONSTRAINT IF EXISTS fk_6vvrdxvd406n48gkm706ow1pt;
ALTER TABLE IF EXISTS ONLY sos52n1.featurerelation DROP CONSTRAINT IF EXISTS featureofinterestparentfk;
ALTER TABLE IF EXISTS ONLY sos52n1.featurerelation DROP CONSTRAINT IF EXISTS featureofinterestchildfk;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinterest DROP CONSTRAINT IF EXISTS featurefeaturetypefk;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinterest DROP CONSTRAINT IF EXISTS featurecodespacenamefk;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinterest DROP CONSTRAINT IF EXISTS featurecodespaceidentifierfk;
DROP INDEX IF EXISTS sos52n1.validproceduretimestarttimeidx;
DROP INDEX IF EXISTS sos52n1.validproceduretimeendtimeidx;
DROP INDEX IF EXISTS sos52n1.seriesprocedureidx;
DROP INDEX IF EXISTS sos52n1.seriesobspropidx;
DROP INDEX IF EXISTS sos52n1.seriesfeatureidx;
DROP INDEX IF EXISTS sos52n1.resulttempprocedureidx;
DROP INDEX IF EXISTS sos52n1.resulttempofferingidx;
DROP INDEX IF EXISTS sos52n1.resulttempidentifieridx;
DROP INDEX IF EXISTS sos52n1.resulttempeobspropidx;
DROP INDEX IF EXISTS sos52n1.obsseriesidx;
DROP INDEX IF EXISTS sos52n1.obsresulttimeidx;
DROP INDEX IF EXISTS sos52n1.obsphentimestartidx;
DROP INDEX IF EXISTS sos52n1.obsphentimeendidx;
DROP INDEX IF EXISTS sos52n1.obshasoffofferingidx;
DROP INDEX IF EXISTS sos52n1.obshasoffobservationidx;
DROP INDEX IF EXISTS sos52n1.obsconstprocedureidx;
DROP INDEX IF EXISTS sos52n1.obsconstofferingidx;
DROP INDEX IF EXISTS sos52n1.obsconstobspropidx;
DROP INDEX IF EXISTS sos52n1.i18nprocedureidx;
DROP INDEX IF EXISTS sos52n1.i18nofferingidx;
DROP INDEX IF EXISTS sos52n1.i18nobspropidx;
DROP INDEX IF EXISTS sos52n1.i18nfeatureidx;
ALTER TABLE IF EXISTS ONLY sos52n1.validproceduretime DROP CONSTRAINT IF EXISTS validproceduretime_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.unit DROP CONSTRAINT IF EXISTS unituk;
ALTER TABLE IF EXISTS ONLY sos52n1.unit DROP CONSTRAINT IF EXISTS unit_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.textvalue DROP CONSTRAINT IF EXISTS textvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.swedataarrayvalue DROP CONSTRAINT IF EXISTS swedataarrayvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.series DROP CONSTRAINT IF EXISTS seriesidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.series DROP CONSTRAINT IF EXISTS series_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.sensorsystem DROP CONSTRAINT IF EXISTS sensorsystem_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.resulttemplate DROP CONSTRAINT IF EXISTS resulttemplate_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeaturerole DROP CONSTRAINT IF EXISTS relfeatroleuk;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeaturerole DROP CONSTRAINT IF EXISTS relatedfeaturerole_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeaturehasrole DROP CONSTRAINT IF EXISTS relatedfeaturehasrole_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.relatedfeature DROP CONSTRAINT IF EXISTS relatedfeature_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.procedure DROP CONSTRAINT IF EXISTS procidentifieruk;
ALTER TABLE IF EXISTS ONLY sos52n1.proceduredescriptionformat DROP CONSTRAINT IF EXISTS proceduredescriptionformat_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.procedure DROP CONSTRAINT IF EXISTS procedure_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.proceduredescriptionformat DROP CONSTRAINT IF EXISTS procdescformatuk;
ALTER TABLE IF EXISTS ONLY sos52n1.parameter DROP CONSTRAINT IF EXISTS parameter_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.offering DROP CONSTRAINT IF EXISTS offidentifieruk;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringhasrelatedfeature DROP CONSTRAINT IF EXISTS offeringhasrelatedfeature_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringallowedobservationtype DROP CONSTRAINT IF EXISTS offeringallowedobservationtype_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.offeringallowedfeaturetype DROP CONSTRAINT IF EXISTS offeringallowedfeaturetype_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.offering DROP CONSTRAINT IF EXISTS offering_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.observableproperty DROP CONSTRAINT IF EXISTS obspropidentifieruk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationconstellation DROP CONSTRAINT IF EXISTS obsnconstellationidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS obsidentifieruk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationtype DROP CONSTRAINT IF EXISTS observationtypeuk;
ALTER TABLE IF EXISTS ONLY sos52n1.observationtype DROP CONSTRAINT IF EXISTS observationtype_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS observationidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.observationhasoffering DROP CONSTRAINT IF EXISTS observationhasoffering_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.observationconstellation DROP CONSTRAINT IF EXISTS observationconstellation_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.observation DROP CONSTRAINT IF EXISTS observation_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.observableproperty DROP CONSTRAINT IF EXISTS observableproperty_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.numericvalue DROP CONSTRAINT IF EXISTS numericvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nprocedure DROP CONSTRAINT IF EXISTS i18nprocedureidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nprocedure DROP CONSTRAINT IF EXISTS i18nprocedure_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.i18noffering DROP CONSTRAINT IF EXISTS i18nofferingidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.i18noffering DROP CONSTRAINT IF EXISTS i18noffering_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nobservableproperty DROP CONSTRAINT IF EXISTS i18nobspropidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nobservableproperty DROP CONSTRAINT IF EXISTS i18nobservableproperty_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nfeatureofinterest DROP CONSTRAINT IF EXISTS i18nfeatureofinterest_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.i18nfeatureofinterest DROP CONSTRAINT IF EXISTS i18nfeatureidentity;
ALTER TABLE IF EXISTS ONLY sos52n1.geometryvalue DROP CONSTRAINT IF EXISTS geometryvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinterest DROP CONSTRAINT IF EXISTS foiidentifieruk;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinterest DROP CONSTRAINT IF EXISTS featureurl;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinteresttype DROP CONSTRAINT IF EXISTS featuretypeuk;
ALTER TABLE IF EXISTS ONLY sos52n1.featurerelation DROP CONSTRAINT IF EXISTS featurerelation_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinteresttype DROP CONSTRAINT IF EXISTS featureofinteresttype_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.featureofinterest DROP CONSTRAINT IF EXISTS featureofinterest_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.countvalue DROP CONSTRAINT IF EXISTS countvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.compositephenomenon DROP CONSTRAINT IF EXISTS compositephenomenon_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.codespace DROP CONSTRAINT IF EXISTS codespaceuk;
ALTER TABLE IF EXISTS ONLY sos52n1.codespace DROP CONSTRAINT IF EXISTS codespace_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.categoryvalue DROP CONSTRAINT IF EXISTS categoryvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.booleanvalue DROP CONSTRAINT IF EXISTS booleanvalue_pkey;
ALTER TABLE IF EXISTS ONLY sos52n1.blobvalue DROP CONSTRAINT IF EXISTS blobvalue_pkey;
DROP SEQUENCE IF EXISTS sos52n1.validproceduretimeid_seq;
DROP TABLE IF EXISTS sos52n1.validproceduretime;
DROP SEQUENCE IF EXISTS sos52n1.unitid_seq;
DROP TABLE IF EXISTS sos52n1.unit;
DROP TABLE IF EXISTS sos52n1.textvalue;
DROP TABLE IF EXISTS sos52n1.swedataarrayvalue;
DROP SEQUENCE IF EXISTS sos52n1.seriesid_seq;
DROP TABLE IF EXISTS sos52n1.series;
DROP TABLE IF EXISTS sos52n1.sensorsystem;
DROP SEQUENCE IF EXISTS sos52n1.resulttemplateid_seq;
DROP TABLE IF EXISTS sos52n1.resulttemplate;
DROP SEQUENCE IF EXISTS sos52n1.relatedfeatureroleid_seq;
DROP TABLE IF EXISTS sos52n1.relatedfeaturerole;
DROP SEQUENCE IF EXISTS sos52n1.relatedfeatureid_seq;
DROP TABLE IF EXISTS sos52n1.relatedfeaturehasrole;
DROP TABLE IF EXISTS sos52n1.relatedfeature;
DROP SEQUENCE IF EXISTS sos52n1.procedureid_seq;
DROP TABLE IF EXISTS sos52n1.proceduredescriptionformat;
DROP TABLE IF EXISTS sos52n1.procedure;
DROP SEQUENCE IF EXISTS sos52n1.procdescformatid_seq;
DROP SEQUENCE IF EXISTS sos52n1.parameterid_seq;
DROP TABLE IF EXISTS sos52n1.parameter;
DROP SEQUENCE IF EXISTS sos52n1.offeringid_seq;
DROP TABLE IF EXISTS sos52n1.offeringhasrelatedfeature;
DROP TABLE IF EXISTS sos52n1.offeringallowedobservationtype;
DROP TABLE IF EXISTS sos52n1.offeringallowedfeaturetype;
DROP TABLE IF EXISTS sos52n1.offering;
DROP SEQUENCE IF EXISTS sos52n1.observationtypeid_seq;
DROP TABLE IF EXISTS sos52n1.observationtype;
DROP SEQUENCE IF EXISTS sos52n1.observationid_seq;
DROP TABLE IF EXISTS sos52n1.observationhasoffering;
DROP SEQUENCE IF EXISTS sos52n1.observationconstellationid_seq;
DROP TABLE IF EXISTS sos52n1.observationconstellation;
DROP TABLE IF EXISTS sos52n1.observation;
DROP SEQUENCE IF EXISTS sos52n1.observablepropertyid_seq;
DROP TABLE IF EXISTS sos52n1.observableproperty;
DROP TABLE IF EXISTS sos52n1.numericvalue;
DROP SEQUENCE IF EXISTS sos52n1.i18nprocedureid_seq;
DROP TABLE IF EXISTS sos52n1.i18nprocedure;
DROP SEQUENCE IF EXISTS sos52n1.i18nofferingid_seq;
DROP TABLE IF EXISTS sos52n1.i18noffering;
DROP SEQUENCE IF EXISTS sos52n1.i18nobspropid_seq;
DROP TABLE IF EXISTS sos52n1.i18nobservableproperty;
DROP SEQUENCE IF EXISTS sos52n1.i18nfeatureofinterestid_seq;
DROP TABLE IF EXISTS sos52n1.i18nfeatureofinterest;
DROP TABLE IF EXISTS sos52n1.geometryvalue;
DROP TABLE IF EXISTS sos52n1.featurerelation;
DROP SEQUENCE IF EXISTS sos52n1.featureofinteresttypeid_seq;
DROP TABLE IF EXISTS sos52n1.featureofinteresttype;
DROP SEQUENCE IF EXISTS sos52n1.featureofinterestid_seq;
DROP TABLE IF EXISTS sos52n1.featureofinterest;
DROP TABLE IF EXISTS sos52n1.countvalue;
DROP TABLE IF EXISTS sos52n1.compositephenomenon;
DROP SEQUENCE IF EXISTS sos52n1.codespaceid_seq;
DROP TABLE IF EXISTS sos52n1.codespace;
DROP TABLE IF EXISTS sos52n1.categoryvalue;
DROP TABLE IF EXISTS sos52n1.booleanvalue;
DROP TABLE IF EXISTS sos52n1.blobvalue;
DROP SCHEMA IF EXISTS sos52n1;
--
-- Name: sos52n1; Type: SCHEMA; Schema: -; Owner: docker
--

CREATE SCHEMA sos52n1;


ALTER SCHEMA sos52n1 OWNER TO docker;

--
-- Name: SCHEMA sos52n1; Type: COMMENT; Schema: -; Owner: docker
--

COMMENT ON SCHEMA sos52n1 IS '52North SOS';


SET search_path = sos52n1, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: blobvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE blobvalue (
    observationid bigint NOT NULL,
    value oid
);


ALTER TABLE blobvalue OWNER TO docker;

--
-- Name: TABLE blobvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE blobvalue IS 'Value table for blob observation';


--
-- Name: COLUMN blobvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN blobvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN blobvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN blobvalue.value IS 'Blob observation value';


--
-- Name: booleanvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE booleanvalue (
    observationid bigint NOT NULL,
    value character(1),
    CONSTRAINT booleanvalue_value_check CHECK ((value = ANY (ARRAY['T'::bpchar, 'F'::bpchar]))),
    CONSTRAINT booleanvalue_value_check1 CHECK ((value = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE booleanvalue OWNER TO docker;

--
-- Name: TABLE booleanvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE booleanvalue IS 'Value table for boolean observation';


--
-- Name: COLUMN booleanvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN booleanvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN booleanvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN booleanvalue.value IS 'Boolean observation value';


--
-- Name: categoryvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE categoryvalue (
    observationid bigint NOT NULL,
    value character varying(255)
);


ALTER TABLE categoryvalue OWNER TO docker;

--
-- Name: TABLE categoryvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE categoryvalue IS 'Value table for category observation';


--
-- Name: COLUMN categoryvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN categoryvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN categoryvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN categoryvalue.value IS 'Category observation value';


--
-- Name: codespace; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE codespace (
    codespaceid bigint NOT NULL,
    codespace character varying(255) NOT NULL
);


ALTER TABLE codespace OWNER TO docker;

--
-- Name: TABLE codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE codespace IS 'Table to store the gml:identifier and gml:name codespace information. Mapping file: mapping/core/Codespace.hbm.xml';


--
-- Name: COLUMN codespace.codespaceid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN codespace.codespaceid IS 'Table primary key, used for relations';


--
-- Name: COLUMN codespace.codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN codespace.codespace IS 'The codespace value';


--
-- Name: codespaceid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE codespaceid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE codespaceid_seq OWNER TO docker;

--
-- Name: compositephenomenon; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE compositephenomenon (
    parentobservablepropertyid bigint NOT NULL,
    childobservablepropertyid bigint NOT NULL
);


ALTER TABLE compositephenomenon OWNER TO docker;

--
-- Name: TABLE compositephenomenon; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE compositephenomenon IS 'NOT YET USED! Relation table to store observableProperty hierarchies, aka compositePhenomenon. E.g. define a parent in a query and all childs are also contained in the response. Mapping file: mapping/transactional/TObservableProperty.hbm.xml';


--
-- Name: COLUMN compositephenomenon.parentobservablepropertyid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN compositephenomenon.parentobservablepropertyid IS 'Foreign Key (FK) to the related parent observableProperty. Contains "observableProperty".observablePropertyid';


--
-- Name: COLUMN compositephenomenon.childobservablepropertyid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN compositephenomenon.childobservablepropertyid IS 'Foreign Key (FK) to the related child observableProperty. Contains "observableProperty".observablePropertyid';


--
-- Name: countvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE countvalue (
    observationid bigint NOT NULL,
    value integer
);


ALTER TABLE countvalue OWNER TO docker;

--
-- Name: TABLE countvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE countvalue IS 'Value table for count observation';


--
-- Name: COLUMN countvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN countvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN countvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN countvalue.value IS 'Count observation value';


--
-- Name: featureofinterest; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE featureofinterest (
    featureofinterestid bigint NOT NULL,
    hibernatediscriminator character(1) NOT NULL,
    featureofinteresttypeid bigint NOT NULL,
    identifier character varying(255),
    codespace bigint,
    name character varying(255),
    codespacename bigint,
    description character varying(255),
    geom public.geometry,
    descriptionxml text,
    url character varying(255)
);


ALTER TABLE featureofinterest OWNER TO docker;

--
-- Name: TABLE featureofinterest; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE featureofinterest IS 'Table to store the FeatureOfInterest information. Mapping file: mapping/core/FeatureOfInterest.hbm.xml';


--
-- Name: COLUMN featureofinterest.featureofinterestid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.featureofinterestid IS 'Table primary key, used for relations';


--
-- Name: COLUMN featureofinterest.featureofinteresttypeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.featureofinteresttypeid IS 'Relation/foreign key to the featureOfInterestType table. Describes the type of the featureOfInterest. Contains "featureOfInterestType".featureOfInterestTypeId';


--
-- Name: COLUMN featureofinterest.identifier; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.identifier IS 'The identifier of the featureOfInterest, gml:identifier. Used as parameter for queries. Optional but unique';


--
-- Name: COLUMN featureofinterest.codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.codespace IS 'Relation/foreign key to the codespace table. Contains the gml:identifier codespace. Optional';


--
-- Name: COLUMN featureofinterest.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.name IS 'The name of the featureOfInterest, gml:name. Optional';


--
-- Name: COLUMN featureofinterest.codespacename; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.codespacename IS 'The name of the featureOfInterest, gml:name. Optional';


--
-- Name: COLUMN featureofinterest.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.description IS 'Description of the featureOfInterest, gml:description. Optional';


--
-- Name: COLUMN featureofinterest.geom; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.geom IS 'The geometry of the featureOfInterest (composed of the “latitude” and “longitude”) . Optional';


--
-- Name: COLUMN featureofinterest.descriptionxml; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.descriptionxml IS 'XML description of the feature, used when transactional profile is supported . Optional';


--
-- Name: COLUMN featureofinterest.url; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinterest.url IS 'Reference URL to the feature if it is stored in another service, e.g. WFS. Optional but unique';


--
-- Name: featureofinterestid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE featureofinterestid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE featureofinterestid_seq OWNER TO docker;

--
-- Name: featureofinteresttype; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE featureofinteresttype (
    featureofinteresttypeid bigint NOT NULL,
    featureofinteresttype character varying(255) NOT NULL
);


ALTER TABLE featureofinteresttype OWNER TO docker;

--
-- Name: TABLE featureofinteresttype; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE featureofinteresttype IS 'Table to store the FeatureOfInterestType information. Mapping file: mapping/core/FeatureOfInterestType.hbm.xml';


--
-- Name: COLUMN featureofinteresttype.featureofinteresttypeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinteresttype.featureofinteresttypeid IS 'Table primary key, used for relations';


--
-- Name: COLUMN featureofinteresttype.featureofinteresttype; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featureofinteresttype.featureofinteresttype IS 'The featureOfInterestType value, e.g. http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint (OGC OM 2.0 specification) for point features';


--
-- Name: featureofinteresttypeid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE featureofinteresttypeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE featureofinteresttypeid_seq OWNER TO docker;

--
-- Name: featurerelation; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE featurerelation (
    parentfeatureid bigint NOT NULL,
    childfeatureid bigint NOT NULL
);


ALTER TABLE featurerelation OWNER TO docker;

--
-- Name: TABLE featurerelation; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE featurerelation IS 'Relation table to store feature hierarchies. E.g. define a parent in a query and all childs are also contained in the response. Mapping file: mapping/transactional/TFeatureOfInterest.hbm.xml';


--
-- Name: COLUMN featurerelation.parentfeatureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featurerelation.parentfeatureid IS 'Foreign Key (FK) to the related parent featureOfInterest. Contains "featureOfInterest".featureOfInterestid';


--
-- Name: COLUMN featurerelation.childfeatureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN featurerelation.childfeatureid IS 'Foreign Key (FK) to the related child featureOfInterest. Contains "featureOfInterest".featureOfInterestid';


--
-- Name: geometryvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE geometryvalue (
    observationid bigint NOT NULL,
    value public.geometry
);


ALTER TABLE geometryvalue OWNER TO docker;

--
-- Name: TABLE geometryvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE geometryvalue IS 'Value table for geometry observation';


--
-- Name: COLUMN geometryvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN geometryvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN geometryvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN geometryvalue.value IS 'Geometry observation value';


--
-- Name: i18nfeatureofinterest; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE i18nfeatureofinterest (
    id bigint NOT NULL,
    objectid bigint NOT NULL,
    locale character varying(255) NOT NULL,
    name character varying(255),
    description character varying(255)
);


ALTER TABLE i18nfeatureofinterest OWNER TO docker;

--
-- Name: TABLE i18nfeatureofinterest; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE i18nfeatureofinterest IS 'Table to i18n metadata for the featureOfInterest. Mapping file: mapping/i18n/HibernateI18NFeatureOfInterestMetadata.hbm.xml';


--
-- Name: COLUMN i18nfeatureofinterest.id; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nfeatureofinterest.id IS 'Table primary key';


--
-- Name: COLUMN i18nfeatureofinterest.objectid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nfeatureofinterest.objectid IS 'Foreign Key (FK) to the related featureOfInterest. Contains "featureOfInterest".featureOfInterestid';


--
-- Name: COLUMN i18nfeatureofinterest.locale; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nfeatureofinterest.locale IS 'Locale/language identification, e.g. eng, ger';


--
-- Name: COLUMN i18nfeatureofinterest.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nfeatureofinterest.name IS 'Locale/language specific name of the featureOfInterest';


--
-- Name: COLUMN i18nfeatureofinterest.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nfeatureofinterest.description IS 'Locale/language specific description of the featureOfInterest';


--
-- Name: i18nfeatureofinterestid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE i18nfeatureofinterestid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE i18nfeatureofinterestid_seq OWNER TO docker;

--
-- Name: i18nobservableproperty; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE i18nobservableproperty (
    id bigint NOT NULL,
    objectid bigint NOT NULL,
    locale character varying(255) NOT NULL,
    name character varying(255),
    description character varying(255)
);


ALTER TABLE i18nobservableproperty OWNER TO docker;

--
-- Name: TABLE i18nobservableproperty; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE i18nobservableproperty IS 'Table to i18n metadata for the observableProperty/phenomenon. Mapping file: mapping/i18n/HibernateI18NObservablePropertyMetadata.hbm.xml';


--
-- Name: COLUMN i18nobservableproperty.id; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nobservableproperty.id IS 'Table primary key';


--
-- Name: COLUMN i18nobservableproperty.objectid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nobservableproperty.objectid IS 'Foreign Key (FK) to the related observableProperty. Contains "observableProperty".observablePropertyid';


--
-- Name: COLUMN i18nobservableproperty.locale; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nobservableproperty.locale IS 'Locale/language identification, e.g. eng, ger';


--
-- Name: COLUMN i18nobservableproperty.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nobservableproperty.name IS 'Locale/language specific name of the observableProperty';


--
-- Name: COLUMN i18nobservableproperty.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nobservableproperty.description IS 'Locale/language specific description of the observableProperty';


--
-- Name: i18nobspropid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE i18nobspropid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE i18nobspropid_seq OWNER TO docker;

--
-- Name: i18noffering; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE i18noffering (
    id bigint NOT NULL,
    objectid bigint NOT NULL,
    locale character varying(255) NOT NULL,
    name character varying(255),
    description character varying(255)
);


ALTER TABLE i18noffering OWNER TO docker;

--
-- Name: TABLE i18noffering; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE i18noffering IS 'Table to i18n metadata for the offering. Mapping file: mapping/i18n/HibernateI18NOfferingMetadata.hbm.xml';


--
-- Name: COLUMN i18noffering.id; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18noffering.id IS 'Table primary key';


--
-- Name: COLUMN i18noffering.objectid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18noffering.objectid IS 'Foreign Key (FK) to the related offering. Contains "offering".offeringid';


--
-- Name: COLUMN i18noffering.locale; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18noffering.locale IS 'Locale/language identification, e.g. eng, ger';


--
-- Name: COLUMN i18noffering.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18noffering.name IS 'Locale/language specific name of the offering';


--
-- Name: COLUMN i18noffering.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18noffering.description IS 'Locale/language specific description of the offering';


--
-- Name: i18nofferingid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE i18nofferingid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE i18nofferingid_seq OWNER TO docker;

--
-- Name: i18nprocedure; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE i18nprocedure (
    id bigint NOT NULL,
    objectid bigint NOT NULL,
    locale character varying(255) NOT NULL,
    name character varying(255),
    description character varying(255),
    shortname character varying(255),
    longname character varying(255)
);


ALTER TABLE i18nprocedure OWNER TO docker;

--
-- Name: TABLE i18nprocedure; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE i18nprocedure IS 'Table to i18n metadata for the procedure. Mapping file: mapping/i18n/HibernateI18NProcedureMetadata.hbm.xml';


--
-- Name: COLUMN i18nprocedure.id; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.id IS 'Table primary key';


--
-- Name: COLUMN i18nprocedure.objectid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.objectid IS 'Foreign Key (FK) to the related procedure. Contains "procedure".procedureid';


--
-- Name: COLUMN i18nprocedure.locale; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.locale IS 'Locale/language identification, e.g. eng, ger';


--
-- Name: COLUMN i18nprocedure.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.name IS 'Locale/language specific name of the procedure';


--
-- Name: COLUMN i18nprocedure.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.description IS 'Locale/language specific description of the procedure';


--
-- Name: COLUMN i18nprocedure.shortname; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.shortname IS 'Locale/language specific shortname of the procedure';


--
-- Name: COLUMN i18nprocedure.longname; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN i18nprocedure.longname IS 'Locale/language specific longname of the procedure';


--
-- Name: i18nprocedureid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE i18nprocedureid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE i18nprocedureid_seq OWNER TO docker;

--
-- Name: numericvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE numericvalue (
    observationid bigint NOT NULL,
    value double precision
);


ALTER TABLE numericvalue OWNER TO docker;

--
-- Name: TABLE numericvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE numericvalue IS 'Value table for numeric/Measurment observation';


--
-- Name: COLUMN numericvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN numericvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN numericvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN numericvalue.value IS 'Numeric/Measurment observation value';


--
-- Name: observableproperty; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE observableproperty (
    observablepropertyid bigint NOT NULL,
    hibernatediscriminator character(1) NOT NULL,
    identifier character varying(255) NOT NULL,
    codespace bigint,
    name character varying(255),
    codespacename bigint,
    description character varying(255),
    disabled character(1) DEFAULT 'F'::bpchar NOT NULL,
    CONSTRAINT observableproperty_disabled_check CHECK ((disabled = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE observableproperty OWNER TO docker;

--
-- Name: TABLE observableproperty; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE observableproperty IS 'Table to store the ObservedProperty/Phenomenon information. Mapping file: mapping/core/ObservableProperty.hbm.xml';


--
-- Name: COLUMN observableproperty.observablepropertyid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.observablepropertyid IS 'Table primary key, used for relations';


--
-- Name: COLUMN observableproperty.identifier; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.identifier IS 'The identifier of the observableProperty, gml:identifier. Used as parameter for queries. Unique';


--
-- Name: COLUMN observableproperty.codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.codespace IS 'Relation/foreign key to the codespace table. Contains the gml:identifier codespace. Optional';


--
-- Name: COLUMN observableproperty.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.name IS 'The name of the observableProperty, gml:name. Optional';


--
-- Name: COLUMN observableproperty.codespacename; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.codespacename IS 'Relation/foreign key to the codespace table. Contains the gml:name codespace. Optional';


--
-- Name: COLUMN observableproperty.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.description IS 'Description of the observableProperty, gml:description. Optional';


--
-- Name: COLUMN observableproperty.disabled; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observableproperty.disabled IS 'For later use by the SOS. Indicator if this observableProperty should not be provided by the SOS.';


--
-- Name: observablepropertyid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE observablepropertyid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE observablepropertyid_seq OWNER TO docker;

--
-- Name: observation; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE observation (
    observationid bigint NOT NULL,
    seriesid bigint NOT NULL,
    phenomenontimestart timestamp without time zone NOT NULL,
    phenomenontimeend timestamp without time zone NOT NULL,
    resulttime timestamp without time zone NOT NULL,
    identifier character varying(255),
    codespace bigint,
    name character varying(255),
    codespacename bigint,
    description character varying(255),
    deleted character(1) DEFAULT 'F'::bpchar NOT NULL,
    validtimestart timestamp without time zone,
    validtimeend timestamp without time zone,
    unitid bigint,
    samplinggeometry public.geometry,
    CONSTRAINT observation_deleted_check CHECK ((deleted = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE observation OWNER TO docker;

--
-- Name: TABLE observation; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE observation IS 'Stores the observations. Mapping file: mapping/series/observation/SeriesObservation.hbm.xml';


--
-- Name: COLUMN observation.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.observationid IS 'Table primary key, used in relations';


--
-- Name: COLUMN observation.seriesid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.seriesid IS 'Relation/foreign key to the associated series table. Contains "series".seriesId';


--
-- Name: COLUMN observation.phenomenontimestart; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.phenomenontimestart IS 'Time stamp when the observation was started or phenomenon was observed';


--
-- Name: COLUMN observation.phenomenontimeend; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.phenomenontimeend IS 'Time stamp when the observation was stopped or phenomenon was observed';


--
-- Name: COLUMN observation.resulttime; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.resulttime IS 'Time stamp when the observation was published or result was published/available';


--
-- Name: COLUMN observation.identifier; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.identifier IS 'The identifier of the observation, gml:identifier. Used as parameter for queries. Optional but unique';


--
-- Name: COLUMN observation.codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.codespace IS 'Relation/foreign key to the codespace table. Contains the gml:identifier codespace. Optional';


--
-- Name: COLUMN observation.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.name IS 'The name of the observation, gml:name. Optional';


--
-- Name: COLUMN observation.codespacename; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.codespacename IS 'The name of the observation, gml:name. Optional';


--
-- Name: COLUMN observation.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.description IS 'Description of the observation, gml:description. Optional';


--
-- Name: COLUMN observation.deleted; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.deleted IS 'Flag to indicate that this observation is deleted or not (OGC SWES 2.0 - DeleteSensor operation or not specified DeleteObservation)';


--
-- Name: COLUMN observation.validtimestart; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.validtimestart IS 'Start time stamp for which the observation/result is valid, e.g. used for forecasting. Optional';


--
-- Name: COLUMN observation.validtimeend; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.validtimeend IS 'End time stamp for which the observation/result is valid, e.g. used for forecasting. Optional';


--
-- Name: COLUMN observation.unitid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.unitid IS 'Foreign Key (FK) to the related unit of measure. Contains "unit".unitid. Optional';


--
-- Name: COLUMN observation.samplinggeometry; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observation.samplinggeometry IS 'Sampling geometry describes exactly where the measurement has taken place. Used for OGC SOS 2.0 Spatial Filtering Profile. Optional';


--
-- Name: observationconstellation; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE observationconstellation (
    observationconstellationid bigint NOT NULL,
    observablepropertyid bigint NOT NULL,
    procedureid bigint NOT NULL,
    observationtypeid bigint,
    offeringid bigint NOT NULL,
    deleted character(1) DEFAULT 'F'::bpchar NOT NULL,
    hiddenchild character(1) DEFAULT 'F'::bpchar NOT NULL,
    CONSTRAINT observationconstellation_deleted_check CHECK ((deleted = ANY (ARRAY['T'::bpchar, 'F'::bpchar]))),
    CONSTRAINT observationconstellation_hiddenchild_check CHECK ((hiddenchild = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE observationconstellation OWNER TO docker;

--
-- Name: TABLE observationconstellation; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE observationconstellation IS 'Table to store the ObservationConstellation information. Contains information about the constellation of observableProperty, procedure, offering and the observationType. Mapping file: mapping/core/ObservationConstellation.hbm.xml';


--
-- Name: COLUMN observationconstellation.observationconstellationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.observationconstellationid IS 'Table primary key, used for relations';


--
-- Name: COLUMN observationconstellation.observablepropertyid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.observablepropertyid IS 'Foreign Key (FK) to the related observableProperty. Contains "observableproperty".observablepropertyid';


--
-- Name: COLUMN observationconstellation.procedureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.procedureid IS 'Foreign Key (FK) to the related procedure. Contains "procedure".procedureid';


--
-- Name: COLUMN observationconstellation.observationtypeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.observationtypeid IS 'Foreign Key (FK) to the related observableProperty. Contains "observationtype".observationtypeid';


--
-- Name: COLUMN observationconstellation.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.offeringid IS 'Foreign Key (FK) to the related observableProperty. Contains "offering".offeringid';


--
-- Name: COLUMN observationconstellation.deleted; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.deleted IS 'Flag to indicate that this observationConstellation is deleted or not. Set if the related procedure is deleted via DeleteSensor operation (OGC SWES 2.0 - DeleteSensor operation)';


--
-- Name: COLUMN observationconstellation.hiddenchild; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationconstellation.hiddenchild IS 'Flag to indicate that this observationConstellations procedure is a child procedure of another procedure. If true, the related procedure is not contained in OGC SOS 2.0 Capabilities but in OGC SOS 1.0.0 Capabilities.';


--
-- Name: observationconstellationid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE observationconstellationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE observationconstellationid_seq OWNER TO docker;

--
-- Name: observationhasoffering; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE observationhasoffering (
    observationid bigint NOT NULL,
    offeringid bigint NOT NULL
);


ALTER TABLE observationhasoffering OWNER TO docker;

--
-- Name: TABLE observationhasoffering; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE observationhasoffering IS 'Table to store relations between observation and associated offerings. Mapping file: mapping/ereporting/EReportingObservation.hbm.xml';


--
-- Name: COLUMN observationhasoffering.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationhasoffering.observationid IS 'Foreign Key (FK) to the related observation. Contains "observation".oobservationid';


--
-- Name: COLUMN observationhasoffering.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationhasoffering.offeringid IS 'Foreign Key (FK) to the related offering. Contains "offering".offeringid';


--
-- Name: observationid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE observationid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE observationid_seq OWNER TO docker;

--
-- Name: observationtype; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE observationtype (
    observationtypeid bigint NOT NULL,
    observationtype character varying(255) NOT NULL
);


ALTER TABLE observationtype OWNER TO docker;

--
-- Name: TABLE observationtype; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE observationtype IS 'Table to store the observationTypes. Mapping file: mapping/core/ObservationType.hbm.xml';


--
-- Name: COLUMN observationtype.observationtypeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationtype.observationtypeid IS 'Table primary key, used for relations';


--
-- Name: COLUMN observationtype.observationtype; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN observationtype.observationtype IS 'The observationType value, e.g. http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement (OGC OM 2.0 specification) for OM_Measurement';


--
-- Name: observationtypeid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE observationtypeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE observationtypeid_seq OWNER TO docker;

--
-- Name: offering; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE offering (
    offeringid bigint NOT NULL,
    hibernatediscriminator character(1) NOT NULL,
    identifier character varying(255) NOT NULL,
    codespace bigint,
    name character varying(255),
    codespacename bigint,
    description character varying(255),
    disabled character(1) DEFAULT 'F'::bpchar NOT NULL,
    CONSTRAINT offering_disabled_check CHECK ((disabled = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE offering OWNER TO docker;

--
-- Name: TABLE offering; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE offering IS 'Table to store the offering information. Mapping file: mapping/core/Offering.hbm.xml';


--
-- Name: COLUMN offering.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.offeringid IS 'Table primary key, used for relations';


--
-- Name: COLUMN offering.identifier; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.identifier IS 'The identifier of the offering, gml:identifier. Used as parameter for queries. Unique';


--
-- Name: COLUMN offering.codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.codespace IS 'Relation/foreign key to the codespace table. Contains the gml:identifier codespace. Optional';


--
-- Name: COLUMN offering.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.name IS 'The name of the offering, gml:name. If available, displyed in the contents of the Capabilites. Optional';


--
-- Name: COLUMN offering.codespacename; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.codespacename IS 'Relation/foreign key to the codespace table. Contains the gml:name codespace. Optional';


--
-- Name: COLUMN offering.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.description IS 'Description of the offering, gml:description. Optional';


--
-- Name: COLUMN offering.disabled; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offering.disabled IS 'For later use by the SOS. Indicator if this offering should not be provided by the SOS.';


--
-- Name: offeringallowedfeaturetype; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE offeringallowedfeaturetype (
    offeringid bigint NOT NULL,
    featureofinteresttypeid bigint NOT NULL
);


ALTER TABLE offeringallowedfeaturetype OWNER TO docker;

--
-- Name: TABLE offeringallowedfeaturetype; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE offeringallowedfeaturetype IS 'Table to store relations between offering and allowed featureOfInterestTypes, defined in InsertSensor request. Mapping file: mapping/transactional/TOffering.hbm.xml';


--
-- Name: COLUMN offeringallowedfeaturetype.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offeringallowedfeaturetype.offeringid IS 'Foreign Key (FK) to the related offering. Contains "offering".offeringid';


--
-- Name: COLUMN offeringallowedfeaturetype.featureofinteresttypeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offeringallowedfeaturetype.featureofinteresttypeid IS 'Foreign Key (FK) to the related featureOfInterestTypeId. Contains "featureOfInterestType".featureOfInterestTypeId';


--
-- Name: offeringallowedobservationtype; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE offeringallowedobservationtype (
    offeringid bigint NOT NULL,
    observationtypeid bigint NOT NULL
);


ALTER TABLE offeringallowedobservationtype OWNER TO docker;

--
-- Name: TABLE offeringallowedobservationtype; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE offeringallowedobservationtype IS 'Table to store relations between offering and allowed observationTypes, defined in InsertSensor request. Mapping file: mapping/transactional/TOffering.hbm.xml';


--
-- Name: COLUMN offeringallowedobservationtype.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offeringallowedobservationtype.offeringid IS 'Foreign Key (FK) to the related offering. Contains "offering".offeringid';


--
-- Name: COLUMN offeringallowedobservationtype.observationtypeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offeringallowedobservationtype.observationtypeid IS 'Foreign Key (FK) to the related observationType. Contains "observationType".observationTypeId';


--
-- Name: offeringhasrelatedfeature; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE offeringhasrelatedfeature (
    relatedfeatureid bigint NOT NULL,
    offeringid bigint NOT NULL
);


ALTER TABLE offeringhasrelatedfeature OWNER TO docker;

--
-- Name: TABLE offeringhasrelatedfeature; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE offeringhasrelatedfeature IS 'Table to store relations between offering and associated relatedFeatures. Mapping file: mapping/transactional/TOffering.hbm.xml';


--
-- Name: COLUMN offeringhasrelatedfeature.relatedfeatureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offeringhasrelatedfeature.relatedfeatureid IS 'Foreign Key (FK) to the related relatedFeature. Contains "relatedFeature".relatedFeatureid';


--
-- Name: COLUMN offeringhasrelatedfeature.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN offeringhasrelatedfeature.offeringid IS 'Foreign Key (FK) to the related offering. Contains "offering".offeringid';


--
-- Name: offeringid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE offeringid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE offeringid_seq OWNER TO docker;

--
-- Name: parameter; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE parameter (
    parameterid bigint NOT NULL,
    observationid bigint NOT NULL,
    definition character varying(255) NOT NULL,
    title character varying(255),
    value oid NOT NULL
);


ALTER TABLE parameter OWNER TO docker;

--
-- Name: TABLE parameter; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE parameter IS 'NOT YET USED! Table to store additional obervation information (om:parameter). Mapping file: mapping/transactional/Parameter.hbm.xml';


--
-- Name: COLUMN parameter.parameterid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN parameter.parameterid IS 'Table primary key';


--
-- Name: COLUMN parameter.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN parameter.observationid IS 'Foreign Key (FK) to the related observation. Contains "observation".observationid';


--
-- Name: COLUMN parameter.definition; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN parameter.definition IS 'Definition of the additional information';


--
-- Name: COLUMN parameter.title; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN parameter.title IS 'optional title of the additional information. Optional';


--
-- Name: COLUMN parameter.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN parameter.value IS 'Value of the additional information';


--
-- Name: parameterid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE parameterid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE parameterid_seq OWNER TO docker;

--
-- Name: procdescformatid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE procdescformatid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE procdescformatid_seq OWNER TO docker;

--
-- Name: procedure; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE procedure (
    procedureid bigint NOT NULL,
    hibernatediscriminator character(1) NOT NULL,
    proceduredescriptionformatid bigint NOT NULL,
    identifier character varying(255) NOT NULL,
    codespace bigint,
    name character varying(255),
    codespacename bigint,
    description character varying(255),
    deleted character(1) DEFAULT 'F'::bpchar NOT NULL,
    disabled character(1) DEFAULT 'F'::bpchar NOT NULL,
    descriptionfile text,
    referenceflag character(1) DEFAULT 'F'::bpchar,
    CONSTRAINT procedure_deleted_check CHECK ((deleted = ANY (ARRAY['T'::bpchar, 'F'::bpchar]))),
    CONSTRAINT procedure_disabled_check CHECK ((disabled = ANY (ARRAY['T'::bpchar, 'F'::bpchar]))),
    CONSTRAINT procedure_referenceflag_check CHECK ((referenceflag = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE procedure OWNER TO docker;

--
-- Name: TABLE procedure; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE procedure IS 'Table to store the procedure/sensor. Mapping file: mapping/core/Procedure.hbm.xml';


--
-- Name: COLUMN procedure.procedureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.procedureid IS 'Table primary key, used for relations';


--
-- Name: COLUMN procedure.proceduredescriptionformatid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.proceduredescriptionformatid IS 'Relation/foreign key to the procedureDescriptionFormat table. Describes the format of the procedure description.';


--
-- Name: COLUMN procedure.identifier; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.identifier IS 'The identifier of the procedure, gml:identifier. Used as parameter for queries. Unique';


--
-- Name: COLUMN procedure.codespace; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.codespace IS 'Relation/foreign key to the codespace table. Contains the gml:identifier codespace. Optional';


--
-- Name: COLUMN procedure.name; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.name IS 'The name of the procedure, gml:name. Optional';


--
-- Name: COLUMN procedure.codespacename; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.codespacename IS 'Relation/foreign key to the codespace table. Contains the gml:name codespace. Optional';


--
-- Name: COLUMN procedure.description; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.description IS 'Description of the procedure, gml:description. Optional';


--
-- Name: COLUMN procedure.deleted; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.deleted IS 'Flag to indicate that this procedure is deleted or not (OGC SWES 2.0 - DeleteSensor operation)';


--
-- Name: COLUMN procedure.disabled; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.disabled IS 'For later use by the SOS. Indicator if this procedure should not be provided by the SOS.';


--
-- Name: COLUMN procedure.descriptionfile; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.descriptionfile IS 'Field for full (XML) encoded procedure description or link to a procedure description file. Optional';


--
-- Name: COLUMN procedure.referenceflag; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN procedure.referenceflag IS 'Flag to indicate that this procedure is a reference procedure of another procedure. Not used by the SOS but by the Sensor Web REST-API';


--
-- Name: proceduredescriptionformat; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE proceduredescriptionformat (
    proceduredescriptionformatid bigint NOT NULL,
    proceduredescriptionformat character varying(255) NOT NULL
);


ALTER TABLE proceduredescriptionformat OWNER TO docker;

--
-- Name: TABLE proceduredescriptionformat; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE proceduredescriptionformat IS 'Table to store the ProcedureDescriptionFormat information of procedures. Mapping file: mapping/core/ProcedureDescriptionFormat.hbm.xml';


--
-- Name: COLUMN proceduredescriptionformat.proceduredescriptionformatid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN proceduredescriptionformat.proceduredescriptionformatid IS 'Table primary key, used for relations';


--
-- Name: COLUMN proceduredescriptionformat.proceduredescriptionformat; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN proceduredescriptionformat.proceduredescriptionformat IS 'The procedureDescriptionFormat value, e.g. http://www.opengis.net/sensorML/1.0.1 for procedures descriptions as specified in OGC SensorML 1.0.1';


--
-- Name: procedureid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE procedureid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE procedureid_seq OWNER TO docker;

--
-- Name: relatedfeature; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE relatedfeature (
    relatedfeatureid bigint NOT NULL,
    featureofinterestid bigint NOT NULL
);


ALTER TABLE relatedfeature OWNER TO docker;

--
-- Name: TABLE relatedfeature; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE relatedfeature IS 'Table to store related feature information used in the OGC SOS 2.0 Capabilities (See also OGC SWES 2.0). Mapping file: mapping/transactionl/RelatedFeature.hbm.xml';


--
-- Name: COLUMN relatedfeature.relatedfeatureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN relatedfeature.relatedfeatureid IS 'Table primary key, used for relations';


--
-- Name: COLUMN relatedfeature.featureofinterestid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN relatedfeature.featureofinterestid IS 'Foreign Key (FK) to the related featureOfInterest. Contains "featureOfInterest".featureOfInterestid';


--
-- Name: relatedfeaturehasrole; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE relatedfeaturehasrole (
    relatedfeatureid bigint NOT NULL,
    relatedfeatureroleid bigint NOT NULL
);


ALTER TABLE relatedfeaturehasrole OWNER TO docker;

--
-- Name: TABLE relatedfeaturehasrole; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE relatedfeaturehasrole IS 'Relation table to store relatedFeatures and their associated relatedFeatureRoles. Mapping file: mapping/transactionl/RelatedFeature.hbm.xml';


--
-- Name: COLUMN relatedfeaturehasrole.relatedfeatureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN relatedfeaturehasrole.relatedfeatureid IS 'Foreign Key (FK) to the related relatedFeature. Contains "relatedFeature".relatedFeatureid';


--
-- Name: COLUMN relatedfeaturehasrole.relatedfeatureroleid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN relatedfeaturehasrole.relatedfeatureroleid IS 'Foreign Key (FK) to the related relatedFeatureRole. Contains "relatedFeatureRole".relatedFeatureRoleid';


--
-- Name: relatedfeatureid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE relatedfeatureid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE relatedfeatureid_seq OWNER TO docker;

--
-- Name: relatedfeaturerole; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE relatedfeaturerole (
    relatedfeatureroleid bigint NOT NULL,
    relatedfeaturerole character varying(255) NOT NULL
);


ALTER TABLE relatedfeaturerole OWNER TO docker;

--
-- Name: TABLE relatedfeaturerole; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE relatedfeaturerole IS 'Table to store related feature role information used in the OGC SOS 2.0 Capabilities (See also OGC SWES 2.0). Mapping file: mapping/transactionl/RelatedFeatureRole.hbm.xml';


--
-- Name: COLUMN relatedfeaturerole.relatedfeatureroleid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN relatedfeaturerole.relatedfeatureroleid IS 'Table primary key, used for relations';


--
-- Name: COLUMN relatedfeaturerole.relatedfeaturerole; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN relatedfeaturerole.relatedfeaturerole IS 'The related feature role definition. See OGC SWES 2.0 specification';


--
-- Name: relatedfeatureroleid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE relatedfeatureroleid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE relatedfeatureroleid_seq OWNER TO docker;

--
-- Name: resulttemplate; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE resulttemplate (
    resulttemplateid bigint NOT NULL,
    offeringid bigint NOT NULL,
    observablepropertyid bigint NOT NULL,
    procedureid bigint NOT NULL,
    featureofinterestid bigint NOT NULL,
    identifier character varying(255) NOT NULL,
    resultstructure text NOT NULL,
    resultencoding text NOT NULL
);


ALTER TABLE resulttemplate OWNER TO docker;

--
-- Name: TABLE resulttemplate; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE resulttemplate IS 'Table to store resultTemplates (OGC SOS 2.0 result handling profile). Mapping file: mapping/transactionl/ResultTemplate.hbm.xml';


--
-- Name: COLUMN resulttemplate.resulttemplateid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.resulttemplateid IS 'Table primary key';


--
-- Name: COLUMN resulttemplate.offeringid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.offeringid IS 'Foreign Key (FK) to the related offering. Contains "offering".offeringid';


--
-- Name: COLUMN resulttemplate.observablepropertyid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.observablepropertyid IS 'Foreign Key (FK) to the related observableProperty. Contains "observableProperty".observablePropertyId';


--
-- Name: COLUMN resulttemplate.procedureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.procedureid IS 'Foreign Key (FK) to the related procedure. Contains "procedure".procedureId';


--
-- Name: COLUMN resulttemplate.featureofinterestid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.featureofinterestid IS 'Foreign Key (FK) to the related featureOfInterest. Contains "featureOfInterest".featureOfInterestid';


--
-- Name: COLUMN resulttemplate.identifier; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.identifier IS 'The resultTemplate identifier, required for InsertResult requests.';


--
-- Name: COLUMN resulttemplate.resultstructure; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.resultstructure IS 'The resultStructure as XML string. Describes the types and order of the values in a GetResultResponse/InsertResultRequest';


--
-- Name: COLUMN resulttemplate.resultencoding; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN resulttemplate.resultencoding IS 'The resultEncoding as XML string. Describes the encoding of the values in a GetResultResponse/InsertResultRequest';


--
-- Name: resulttemplateid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE resulttemplateid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE resulttemplateid_seq OWNER TO docker;

--
-- Name: sensorsystem; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE sensorsystem (
    parentsensorid bigint NOT NULL,
    childsensorid bigint NOT NULL
);


ALTER TABLE sensorsystem OWNER TO docker;

--
-- Name: TABLE sensorsystem; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE sensorsystem IS 'Relation table to store procedure hierarchies. E.g. define a parent in a query and all childs are also contained in the response. Mapping file: mapping/transactional/TProcedure.hbm.xml';


--
-- Name: COLUMN sensorsystem.parentsensorid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN sensorsystem.parentsensorid IS 'Foreign Key (FK) to the related parent procedure. Contains "procedure".procedureid';


--
-- Name: COLUMN sensorsystem.childsensorid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN sensorsystem.childsensorid IS 'Foreign Key (FK) to the related child procedure. Contains "procedure".procedureid';


--
-- Name: series; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE series (
    seriesid bigint NOT NULL,
    featureofinterestid bigint NOT NULL,
    observablepropertyid bigint NOT NULL,
    procedureid bigint NOT NULL,
    deleted character(1) DEFAULT 'F'::bpchar NOT NULL,
    published character(1) DEFAULT 'T'::bpchar NOT NULL,
    firsttimestamp timestamp without time zone,
    lasttimestamp timestamp without time zone,
    firstnumericvalue double precision,
    lastnumericvalue double precision,
    unitid bigint,
    CONSTRAINT series_deleted_check CHECK ((deleted = ANY (ARRAY['T'::bpchar, 'F'::bpchar]))),
    CONSTRAINT series_published_check CHECK ((published = ANY (ARRAY['T'::bpchar, 'F'::bpchar])))
);


ALTER TABLE series OWNER TO docker;

--
-- Name: TABLE series; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE series IS 'Table to store a (time-) series which consists of featureOfInterest, observableProperty, and procedure. Mapping file: mapping/series/Series.hbm.xml';


--
-- Name: COLUMN series.seriesid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.seriesid IS 'Table primary key, used for relations';


--
-- Name: COLUMN series.featureofinterestid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.featureofinterestid IS 'Foreign Key (FK) to the related featureOfInterest. Contains "featureOfInterest".featureOfInterestId';


--
-- Name: COLUMN series.observablepropertyid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.observablepropertyid IS 'Foreign Key (FK) to the related observableProperty. Contains "observableproperty".observablepropertyid';


--
-- Name: COLUMN series.procedureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.procedureid IS 'Foreign Key (FK) to the related procedure. Contains "procedure".procedureid';


--
-- Name: COLUMN series.deleted; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.deleted IS 'Flag to indicate that this series is deleted or not. Set if the related procedure is deleted via DeleteSensor operation (OGC SWES 2.0 - DeleteSensor operation)';


--
-- Name: COLUMN series.published; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.published IS 'Flag to indicate that this series is published or not. A not published series is not contained in GetObservation and GetDataAvailability responses';


--
-- Name: COLUMN series.firsttimestamp; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.firsttimestamp IS 'The time stamp of the first (temporal) observation associated to this series';


--
-- Name: COLUMN series.lasttimestamp; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.lasttimestamp IS 'The time stamp of the last (temporal) observation associated to this series';


--
-- Name: COLUMN series.firstnumericvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.firstnumericvalue IS 'The value of the first (temporal) observation associated to this series';


--
-- Name: COLUMN series.lastnumericvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.lastnumericvalue IS 'The value of the last (temporal) observation associated to this series';


--
-- Name: COLUMN series.unitid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN series.unitid IS 'Foreign Key (FK) to the related unit of the first/last numeric values . Contains "unit".unitid';


--
-- Name: seriesid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE seriesid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE seriesid_seq OWNER TO docker;

--
-- Name: swedataarrayvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE swedataarrayvalue (
    observationid bigint NOT NULL,
    value text
);


ALTER TABLE swedataarrayvalue OWNER TO docker;

--
-- Name: TABLE swedataarrayvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE swedataarrayvalue IS 'Value table for SweDataArray observation';


--
-- Name: COLUMN swedataarrayvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN swedataarrayvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN swedataarrayvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN swedataarrayvalue.value IS 'SweDataArray observation value';


--
-- Name: textvalue; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE textvalue (
    observationid bigint NOT NULL,
    value text
);


ALTER TABLE textvalue OWNER TO docker;

--
-- Name: TABLE textvalue; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE textvalue IS 'Value table for text observation';


--
-- Name: COLUMN textvalue.observationid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN textvalue.observationid IS 'Foreign Key (FK) to the related observation from the observation table. Contains "observation".observationid';


--
-- Name: COLUMN textvalue.value; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN textvalue.value IS 'Text observation value';


--
-- Name: unit; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE unit (
    unitid bigint NOT NULL,
    unit character varying(255) NOT NULL
);


ALTER TABLE unit OWNER TO docker;

--
-- Name: TABLE unit; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE unit IS 'Table to store the unit of measure information, used in observations. Mapping file: mapping/core/Unit.hbm.xml';


--
-- Name: COLUMN unit.unitid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN unit.unitid IS 'Table primary key, used for relations';


--
-- Name: COLUMN unit.unit; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN unit.unit IS 'The unit of measure of observations. See http://unitsofmeasure.org/ucum.html';


--
-- Name: unitid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE unitid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE unitid_seq OWNER TO docker;

--
-- Name: validproceduretime; Type: TABLE; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE TABLE validproceduretime (
    validproceduretimeid bigint NOT NULL,
    procedureid bigint NOT NULL,
    proceduredescriptionformatid bigint NOT NULL,
    starttime timestamp without time zone NOT NULL,
    endtime timestamp without time zone,
    descriptionxml text NOT NULL
);


ALTER TABLE validproceduretime OWNER TO docker;

--
-- Name: TABLE validproceduretime; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON TABLE validproceduretime IS 'Table to store procedure descriptions which were inserted or updated via the transactional Profile. Mapping file: mapping/transactionl/ValidProcedureTime.hbm.xml';


--
-- Name: COLUMN validproceduretime.validproceduretimeid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN validproceduretime.validproceduretimeid IS 'Table primary key';


--
-- Name: COLUMN validproceduretime.procedureid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN validproceduretime.procedureid IS 'Foreign Key (FK) to the related procedure. Contains "procedure".procedureid';


--
-- Name: COLUMN validproceduretime.proceduredescriptionformatid; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN validproceduretime.proceduredescriptionformatid IS 'Foreign Key (FK) to the related procedureDescriptionFormat. Contains "procedureDescriptionFormat".procedureDescriptionFormatid';


--
-- Name: COLUMN validproceduretime.starttime; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN validproceduretime.starttime IS 'Timestamp since this procedure description is valid';


--
-- Name: COLUMN validproceduretime.endtime; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN validproceduretime.endtime IS 'Timestamp since this procedure description is invalid';


--
-- Name: COLUMN validproceduretime.descriptionxml; Type: COMMENT; Schema: sos52n1; Owner: docker
--

COMMENT ON COLUMN validproceduretime.descriptionxml IS 'Procedure description as XML string';


--
-- Name: validproceduretimeid_seq; Type: SEQUENCE; Schema: sos52n1; Owner: docker
--

CREATE SEQUENCE validproceduretimeid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE validproceduretimeid_seq OWNER TO docker;

--
-- Data for Name: blobvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY blobvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: booleanvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY booleanvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: categoryvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY categoryvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: codespace; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY codespace (codespaceid, codespace) FROM stdin;
\.


--
-- Name: codespaceid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('codespaceid_seq', 1, false);


--
-- Data for Name: compositephenomenon; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY compositephenomenon (parentobservablepropertyid, childobservablepropertyid) FROM stdin;
\.


--
-- Data for Name: countvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY countvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: featureofinterest; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY featureofinterest (featureofinterestid, hibernatediscriminator, featureofinteresttypeid, identifier, codespace, name, codespacename, description, geom, descriptionxml, url) FROM stdin;
\.


--
-- Name: featureofinterestid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('featureofinterestid_seq', 1, false);


--
-- Data for Name: featureofinteresttype; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY featureofinteresttype (featureofinteresttypeid, featureofinteresttype) FROM stdin;
\.


--
-- Name: featureofinteresttypeid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('featureofinteresttypeid_seq', 1, false);


--
-- Data for Name: featurerelation; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY featurerelation (parentfeatureid, childfeatureid) FROM stdin;
\.


--
-- Data for Name: geometryvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY geometryvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: i18nfeatureofinterest; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY i18nfeatureofinterest (id, objectid, locale, name, description) FROM stdin;
\.


--
-- Name: i18nfeatureofinterestid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('i18nfeatureofinterestid_seq', 1, false);


--
-- Data for Name: i18nobservableproperty; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY i18nobservableproperty (id, objectid, locale, name, description) FROM stdin;
\.


--
-- Name: i18nobspropid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('i18nobspropid_seq', 1, false);


--
-- Data for Name: i18noffering; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY i18noffering (id, objectid, locale, name, description) FROM stdin;
\.


--
-- Name: i18nofferingid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('i18nofferingid_seq', 1, false);


--
-- Data for Name: i18nprocedure; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY i18nprocedure (id, objectid, locale, name, description, shortname, longname) FROM stdin;
\.


--
-- Name: i18nprocedureid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('i18nprocedureid_seq', 1, false);


--
-- Data for Name: numericvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY numericvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: observableproperty; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY observableproperty (observablepropertyid, hibernatediscriminator, identifier, codespace, name, codespacename, description, disabled) FROM stdin;
\.


--
-- Name: observablepropertyid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('observablepropertyid_seq', 1, false);


--
-- Data for Name: observation; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY observation (observationid, seriesid, phenomenontimestart, phenomenontimeend, resulttime, identifier, codespace, name, codespacename, description, deleted, validtimestart, validtimeend, unitid, samplinggeometry) FROM stdin;
\.


--
-- Data for Name: observationconstellation; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY observationconstellation (observationconstellationid, observablepropertyid, procedureid, observationtypeid, offeringid, deleted, hiddenchild) FROM stdin;
\.


--
-- Name: observationconstellationid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('observationconstellationid_seq', 1, false);


--
-- Data for Name: observationhasoffering; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY observationhasoffering (observationid, offeringid) FROM stdin;
\.


--
-- Name: observationid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('observationid_seq', 1, false);


--
-- Data for Name: observationtype; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY observationtype (observationtypeid, observationtype) FROM stdin;
\.


--
-- Name: observationtypeid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('observationtypeid_seq', 1, false);


--
-- Data for Name: offering; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY offering (offeringid, hibernatediscriminator, identifier, codespace, name, codespacename, description, disabled) FROM stdin;
\.


--
-- Data for Name: offeringallowedfeaturetype; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY offeringallowedfeaturetype (offeringid, featureofinteresttypeid) FROM stdin;
\.


--
-- Data for Name: offeringallowedobservationtype; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY offeringallowedobservationtype (offeringid, observationtypeid) FROM stdin;
\.


--
-- Data for Name: offeringhasrelatedfeature; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY offeringhasrelatedfeature (relatedfeatureid, offeringid) FROM stdin;
\.


--
-- Name: offeringid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('offeringid_seq', 1, false);


--
-- Data for Name: parameter; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY parameter (parameterid, observationid, definition, title, value) FROM stdin;
\.


--
-- Name: parameterid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('parameterid_seq', 1, false);


--
-- Name: procdescformatid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('procdescformatid_seq', 1, false);


--
-- Data for Name: procedure; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY procedure (procedureid, hibernatediscriminator, proceduredescriptionformatid, identifier, codespace, name, codespacename, description, deleted, disabled, descriptionfile, referenceflag) FROM stdin;
\.


--
-- Data for Name: proceduredescriptionformat; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY proceduredescriptionformat (proceduredescriptionformatid, proceduredescriptionformat) FROM stdin;
\.


--
-- Name: procedureid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('procedureid_seq', 1, false);


--
-- Data for Name: relatedfeature; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY relatedfeature (relatedfeatureid, featureofinterestid) FROM stdin;
\.


--
-- Data for Name: relatedfeaturehasrole; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY relatedfeaturehasrole (relatedfeatureid, relatedfeatureroleid) FROM stdin;
\.


--
-- Name: relatedfeatureid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('relatedfeatureid_seq', 1, false);


--
-- Data for Name: relatedfeaturerole; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY relatedfeaturerole (relatedfeatureroleid, relatedfeaturerole) FROM stdin;
\.


--
-- Name: relatedfeatureroleid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('relatedfeatureroleid_seq', 1, false);


--
-- Data for Name: resulttemplate; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY resulttemplate (resulttemplateid, offeringid, observablepropertyid, procedureid, featureofinterestid, identifier, resultstructure, resultencoding) FROM stdin;
\.


--
-- Name: resulttemplateid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('resulttemplateid_seq', 1, false);


--
-- Data for Name: sensorsystem; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY sensorsystem (parentsensorid, childsensorid) FROM stdin;
\.


--
-- Data for Name: series; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY series (seriesid, featureofinterestid, observablepropertyid, procedureid, deleted, published, firsttimestamp, lasttimestamp, firstnumericvalue, lastnumericvalue, unitid) FROM stdin;
\.


--
-- Name: seriesid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('seriesid_seq', 1, false);


--
-- Data for Name: swedataarrayvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY swedataarrayvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: textvalue; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY textvalue (observationid, value) FROM stdin;
\.


--
-- Data for Name: unit; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY unit (unitid, unit) FROM stdin;
\.


--
-- Name: unitid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('unitid_seq', 1, false);


--
-- Data for Name: validproceduretime; Type: TABLE DATA; Schema: sos52n1; Owner: docker
--

COPY validproceduretime (validproceduretimeid, procedureid, proceduredescriptionformatid, starttime, endtime, descriptionxml) FROM stdin;
\.


--
-- Name: validproceduretimeid_seq; Type: SEQUENCE SET; Schema: sos52n1; Owner: docker
--

SELECT pg_catalog.setval('validproceduretimeid_seq', 1, false);


--
-- Name: blobvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY blobvalue
    ADD CONSTRAINT blobvalue_pkey PRIMARY KEY (observationid);


--
-- Name: booleanvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY booleanvalue
    ADD CONSTRAINT booleanvalue_pkey PRIMARY KEY (observationid);


--
-- Name: categoryvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY categoryvalue
    ADD CONSTRAINT categoryvalue_pkey PRIMARY KEY (observationid);


--
-- Name: codespace_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY codespace
    ADD CONSTRAINT codespace_pkey PRIMARY KEY (codespaceid);


--
-- Name: codespaceuk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY codespace
    ADD CONSTRAINT codespaceuk UNIQUE (codespace);


--
-- Name: compositephenomenon_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY compositephenomenon
    ADD CONSTRAINT compositephenomenon_pkey PRIMARY KEY (childobservablepropertyid, parentobservablepropertyid);


--
-- Name: countvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY countvalue
    ADD CONSTRAINT countvalue_pkey PRIMARY KEY (observationid);


--
-- Name: featureofinterest_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY featureofinterest
    ADD CONSTRAINT featureofinterest_pkey PRIMARY KEY (featureofinterestid);


--
-- Name: featureofinteresttype_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY featureofinteresttype
    ADD CONSTRAINT featureofinteresttype_pkey PRIMARY KEY (featureofinteresttypeid);


--
-- Name: featurerelation_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY featurerelation
    ADD CONSTRAINT featurerelation_pkey PRIMARY KEY (childfeatureid, parentfeatureid);


--
-- Name: featuretypeuk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY featureofinteresttype
    ADD CONSTRAINT featuretypeuk UNIQUE (featureofinteresttype);


--
-- Name: featureurl; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY featureofinterest
    ADD CONSTRAINT featureurl UNIQUE (url);


--
-- Name: foiidentifieruk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY featureofinterest
    ADD CONSTRAINT foiidentifieruk UNIQUE (identifier);


--
-- Name: geometryvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY geometryvalue
    ADD CONSTRAINT geometryvalue_pkey PRIMARY KEY (observationid);


--
-- Name: i18nfeatureidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18nfeatureofinterest
    ADD CONSTRAINT i18nfeatureidentity UNIQUE (objectid, locale);


--
-- Name: i18nfeatureofinterest_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18nfeatureofinterest
    ADD CONSTRAINT i18nfeatureofinterest_pkey PRIMARY KEY (id);


--
-- Name: i18nobservableproperty_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18nobservableproperty
    ADD CONSTRAINT i18nobservableproperty_pkey PRIMARY KEY (id);


--
-- Name: i18nobspropidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18nobservableproperty
    ADD CONSTRAINT i18nobspropidentity UNIQUE (objectid, locale);


--
-- Name: i18noffering_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18noffering
    ADD CONSTRAINT i18noffering_pkey PRIMARY KEY (id);


--
-- Name: i18nofferingidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18noffering
    ADD CONSTRAINT i18nofferingidentity UNIQUE (objectid, locale);


--
-- Name: i18nprocedure_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18nprocedure
    ADD CONSTRAINT i18nprocedure_pkey PRIMARY KEY (id);


--
-- Name: i18nprocedureidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY i18nprocedure
    ADD CONSTRAINT i18nprocedureidentity UNIQUE (objectid, locale);


--
-- Name: numericvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY numericvalue
    ADD CONSTRAINT numericvalue_pkey PRIMARY KEY (observationid);


--
-- Name: observableproperty_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observableproperty
    ADD CONSTRAINT observableproperty_pkey PRIMARY KEY (observablepropertyid);


--
-- Name: observation_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT observation_pkey PRIMARY KEY (observationid);


--
-- Name: observationconstellation_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observationconstellation
    ADD CONSTRAINT observationconstellation_pkey PRIMARY KEY (observationconstellationid);


--
-- Name: observationhasoffering_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observationhasoffering
    ADD CONSTRAINT observationhasoffering_pkey PRIMARY KEY (observationid, offeringid);


--
-- Name: observationidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT observationidentity UNIQUE (seriesid, phenomenontimestart, phenomenontimeend, resulttime);


--
-- Name: observationtype_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observationtype
    ADD CONSTRAINT observationtype_pkey PRIMARY KEY (observationtypeid);


--
-- Name: observationtypeuk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observationtype
    ADD CONSTRAINT observationtypeuk UNIQUE (observationtype);


--
-- Name: obsidentifieruk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT obsidentifieruk UNIQUE (identifier);


--
-- Name: obsnconstellationidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observationconstellation
    ADD CONSTRAINT obsnconstellationidentity UNIQUE (observablepropertyid, procedureid, offeringid);


--
-- Name: obspropidentifieruk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY observableproperty
    ADD CONSTRAINT obspropidentifieruk UNIQUE (identifier);


--
-- Name: offering_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY offering
    ADD CONSTRAINT offering_pkey PRIMARY KEY (offeringid);


--
-- Name: offeringallowedfeaturetype_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY offeringallowedfeaturetype
    ADD CONSTRAINT offeringallowedfeaturetype_pkey PRIMARY KEY (offeringid, featureofinteresttypeid);


--
-- Name: offeringallowedobservationtype_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY offeringallowedobservationtype
    ADD CONSTRAINT offeringallowedobservationtype_pkey PRIMARY KEY (offeringid, observationtypeid);


--
-- Name: offeringhasrelatedfeature_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY offeringhasrelatedfeature
    ADD CONSTRAINT offeringhasrelatedfeature_pkey PRIMARY KEY (offeringid, relatedfeatureid);


--
-- Name: offidentifieruk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY offering
    ADD CONSTRAINT offidentifieruk UNIQUE (identifier);


--
-- Name: parameter_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY parameter
    ADD CONSTRAINT parameter_pkey PRIMARY KEY (parameterid);


--
-- Name: procdescformatuk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY proceduredescriptionformat
    ADD CONSTRAINT procdescformatuk UNIQUE (proceduredescriptionformat);


--
-- Name: procedure_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY procedure
    ADD CONSTRAINT procedure_pkey PRIMARY KEY (procedureid);


--
-- Name: proceduredescriptionformat_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY proceduredescriptionformat
    ADD CONSTRAINT proceduredescriptionformat_pkey PRIMARY KEY (proceduredescriptionformatid);


--
-- Name: procidentifieruk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY procedure
    ADD CONSTRAINT procidentifieruk UNIQUE (identifier);


--
-- Name: relatedfeature_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY relatedfeature
    ADD CONSTRAINT relatedfeature_pkey PRIMARY KEY (relatedfeatureid);


--
-- Name: relatedfeaturehasrole_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY relatedfeaturehasrole
    ADD CONSTRAINT relatedfeaturehasrole_pkey PRIMARY KEY (relatedfeatureid, relatedfeatureroleid);


--
-- Name: relatedfeaturerole_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY relatedfeaturerole
    ADD CONSTRAINT relatedfeaturerole_pkey PRIMARY KEY (relatedfeatureroleid);


--
-- Name: relfeatroleuk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY relatedfeaturerole
    ADD CONSTRAINT relfeatroleuk UNIQUE (relatedfeaturerole);


--
-- Name: resulttemplate_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY resulttemplate
    ADD CONSTRAINT resulttemplate_pkey PRIMARY KEY (resulttemplateid);


--
-- Name: sensorsystem_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY sensorsystem
    ADD CONSTRAINT sensorsystem_pkey PRIMARY KEY (childsensorid, parentsensorid);


--
-- Name: series_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY series
    ADD CONSTRAINT series_pkey PRIMARY KEY (seriesid);


--
-- Name: seriesidentity; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY series
    ADD CONSTRAINT seriesidentity UNIQUE (featureofinterestid, observablepropertyid, procedureid);


--
-- Name: swedataarrayvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY swedataarrayvalue
    ADD CONSTRAINT swedataarrayvalue_pkey PRIMARY KEY (observationid);


--
-- Name: textvalue_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY textvalue
    ADD CONSTRAINT textvalue_pkey PRIMARY KEY (observationid);


--
-- Name: unit_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY unit
    ADD CONSTRAINT unit_pkey PRIMARY KEY (unitid);


--
-- Name: unituk; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY unit
    ADD CONSTRAINT unituk UNIQUE (unit);


--
-- Name: validproceduretime_pkey; Type: CONSTRAINT; Schema: sos52n1; Owner: docker; Tablespace: 
--

ALTER TABLE ONLY validproceduretime
    ADD CONSTRAINT validproceduretime_pkey PRIMARY KEY (validproceduretimeid);


--
-- Name: i18nfeatureidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX i18nfeatureidx ON i18nfeatureofinterest USING btree (objectid);


--
-- Name: i18nobspropidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX i18nobspropidx ON i18nobservableproperty USING btree (objectid);


--
-- Name: i18nofferingidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX i18nofferingidx ON i18noffering USING btree (objectid);


--
-- Name: i18nprocedureidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX i18nprocedureidx ON i18nprocedure USING btree (objectid);


--
-- Name: obsconstobspropidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsconstobspropidx ON observationconstellation USING btree (observablepropertyid);


--
-- Name: obsconstofferingidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsconstofferingidx ON observationconstellation USING btree (offeringid);


--
-- Name: obsconstprocedureidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsconstprocedureidx ON observationconstellation USING btree (procedureid);


--
-- Name: obshasoffobservationidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obshasoffobservationidx ON observationhasoffering USING btree (observationid);


--
-- Name: obshasoffofferingidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obshasoffofferingidx ON observationhasoffering USING btree (offeringid);


--
-- Name: obsphentimeendidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsphentimeendidx ON observation USING btree (phenomenontimeend);


--
-- Name: obsphentimestartidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsphentimestartidx ON observation USING btree (phenomenontimestart);


--
-- Name: obsresulttimeidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsresulttimeidx ON observation USING btree (resulttime);


--
-- Name: obsseriesidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX obsseriesidx ON observation USING btree (seriesid);


--
-- Name: resulttempeobspropidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX resulttempeobspropidx ON resulttemplate USING btree (observablepropertyid);


--
-- Name: resulttempidentifieridx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX resulttempidentifieridx ON resulttemplate USING btree (identifier);


--
-- Name: resulttempofferingidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX resulttempofferingidx ON resulttemplate USING btree (offeringid);


--
-- Name: resulttempprocedureidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX resulttempprocedureidx ON resulttemplate USING btree (procedureid);


--
-- Name: seriesfeatureidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX seriesfeatureidx ON series USING btree (featureofinterestid);


--
-- Name: seriesobspropidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX seriesobspropidx ON series USING btree (observablepropertyid);


--
-- Name: seriesprocedureidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX seriesprocedureidx ON series USING btree (procedureid);


--
-- Name: validproceduretimeendtimeidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX validproceduretimeendtimeidx ON validproceduretime USING btree (endtime);


--
-- Name: validproceduretimestarttimeidx; Type: INDEX; Schema: sos52n1; Owner: docker; Tablespace: 
--

CREATE INDEX validproceduretimestarttimeidx ON validproceduretime USING btree (starttime);


--
-- Name: featurecodespaceidentifierfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY featureofinterest
    ADD CONSTRAINT featurecodespaceidentifierfk FOREIGN KEY (codespace) REFERENCES codespace(codespaceid);


--
-- Name: featurecodespacenamefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY featureofinterest
    ADD CONSTRAINT featurecodespacenamefk FOREIGN KEY (codespacename) REFERENCES codespace(codespaceid);


--
-- Name: featurefeaturetypefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY featureofinterest
    ADD CONSTRAINT featurefeaturetypefk FOREIGN KEY (featureofinteresttypeid) REFERENCES featureofinteresttype(featureofinteresttypeid);


--
-- Name: featureofinterestchildfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY featurerelation
    ADD CONSTRAINT featureofinterestchildfk FOREIGN KEY (childfeatureid) REFERENCES featureofinterest(featureofinterestid);


--
-- Name: featureofinterestparentfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY featurerelation
    ADD CONSTRAINT featureofinterestparentfk FOREIGN KEY (parentfeatureid) REFERENCES featureofinterest(featureofinterestid);


--
-- Name: fk_6vvrdxvd406n48gkm706ow1pt; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offeringallowedfeaturetype
    ADD CONSTRAINT fk_6vvrdxvd406n48gkm706ow1pt FOREIGN KEY (offeringid) REFERENCES offering(offeringid);


--
-- Name: fk_6ynwkk91xe8p1uibmjt98sog3; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY relatedfeaturehasrole
    ADD CONSTRAINT fk_6ynwkk91xe8p1uibmjt98sog3 FOREIGN KEY (relatedfeatureid) REFERENCES relatedfeature(relatedfeatureid);


--
-- Name: fk_9ex7hawh3dbplkllmw5w3kvej; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observationhasoffering
    ADD CONSTRAINT fk_9ex7hawh3dbplkllmw5w3kvej FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: fk_lkljeohulvu7cr26pduyp5bd0; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offeringallowedobservationtype
    ADD CONSTRAINT fk_lkljeohulvu7cr26pduyp5bd0 FOREIGN KEY (offeringid) REFERENCES offering(offeringid);


--
-- Name: i18nfeaturefeaturefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY i18nfeatureofinterest
    ADD CONSTRAINT i18nfeaturefeaturefk FOREIGN KEY (objectid) REFERENCES featureofinterest(featureofinterestid);


--
-- Name: i18nobspropobspropfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY i18nobservableproperty
    ADD CONSTRAINT i18nobspropobspropfk FOREIGN KEY (objectid) REFERENCES observableproperty(observablepropertyid);


--
-- Name: i18nofferingofferingfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY i18noffering
    ADD CONSTRAINT i18nofferingofferingfk FOREIGN KEY (objectid) REFERENCES offering(offeringid);


--
-- Name: i18nprocedureprocedurefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY i18nprocedure
    ADD CONSTRAINT i18nprocedureprocedurefk FOREIGN KEY (objectid) REFERENCES procedure(procedureid);


--
-- Name: obscodespaceidentifierfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT obscodespaceidentifierfk FOREIGN KEY (codespace) REFERENCES codespace(codespaceid);


--
-- Name: obscodespacenamefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT obscodespacenamefk FOREIGN KEY (codespacename) REFERENCES codespace(codespaceid);


--
-- Name: obsconstobservationiypefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observationconstellation
    ADD CONSTRAINT obsconstobservationiypefk FOREIGN KEY (observationtypeid) REFERENCES observationtype(observationtypeid);


--
-- Name: obsconstobspropfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observationconstellation
    ADD CONSTRAINT obsconstobspropfk FOREIGN KEY (observablepropertyid) REFERENCES observableproperty(observablepropertyid);


--
-- Name: obsconstofferingfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observationconstellation
    ADD CONSTRAINT obsconstofferingfk FOREIGN KEY (offeringid) REFERENCES offering(offeringid);


--
-- Name: observablepropertychildfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY compositephenomenon
    ADD CONSTRAINT observablepropertychildfk FOREIGN KEY (childobservablepropertyid) REFERENCES observableproperty(observablepropertyid);


--
-- Name: observablepropertyparentfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY compositephenomenon
    ADD CONSTRAINT observablepropertyparentfk FOREIGN KEY (parentobservablepropertyid) REFERENCES observableproperty(observablepropertyid);


--
-- Name: observationblobvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY blobvalue
    ADD CONSTRAINT observationblobvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationbooleanvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY booleanvalue
    ADD CONSTRAINT observationbooleanvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationcategoryvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY categoryvalue
    ADD CONSTRAINT observationcategoryvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationcountvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY countvalue
    ADD CONSTRAINT observationcountvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationgeometryvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY geometryvalue
    ADD CONSTRAINT observationgeometryvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationnumericvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY numericvalue
    ADD CONSTRAINT observationnumericvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationofferingfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observationhasoffering
    ADD CONSTRAINT observationofferingfk FOREIGN KEY (offeringid) REFERENCES offering(offeringid);


--
-- Name: observationseriesfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT observationseriesfk FOREIGN KEY (seriesid) REFERENCES series(seriesid);


--
-- Name: observationswedataarrayvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY swedataarrayvalue
    ADD CONSTRAINT observationswedataarrayvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationtextvaluefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY textvalue
    ADD CONSTRAINT observationtextvaluefk FOREIGN KEY (observationid) REFERENCES observation(observationid);


--
-- Name: observationunitfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observation
    ADD CONSTRAINT observationunitfk FOREIGN KEY (unitid) REFERENCES unit(unitid);


--
-- Name: obsnconstprocedurefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observationconstellation
    ADD CONSTRAINT obsnconstprocedurefk FOREIGN KEY (procedureid) REFERENCES procedure(procedureid);


--
-- Name: obspropcodespaceidentifierfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observableproperty
    ADD CONSTRAINT obspropcodespaceidentifierfk FOREIGN KEY (codespace) REFERENCES codespace(codespaceid);


--
-- Name: obspropcodespacenamefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY observableproperty
    ADD CONSTRAINT obspropcodespacenamefk FOREIGN KEY (codespacename) REFERENCES codespace(codespaceid);


--
-- Name: offcodespaceidentifierfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offering
    ADD CONSTRAINT offcodespaceidentifierfk FOREIGN KEY (codespace) REFERENCES codespace(codespaceid);


--
-- Name: offcodespacenamefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offering
    ADD CONSTRAINT offcodespacenamefk FOREIGN KEY (codespacename) REFERENCES codespace(codespaceid);


--
-- Name: offeringfeaturetypefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offeringallowedfeaturetype
    ADD CONSTRAINT offeringfeaturetypefk FOREIGN KEY (featureofinteresttypeid) REFERENCES featureofinteresttype(featureofinteresttypeid);


--
-- Name: offeringobservationtypefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offeringallowedobservationtype
    ADD CONSTRAINT offeringobservationtypefk FOREIGN KEY (observationtypeid) REFERENCES observationtype(observationtypeid);


--
-- Name: offeringrelatedfeaturefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offeringhasrelatedfeature
    ADD CONSTRAINT offeringrelatedfeaturefk FOREIGN KEY (relatedfeatureid) REFERENCES relatedfeature(relatedfeatureid);


--
-- Name: proccodespaceidentifierfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY procedure
    ADD CONSTRAINT proccodespaceidentifierfk FOREIGN KEY (codespace) REFERENCES codespace(codespaceid);


--
-- Name: proccodespacenamefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY procedure
    ADD CONSTRAINT proccodespacenamefk FOREIGN KEY (codespacename) REFERENCES codespace(codespaceid);


--
-- Name: procedurechildfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY sensorsystem
    ADD CONSTRAINT procedurechildfk FOREIGN KEY (childsensorid) REFERENCES procedure(procedureid);


--
-- Name: procedureparenffk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY sensorsystem
    ADD CONSTRAINT procedureparenffk FOREIGN KEY (parentsensorid) REFERENCES procedure(procedureid);


--
-- Name: procprocdescformatfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY procedure
    ADD CONSTRAINT procprocdescformatfk FOREIGN KEY (proceduredescriptionformatid) REFERENCES proceduredescriptionformat(proceduredescriptionformatid);


--
-- Name: relatedfeatrelatedfeatrolefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY relatedfeaturehasrole
    ADD CONSTRAINT relatedfeatrelatedfeatrolefk FOREIGN KEY (relatedfeatureroleid) REFERENCES relatedfeaturerole(relatedfeatureroleid);


--
-- Name: relatedfeaturefeaturefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY relatedfeature
    ADD CONSTRAINT relatedfeaturefeaturefk FOREIGN KEY (featureofinterestid) REFERENCES featureofinterest(featureofinterestid);


--
-- Name: relatedfeatureofferingfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY offeringhasrelatedfeature
    ADD CONSTRAINT relatedfeatureofferingfk FOREIGN KEY (offeringid) REFERENCES offering(offeringid);


--
-- Name: resulttemplatefeatureidx; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY resulttemplate
    ADD CONSTRAINT resulttemplatefeatureidx FOREIGN KEY (featureofinterestid) REFERENCES featureofinterest(featureofinterestid);


--
-- Name: resulttemplateobspropfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY resulttemplate
    ADD CONSTRAINT resulttemplateobspropfk FOREIGN KEY (observablepropertyid) REFERENCES observableproperty(observablepropertyid);


--
-- Name: resulttemplateofferingidx; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY resulttemplate
    ADD CONSTRAINT resulttemplateofferingidx FOREIGN KEY (offeringid) REFERENCES offering(offeringid);


--
-- Name: resulttemplateprocedurefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY resulttemplate
    ADD CONSTRAINT resulttemplateprocedurefk FOREIGN KEY (procedureid) REFERENCES procedure(procedureid);


--
-- Name: seriesfeaturefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY series
    ADD CONSTRAINT seriesfeaturefk FOREIGN KEY (featureofinterestid) REFERENCES featureofinterest(featureofinterestid);


--
-- Name: seriesobpropfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY series
    ADD CONSTRAINT seriesobpropfk FOREIGN KEY (observablepropertyid) REFERENCES observableproperty(observablepropertyid);


--
-- Name: seriesprocedurefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY series
    ADD CONSTRAINT seriesprocedurefk FOREIGN KEY (procedureid) REFERENCES procedure(procedureid);


--
-- Name: seriesunitfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY series
    ADD CONSTRAINT seriesunitfk FOREIGN KEY (unitid) REFERENCES unit(unitid);


--
-- Name: validproceduretimeprocedurefk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY validproceduretime
    ADD CONSTRAINT validproceduretimeprocedurefk FOREIGN KEY (procedureid) REFERENCES procedure(procedureid);


--
-- Name: validprocprocdescformatfk; Type: FK CONSTRAINT; Schema: sos52n1; Owner: docker
--

ALTER TABLE ONLY validproceduretime
    ADD CONSTRAINT validprocprocdescformatfk FOREIGN KEY (proceduredescriptionformatid) REFERENCES proceduredescriptionformat(proceduredescriptionformatid);


--
-- PostgreSQL database dump complete
--

