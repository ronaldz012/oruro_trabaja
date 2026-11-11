--
-- PostgreSQL database dump
--

\restrict eIxFf9EpuVu1Y8aOwlFz4JeeY2R9pP6RVplGdtFTtaVZoVMrO2T7gRptI6SxZyO

-- Dumped from database version 18.4 (Debian 18.4-1.pgdg13+1)
-- Dumped by pg_dump version 18.4 (Debian 18.4-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_user_id_92473840_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissio_permission_id_6d08dcd2_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_role_id_1900a745_fk_roles_id;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_user_id_f500bee5_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_group_id_2f3517aa_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.postulante_profiles DROP CONSTRAINT IF EXISTS postulante_profiles_user_id_c041dc85_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.postulante_profiles DROP CONSTRAINT IF EXISTS postulante_profiles_profesion_id_8e0c0516_fk_profesiones_id;
ALTER TABLE IF EXISTS ONLY public.postulante_idiomas DROP CONSTRAINT IF EXISTS postulante_idiomas_profile_id_37040d5a_fk_postulant;
ALTER TABLE IF EXISTS ONLY public.postulante_idiomas DROP CONSTRAINT IF EXISTS postulante_idiomas_idioma_id_aa9f19ae_fk_idiomas_id;
ALTER TABLE IF EXISTS ONLY public.postulante_habilidades DROP CONSTRAINT IF EXISTS postulante_habilidades_habilidad_id_f6f3cf3e_fk_habilidades_id;
ALTER TABLE IF EXISTS ONLY public.postulante_habilidades DROP CONSTRAINT IF EXISTS postulante_habilidad_profile_id_e3309758_fk_postulant;
ALTER TABLE IF EXISTS ONLY public.postulaciones DROP CONSTRAINT IF EXISTS postulaciones_postulante_id_b169e96a_fk_postulante_profiles_id;
ALTER TABLE IF EXISTS ONLY public.postulaciones DROP CONSTRAINT IF EXISTS postulaciones_oferta_id_37c23232_fk_ofertas_id;
ALTER TABLE IF EXISTS ONLY public.ofertas DROP CONSTRAINT IF EXISTS ofertas_tipo_contrato_id_b3721731_fk_tipos_contrato_id;
ALTER TABLE IF EXISTS ONLY public.ofertas DROP CONSTRAINT IF EXISTS ofertas_revisada_por_id_af24498c_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.ofertas_profesiones DROP CONSTRAINT IF EXISTS ofertas_profesiones_profesion_id_c52380fe_fk_profesiones_id;
ALTER TABLE IF EXISTS ONLY public.ofertas_profesiones DROP CONSTRAINT IF EXISTS ofertas_profesiones_oferta_id_d43cdd60_fk_ofertas_id;
ALTER TABLE IF EXISTS ONLY public.ofertas DROP CONSTRAINT IF EXISTS ofertas_modalidad_id_2ce5f626_fk_modalidades_id;
ALTER TABLE IF EXISTS ONLY public.ofertas_guardadas DROP CONSTRAINT IF EXISTS ofertas_guardadas_postulante_id_aa9b88fb_fk_postulant;
ALTER TABLE IF EXISTS ONLY public.ofertas_guardadas DROP CONSTRAINT IF EXISTS ofertas_guardadas_oferta_id_687ff106_fk_ofertas_id;
ALTER TABLE IF EXISTS ONLY public.ofertas DROP CONSTRAINT IF EXISTS ofertas_empresa_id_57a168b1_fk_empresas_id;
ALTER TABLE IF EXISTS ONLY public.ofertas DROP CONSTRAINT IF EXISTS ofertas_departamento_id_aadaefa1_fk_departamentos_id;
ALTER TABLE IF EXISTS ONLY public.oferta_habilidades DROP CONSTRAINT IF EXISTS oferta_habilidades_oferta_id_91954529_fk_ofertas_id;
ALTER TABLE IF EXISTS ONLY public.oferta_habilidades DROP CONSTRAINT IF EXISTS oferta_habilidades_habilidad_id_a0ab4903_fk_habilidades_id;
ALTER TABLE IF EXISTS ONLY public.formaciones DROP CONSTRAINT IF EXISTS formaciones_profile_id_2a436406_fk_postulante_profiles_id;
ALTER TABLE IF EXISTS ONLY public.experiencias DROP CONSTRAINT IF EXISTS experiencias_profile_id_083d5d7f_fk_postulante_profiles_id;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_user_id_cf30b035_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_rubro_id_0ca0be2a_fk_rubros_id;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_revisada_por_id_78b8567c_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.codigos_otp DROP CONSTRAINT IF EXISTS codigos_otp_user_id_93000663_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.codigos_otp DROP CONSTRAINT IF EXISTS codigos_otp_registro_pendiente_i_9c14ca23_fk_registros;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.audit_auditlog DROP CONSTRAINT IF EXISTS audit_auditlog_usuario_id_7754169a_fk_users_id;
DROP INDEX IF EXISTS public.users_user_permissions_user_id_92473840;
DROP INDEX IF EXISTS public.users_user_permissions_permission_id_6d08dcd2;
DROP INDEX IF EXISTS public.users_role_id_1900a745;
DROP INDEX IF EXISTS public.users_groups_user_id_f500bee5;
DROP INDEX IF EXISTS public.users_groups_group_id_2f3517aa;
DROP INDEX IF EXISTS public.users_email_0ea73cca_like;
DROP INDEX IF EXISTS public.users_celular_233cc330_like;
DROP INDEX IF EXISTS public.tipos_contrato_nombre_8bb9a70d_like;
DROP INDEX IF EXISTS public.rubros_nombre_8ba97d42_like;
DROP INDEX IF EXISTS public.roles_codigo_64af986f_like;
DROP INDEX IF EXISTS public.registros_pendientes_celular_a3c1a3e7_like;
DROP INDEX IF EXISTS public.registros_p_expira__59b079_idx;
DROP INDEX IF EXISTS public.registros_p_email_4de006_idx;
DROP INDEX IF EXISTS public.registros_p_ci_74e63d_idx;
DROP INDEX IF EXISTS public.profesiones_nombre_2c6b85ce_like;
DROP INDEX IF EXISTS public.postulante_profiles_profesion_id_8e0c0516;
DROP INDEX IF EXISTS public.postulante_profiles_ci_6b8b9fe3_like;
DROP INDEX IF EXISTS public.postulante_idiomas_profile_id_37040d5a;
DROP INDEX IF EXISTS public.postulante_idiomas_idioma_id_aa9f19ae;
DROP INDEX IF EXISTS public.postulante_habilidades_profile_id_e3309758;
DROP INDEX IF EXISTS public.postulante_habilidades_habilidad_id_f6f3cf3e;
DROP INDEX IF EXISTS public.postulaciones_postulante_id_b169e96a;
DROP INDEX IF EXISTS public.postulaciones_oferta_id_37c23232;
DROP INDEX IF EXISTS public.postulaciones_estado_f77dd568_like;
DROP INDEX IF EXISTS public.postulaciones_estado_f77dd568;
DROP INDEX IF EXISTS public.ofertas_tipo_contrato_id_b3721731;
DROP INDEX IF EXISTS public.ofertas_revisada_por_id_af24498c;
DROP INDEX IF EXISTS public.ofertas_profesiones_profesion_id_c52380fe;
DROP INDEX IF EXISTS public.ofertas_profesiones_oferta_id_d43cdd60;
DROP INDEX IF EXISTS public.ofertas_modalidad_id_2ce5f626;
DROP INDEX IF EXISTS public.ofertas_guardadas_postulante_id_aa9b88fb;
DROP INDEX IF EXISTS public.ofertas_guardadas_oferta_id_687ff106;
DROP INDEX IF EXISTS public.ofertas_estado_44ebe942_like;
DROP INDEX IF EXISTS public.ofertas_estado_44ebe942;
DROP INDEX IF EXISTS public.ofertas_empresa_id_57a168b1;
DROP INDEX IF EXISTS public.ofertas_departamento_id_aadaefa1;
DROP INDEX IF EXISTS public.oferta_habilidades_oferta_id_91954529;
DROP INDEX IF EXISTS public.oferta_habilidades_habilidad_id_a0ab4903;
DROP INDEX IF EXISTS public.modalidades_nombre_64734915_like;
DROP INDEX IF EXISTS public.idiomas_nombre_7f8f4369_like;
DROP INDEX IF EXISTS public.habilidades_nombre_c32cfed8_like;
DROP INDEX IF EXISTS public.formaciones_profile_id_2a436406;
DROP INDEX IF EXISTS public.experiencias_profile_id_083d5d7f;
DROP INDEX IF EXISTS public.empresas_rubro_id_0ca0be2a;
DROP INDEX IF EXISTS public.empresas_revisada_por_id_78b8567c;
DROP INDEX IF EXISTS public.empresas_nit_5a5af0f1_like;
DROP INDEX IF EXISTS public.empresas_estado_2f40fdd1_like;
DROP INDEX IF EXISTS public.empresas_estado_2f40fdd1;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.departamentos_nombre_ee12a90a_like;
DROP INDEX IF EXISTS public.codigos_otp_user_id_abc3cc_idx;
DROP INDEX IF EXISTS public.codigos_otp_user_id_93000663;
DROP INDEX IF EXISTS public.codigos_otp_registro_pendiente_id_9c14ca23;
DROP INDEX IF EXISTS public.codigos_otp_registr_d04816_idx;
DROP INDEX IF EXISTS public.codigos_otp_ip_3b5cc9_idx;
DROP INDEX IF EXISTS public.codigos_otp_celular_e9c792_idx;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.audit_auditlog_usuario_id_7754169a;
DROP INDEX IF EXISTS public.audit_auditlog_fecha_3639eaad;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_user_id_permission_id_3b86cbdf_uniq;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_user_id_group_id_fc7788e8_uniq;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_celular_key;
ALTER TABLE IF EXISTS ONLY public.postulaciones DROP CONSTRAINT IF EXISTS unique_postulacion_por_oferta;
ALTER TABLE IF EXISTS ONLY public.ofertas_guardadas DROP CONSTRAINT IF EXISTS unique_oferta_guardada_por_postulante;
ALTER TABLE IF EXISTS ONLY public.postulante_idiomas DROP CONSTRAINT IF EXISTS unique_idioma_por_postulante;
ALTER TABLE IF EXISTS ONLY public.postulante_habilidades DROP CONSTRAINT IF EXISTS unique_habilidad_por_postulante;
ALTER TABLE IF EXISTS ONLY public.oferta_habilidades DROP CONSTRAINT IF EXISTS unique_habilidad_por_oferta;
ALTER TABLE IF EXISTS ONLY public.tipos_contrato DROP CONSTRAINT IF EXISTS tipos_contrato_pkey;
ALTER TABLE IF EXISTS ONLY public.tipos_contrato DROP CONSTRAINT IF EXISTS tipos_contrato_nombre_key;
ALTER TABLE IF EXISTS ONLY public.rubros DROP CONSTRAINT IF EXISTS rubros_pkey;
ALTER TABLE IF EXISTS ONLY public.rubros DROP CONSTRAINT IF EXISTS rubros_nombre_key;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_pkey;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_codigo_key;
ALTER TABLE IF EXISTS ONLY public.registros_pendientes DROP CONSTRAINT IF EXISTS registros_pendientes_pkey;
ALTER TABLE IF EXISTS ONLY public.registros_pendientes DROP CONSTRAINT IF EXISTS registros_pendientes_celular_key;
ALTER TABLE IF EXISTS ONLY public.profesiones DROP CONSTRAINT IF EXISTS profesiones_pkey;
ALTER TABLE IF EXISTS ONLY public.profesiones DROP CONSTRAINT IF EXISTS profesiones_nombre_key;
ALTER TABLE IF EXISTS ONLY public.postulante_profiles DROP CONSTRAINT IF EXISTS postulante_profiles_user_id_key;
ALTER TABLE IF EXISTS ONLY public.postulante_profiles DROP CONSTRAINT IF EXISTS postulante_profiles_pkey;
ALTER TABLE IF EXISTS ONLY public.postulante_profiles DROP CONSTRAINT IF EXISTS postulante_profiles_ci_key;
ALTER TABLE IF EXISTS ONLY public.postulante_idiomas DROP CONSTRAINT IF EXISTS postulante_idiomas_pkey;
ALTER TABLE IF EXISTS ONLY public.postulante_habilidades DROP CONSTRAINT IF EXISTS postulante_habilidades_pkey;
ALTER TABLE IF EXISTS ONLY public.postulaciones DROP CONSTRAINT IF EXISTS postulaciones_pkey;
ALTER TABLE IF EXISTS ONLY public.ofertas_profesiones DROP CONSTRAINT IF EXISTS ofertas_profesiones_pkey;
ALTER TABLE IF EXISTS ONLY public.ofertas_profesiones DROP CONSTRAINT IF EXISTS ofertas_profesiones_oferta_id_profesion_id_f93c8bc8_uniq;
ALTER TABLE IF EXISTS ONLY public.ofertas DROP CONSTRAINT IF EXISTS ofertas_pkey;
ALTER TABLE IF EXISTS ONLY public.ofertas_guardadas DROP CONSTRAINT IF EXISTS ofertas_guardadas_pkey;
ALTER TABLE IF EXISTS ONLY public.oferta_habilidades DROP CONSTRAINT IF EXISTS oferta_habilidades_pkey;
ALTER TABLE IF EXISTS ONLY public.modalidades DROP CONSTRAINT IF EXISTS modalidades_pkey;
ALTER TABLE IF EXISTS ONLY public.modalidades DROP CONSTRAINT IF EXISTS modalidades_nombre_key;
ALTER TABLE IF EXISTS ONLY public.idiomas DROP CONSTRAINT IF EXISTS idiomas_pkey;
ALTER TABLE IF EXISTS ONLY public.idiomas DROP CONSTRAINT IF EXISTS idiomas_nombre_key;
ALTER TABLE IF EXISTS ONLY public.habilidades DROP CONSTRAINT IF EXISTS habilidades_pkey;
ALTER TABLE IF EXISTS ONLY public.habilidades DROP CONSTRAINT IF EXISTS habilidades_nombre_key;
ALTER TABLE IF EXISTS ONLY public.formaciones DROP CONSTRAINT IF EXISTS formaciones_pkey;
ALTER TABLE IF EXISTS ONLY public.experiencias DROP CONSTRAINT IF EXISTS experiencias_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_user_id_key;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_pkey;
ALTER TABLE IF EXISTS ONLY public.empresas DROP CONSTRAINT IF EXISTS empresas_nit_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS departamentos_pkey;
ALTER TABLE IF EXISTS ONLY public.departamentos DROP CONSTRAINT IF EXISTS departamentos_nombre_key;
ALTER TABLE IF EXISTS ONLY public.codigos_otp DROP CONSTRAINT IF EXISTS codigos_otp_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.audit_auditlog DROP CONSTRAINT IF EXISTS audit_auditlog_pkey;
DROP TABLE IF EXISTS public.users_user_permissions;
DROP TABLE IF EXISTS public.users_groups;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.tipos_contrato;
DROP TABLE IF EXISTS public.rubros;
DROP TABLE IF EXISTS public.roles;
DROP TABLE IF EXISTS public.registros_pendientes;
DROP TABLE IF EXISTS public.profesiones;
DROP TABLE IF EXISTS public.postulante_profiles;
DROP TABLE IF EXISTS public.postulante_idiomas;
DROP TABLE IF EXISTS public.postulante_habilidades;
DROP TABLE IF EXISTS public.postulaciones;
DROP TABLE IF EXISTS public.ofertas_profesiones;
DROP TABLE IF EXISTS public.ofertas_guardadas;
DROP TABLE IF EXISTS public.ofertas;
DROP TABLE IF EXISTS public.oferta_habilidades;
DROP TABLE IF EXISTS public.modalidades;
DROP TABLE IF EXISTS public.idiomas;
DROP TABLE IF EXISTS public.habilidades;
DROP TABLE IF EXISTS public.formaciones;
DROP TABLE IF EXISTS public.experiencias;
DROP TABLE IF EXISTS public.empresas;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.departamentos;
DROP TABLE IF EXISTS public.codigos_otp;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.audit_auditlog;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_auditlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_auditlog (
    id bigint NOT NULL,
    accion character varying(20) NOT NULL,
    tabla character varying(64) NOT NULL,
    registro_id integer,
    datos_antes jsonb,
    datos_despues jsonb,
    ip inet,
    fecha timestamp with time zone NOT NULL,
    usuario_id bigint,
    CONSTRAINT audit_auditlog_registro_id_check CHECK ((registro_id >= 0))
);


ALTER TABLE public.audit_auditlog OWNER TO postgres;

--
-- Name: audit_auditlog_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.audit_auditlog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.audit_auditlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: codigos_otp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.codigos_otp (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    celular character varying(20) NOT NULL,
    codigo_hash character varying(128) NOT NULL,
    proposito character varying(20) NOT NULL,
    expira_en timestamp with time zone NOT NULL,
    intentos smallint NOT NULL,
    consumido_en timestamp with time zone,
    ip inet,
    user_id bigint,
    registro_pendiente_id uuid,
    CONSTRAINT codigos_otp_intentos_check CHECK ((intentos >= 0))
);


ALTER TABLE public.codigos_otp OWNER TO postgres;

--
-- Name: codigos_otp_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.codigos_otp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.codigos_otp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: departamentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departamentos (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.departamentos OWNER TO postgres;

--
-- Name: departamentos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.departamentos ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.departamentos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: empresas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.empresas (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nit character varying(20) NOT NULL,
    razon_social character varying(200) NOT NULL,
    representante_nombres character varying(150) NOT NULL,
    representante_apellidos character varying(150) NOT NULL,
    representante_ci character varying(20) NOT NULL,
    direccion character varying(255) NOT NULL,
    logo character varying(100) NOT NULL,
    descripcion text NOT NULL,
    estado character varying(30) NOT NULL,
    motivo_rechazo text NOT NULL,
    revisada_en timestamp with time zone,
    revisada_por_id bigint,
    rubro_id bigint NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.empresas OWNER TO postgres;

--
-- Name: empresas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.empresas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.empresas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: experiencias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.experiencias (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    empresa character varying(160) NOT NULL,
    cargo character varying(160) NOT NULL,
    anos smallint NOT NULL,
    descripcion text NOT NULL,
    profile_id bigint NOT NULL,
    CONSTRAINT experiencias_anos_check CHECK ((anos >= 0))
);


ALTER TABLE public.experiencias OWNER TO postgres;

--
-- Name: experiencias_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.experiencias ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.experiencias_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: formaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formaciones (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    titulo character varying(160) NOT NULL,
    institucion character varying(160) NOT NULL,
    anio_titulacion smallint NOT NULL,
    nro_titulo character varying(60) NOT NULL,
    profile_id bigint NOT NULL,
    CONSTRAINT formaciones_anio_titulacion_check CHECK ((anio_titulacion >= 0))
);


ALTER TABLE public.formaciones OWNER TO postgres;

--
-- Name: formaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.formaciones ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.formaciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: habilidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.habilidades (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(120) NOT NULL
);


ALTER TABLE public.habilidades OWNER TO postgres;

--
-- Name: habilidades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.habilidades ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.habilidades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: idiomas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.idiomas (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.idiomas OWNER TO postgres;

--
-- Name: idiomas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.idiomas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.idiomas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: modalidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modalidades (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.modalidades OWNER TO postgres;

--
-- Name: modalidades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.modalidades ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.modalidades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oferta_habilidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oferta_habilidades (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    obligatoria boolean NOT NULL,
    habilidad_id bigint NOT NULL,
    oferta_id bigint NOT NULL
);


ALTER TABLE public.oferta_habilidades OWNER TO postgres;

--
-- Name: oferta_habilidades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.oferta_habilidades ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.oferta_habilidades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ofertas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ofertas (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    titulo character varying(200) NOT NULL,
    descripcion text NOT NULL,
    requisitos_obligatorios text NOT NULL,
    requisitos_deseables text NOT NULL,
    anos_experiencia smallint NOT NULL,
    municipio character varying(120) NOT NULL,
    salario_min numeric(12,2),
    salario_max numeric(12,2),
    a_tratar boolean NOT NULL,
    beneficios text NOT NULL,
    fecha_cierre date NOT NULL,
    plazas smallint NOT NULL,
    vistas integer NOT NULL,
    estado character varying(30) NOT NULL,
    motivo_revision text NOT NULL,
    publicada_en timestamp with time zone,
    revisada_en timestamp with time zone,
    departamento_id bigint NOT NULL,
    empresa_id bigint NOT NULL,
    modalidad_id bigint NOT NULL,
    revisada_por_id bigint,
    tipo_contrato_id bigint NOT NULL,
    CONSTRAINT ofertas_anos_experiencia_check CHECK ((anos_experiencia >= 0)),
    CONSTRAINT ofertas_plazas_check CHECK ((plazas >= 0)),
    CONSTRAINT ofertas_vistas_check CHECK ((vistas >= 0))
);


ALTER TABLE public.ofertas OWNER TO postgres;

--
-- Name: ofertas_guardadas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ofertas_guardadas (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    oferta_id bigint NOT NULL,
    postulante_id bigint NOT NULL
);


ALTER TABLE public.ofertas_guardadas OWNER TO postgres;

--
-- Name: ofertas_guardadas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.ofertas_guardadas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.ofertas_guardadas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ofertas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.ofertas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.ofertas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ofertas_profesiones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ofertas_profesiones (
    id bigint NOT NULL,
    oferta_id bigint NOT NULL,
    profesion_id bigint NOT NULL
);


ALTER TABLE public.ofertas_profesiones OWNER TO postgres;

--
-- Name: ofertas_profesiones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.ofertas_profesiones ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.ofertas_profesiones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: postulaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postulaciones (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    estado character varying(20) NOT NULL,
    visto_en timestamp with time zone,
    oferta_id bigint NOT NULL,
    postulante_id bigint NOT NULL
);


ALTER TABLE public.postulaciones OWNER TO postgres;

--
-- Name: postulaciones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.postulaciones ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.postulaciones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: postulante_habilidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postulante_habilidades (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nivel character varying(20) NOT NULL,
    habilidad_id bigint NOT NULL,
    profile_id bigint NOT NULL
);


ALTER TABLE public.postulante_habilidades OWNER TO postgres;

--
-- Name: postulante_habilidades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.postulante_habilidades ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.postulante_habilidades_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: postulante_idiomas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postulante_idiomas (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nivel character varying(20) NOT NULL,
    idioma_id bigint NOT NULL,
    profile_id bigint NOT NULL
);


ALTER TABLE public.postulante_idiomas OWNER TO postgres;

--
-- Name: postulante_idiomas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.postulante_idiomas ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.postulante_idiomas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: postulante_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.postulante_profiles (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    ci character varying(20) NOT NULL,
    foto character varying(100) NOT NULL,
    direccion character varying(255) NOT NULL,
    fecha_nacimiento date,
    presentacion text NOT NULL,
    cv character varying(100) NOT NULL,
    profesion_id bigint,
    user_id bigint NOT NULL
);


ALTER TABLE public.postulante_profiles OWNER TO postgres;

--
-- Name: postulante_profiles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.postulante_profiles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.postulante_profiles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: profesiones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.profesiones (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(120) NOT NULL
);


ALTER TABLE public.profesiones OWNER TO postgres;

--
-- Name: profesiones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.profesiones ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.profesiones_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: registros_pendientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.registros_pendientes (
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    ci character varying(20) NOT NULL,
    nombres character varying(150) NOT NULL,
    apellidos character varying(150) NOT NULL,
    celular character varying(20) NOT NULL,
    email character varying(254) NOT NULL,
    password_hash character varying(128) NOT NULL,
    expira_en timestamp with time zone NOT NULL,
    ip inet
);


ALTER TABLE public.registros_pendientes OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id bigint NOT NULL,
    codigo character varying(20) NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.roles ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: rubros; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rubros (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(120) NOT NULL
);


ALTER TABLE public.rubros OWNER TO postgres;

--
-- Name: rubros_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.rubros ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.rubros_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tipos_contrato; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_contrato (
    id bigint NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.tipos_contrato OWNER TO postgres;

--
-- Name: tipos_contrato_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.tipos_contrato ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tipos_contrato_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    celular character varying(20),
    celular_verificado boolean NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.users_groups OWNER TO postgres;

--
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_user_permissions OWNER TO postgres;

--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: audit_auditlog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_auditlog (id, accion, tabla, registro_id, datos_antes, datos_despues, ip, fecha, usuario_id) FROM stdin;
1	CREAR	users	1	\N	{"rol": "SUPERADMIN"}	\N	2026-11-11 01:21:48.245943+00	1
2	CREAR	users	2	\N	{"rol": "EMPRESA"}	\N	2026-11-11 01:21:48.464786+00	2
3	CREAR	users	3	\N	{"rol": "POSTULANTE"}	\N	2026-11-11 01:21:48.686258+00	3
4	CREAR	empresas	1	\N	{"estado": "PENDIENTE_VALIDACION"}	\N	2026-11-11 01:21:50.658366+00	2
5	CAMBIO_ESTADO	empresas	1	{"estado": "PENDIENTE_VALIDACION", "motivo": ""}	{"estado": "APROBADA", "motivo": ""}	\N	2026-11-11 01:21:50.659452+00	1
6	CREAR	empresas	2	\N	{"estado": "PENDIENTE_VALIDACION"}	\N	2026-11-11 01:21:50.884992+00	4
7	CREAR	ofertas	1	\N	{"estado": "EN_REVISION_GADOR"}	\N	2026-11-11 01:21:51.381824+00	2
8	CAMBIO_ESTADO	ofertas	1	{"estado": "EN_REVISION_GADOR", "motivo": ""}	{"estado": "PUBLICADA", "motivo": ""}	\N	2026-11-11 01:21:51.382968+00	1
9	CREAR	ofertas	2	\N	{"estado": "EN_REVISION_GADOR"}	\N	2026-11-11 01:21:51.384092+00	2
10	CREAR	ofertas	3	\N	{"estado": "BORRADOR"}	\N	2026-11-11 01:21:51.38518+00	2
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Rol	8	add_role
22	Can change Rol	8	change_role
23	Can delete Rol	8	delete_role
24	Can view Rol	8	view_role
25	Can add Usuario	9	add_user
26	Can change Usuario	9	change_user
27	Can delete Usuario	9	delete_user
28	Can view Usuario	9	view_user
29	Can add Registro pendiente	7	add_registropendiente
30	Can change Registro pendiente	7	change_registropendiente
31	Can delete Registro pendiente	7	delete_registropendiente
32	Can view Registro pendiente	7	view_registropendiente
33	Can add Código OTP	6	add_codigootp
34	Can change Código OTP	6	change_codigootp
35	Can delete Código OTP	6	delete_codigootp
36	Can view Código OTP	6	view_codigootp
37	Can add registro de auditoría	10	add_auditlog
38	Can change registro de auditoría	10	change_auditlog
39	Can delete registro de auditoría	10	delete_auditlog
40	Can view registro de auditoría	10	view_auditlog
41	Can add Departamento	11	add_departamento
42	Can change Departamento	11	change_departamento
43	Can delete Departamento	11	delete_departamento
44	Can view Departamento	11	view_departamento
45	Can add Habilidad	12	add_habilidad
46	Can change Habilidad	12	change_habilidad
47	Can delete Habilidad	12	delete_habilidad
48	Can view Habilidad	12	view_habilidad
49	Can add Idioma	13	add_idioma
50	Can change Idioma	13	change_idioma
51	Can delete Idioma	13	delete_idioma
52	Can view Idioma	13	view_idioma
53	Can add Modalidad	14	add_modalidad
54	Can change Modalidad	14	change_modalidad
55	Can delete Modalidad	14	delete_modalidad
56	Can view Modalidad	14	view_modalidad
57	Can add Profesión	15	add_profesion
58	Can change Profesión	15	change_profesion
59	Can delete Profesión	15	delete_profesion
60	Can view Profesión	15	view_profesion
61	Can add Rubro	16	add_rubro
62	Can change Rubro	16	change_rubro
63	Can delete Rubro	16	delete_rubro
64	Can view Rubro	16	view_rubro
65	Can add Tipo de contrato	17	add_tipocontrato
66	Can change Tipo de contrato	17	change_tipocontrato
67	Can delete Tipo de contrato	17	delete_tipocontrato
68	Can view Tipo de contrato	17	view_tipocontrato
69	Can add Empresa	18	add_empresa
70	Can change Empresa	18	change_empresa
71	Can delete Empresa	18	delete_empresa
72	Can view Empresa	18	view_empresa
73	Can add Oferta	19	add_oferta
74	Can change Oferta	19	change_oferta
75	Can delete Oferta	19	delete_oferta
76	Can view Oferta	19	view_oferta
77	Can add Habilidad de la oferta	21	add_ofertahabilidad
78	Can change Habilidad de la oferta	21	change_ofertahabilidad
79	Can delete Habilidad de la oferta	21	delete_ofertahabilidad
80	Can view Habilidad de la oferta	21	view_ofertahabilidad
81	Can add Postulación	22	add_postulacion
82	Can change Postulación	22	change_postulacion
83	Can delete Postulación	22	delete_postulacion
84	Can view Postulación	22	view_postulacion
85	Can add Oferta guardada	20	add_ofertaguardada
86	Can change Oferta guardada	20	change_ofertaguardada
87	Can delete Oferta guardada	20	delete_ofertaguardada
88	Can view Oferta guardada	20	view_ofertaguardada
89	Can add Perfil de postulante	27	add_postulanteprofile
90	Can change Perfil de postulante	27	change_postulanteprofile
91	Can delete Perfil de postulante	27	delete_postulanteprofile
92	Can view Perfil de postulante	27	view_postulanteprofile
93	Can add Formación académica	24	add_formacion
94	Can change Formación académica	24	change_formacion
95	Can delete Formación académica	24	delete_formacion
96	Can view Formación académica	24	view_formacion
97	Can add Experiencia laboral	23	add_experiencia
98	Can change Experiencia laboral	23	change_experiencia
99	Can delete Experiencia laboral	23	delete_experiencia
100	Can view Experiencia laboral	23	view_experiencia
101	Can add Idioma del postulante	26	add_postulanteidioma
102	Can change Idioma del postulante	26	change_postulanteidioma
103	Can delete Idioma del postulante	26	delete_postulanteidioma
104	Can view Idioma del postulante	26	view_postulanteidioma
105	Can add Habilidad del postulante	25	add_postulantehabilidad
106	Can change Habilidad del postulante	25	change_postulantehabilidad
107	Can delete Habilidad del postulante	25	delete_postulantehabilidad
108	Can view Habilidad del postulante	25	view_postulantehabilidad
\.


--
-- Data for Name: codigos_otp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.codigos_otp (id, creado_en, actualizado_en, celular, codigo_hash, proposito, expira_en, intentos, consumido_en, ip, user_id, registro_pendiente_id) FROM stdin;
\.


--
-- Data for Name: departamentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departamentos (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.509014+00	2026-11-11 01:21:47.509025+00	La Paz
2	2026-11-11 01:21:47.511266+00	2026-11-11 01:21:47.511275+00	Cochabamba
3	2026-11-11 01:21:47.512868+00	2026-11-11 01:21:47.512875+00	Santa Cruz
4	2026-11-11 01:21:47.514236+00	2026-11-11 01:21:47.514242+00	Oruro
5	2026-11-11 01:21:47.515691+00	2026-11-11 01:21:47.515699+00	Potosí
6	2026-11-11 01:21:47.51729+00	2026-11-11 01:21:47.517296+00	Chuquisaca
7	2026-11-11 01:21:47.518614+00	2026-11-11 01:21:47.518619+00	Tarija
8	2026-11-11 01:21:47.5199+00	2026-11-11 01:21:47.519907+00	Beni
9	2026-11-11 01:21:47.521208+00	2026-11-11 01:21:47.521215+00	Pando
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	contenttypes	contenttype
5	sessions	session
6	accounts	codigootp
7	accounts	registropendiente
8	accounts	role
9	accounts	user
10	audit	auditlog
11	catalogos	departamento
12	catalogos	habilidad
13	catalogos	idioma
14	catalogos	modalidad
15	catalogos	profesion
16	catalogos	rubro
17	catalogos	tipocontrato
18	empresas	empresa
19	ofertas	oferta
20	ofertas	ofertaguardada
21	ofertas	ofertahabilidad
22	ofertas	postulacion
23	postulantes	experiencia
24	postulantes	formacion
25	postulantes	postulantehabilidad
26	postulantes	postulanteidioma
27	postulantes	postulanteprofile
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-11-11 01:21:46.412328+00
2	contenttypes	0002_remove_content_type_name	2026-11-11 01:21:46.416289+00
3	auth	0001_initial	2026-11-11 01:21:46.430798+00
4	auth	0002_alter_permission_name_max_length	2026-11-11 01:21:46.433946+00
5	auth	0003_alter_user_email_max_length	2026-11-11 01:21:46.43688+00
6	auth	0004_alter_user_username_opts	2026-11-11 01:21:46.439845+00
7	auth	0005_alter_user_last_login_null	2026-11-11 01:21:46.442553+00
8	auth	0006_require_contenttypes_0002	2026-11-11 01:21:46.443771+00
9	auth	0007_alter_validators_add_error_messages	2026-11-11 01:21:46.446947+00
10	auth	0008_alter_user_username_max_length	2026-11-11 01:21:46.450177+00
11	auth	0009_alter_user_last_name_max_length	2026-11-11 01:21:46.453241+00
12	auth	0010_alter_group_name_max_length	2026-11-11 01:21:46.456863+00
13	auth	0011_update_proxy_permissions	2026-11-11 01:21:46.459753+00
14	auth	0012_alter_user_first_name_max_length	2026-11-11 01:21:46.463538+00
15	accounts	0001_initial	2026-11-11 01:21:46.494164+00
16	accounts	0002_seed_roles	2026-11-11 01:21:46.503175+00
17	admin	0001_initial	2026-11-11 01:21:46.512902+00
18	admin	0002_logentry_remove_auto_add	2026-11-11 01:21:46.517809+00
19	admin	0003_logentry_add_action_flag_choices	2026-11-11 01:21:46.522513+00
20	audit	0001_initial	2026-11-11 01:21:46.532704+00
21	catalogos	0001_initial	2026-11-11 01:21:46.548366+00
22	empresas	0001_initial	2026-11-11 01:21:46.561743+00
23	postulantes	0001_initial	2026-11-11 01:21:46.614662+00
24	ofertas	0001_initial	2026-11-11 01:21:46.745372+00
25	sessions	0001_initial	2026-11-11 01:21:46.749841+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: empresas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.empresas (id, creado_en, actualizado_en, nit, razon_social, representante_nombres, representante_apellidos, representante_ci, direccion, logo, descripcion, estado, motivo_rechazo, revisada_en, revisada_por_id, rubro_id, user_id) FROM stdin;
1	2026-11-11 01:21:50.656536+00	2026-11-11 01:21:50.656547+00	1000001	Empresa Demo Aprobada S.R.L.	Ana	Aprobada	1111111 LP	Av. Demo 123, Oruro		Empresa de ejemplo ya validada por GADOR.	APROBADA		2026-11-11 01:21:50.655285+00	1	2	2
2	2026-11-11 01:21:50.883611+00	2026-11-11 01:21:50.88362+00	1000002	Empresa Demo Pendiente S.R.L.	Luis	Pendiente	2222222 OR	Calle Pendiente 456, Oruro		Empresa de ejemplo esperando validación de GADOR.	PENDIENTE_VALIDACION		\N	\N	3	4
\.


--
-- Data for Name: experiencias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.experiencias (id, creado_en, actualizado_en, empresa, cargo, anos, descripcion, profile_id) FROM stdin;
\.


--
-- Data for Name: formaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formaciones (id, creado_en, actualizado_en, titulo, institucion, anio_titulacion, nro_titulo, profile_id) FROM stdin;
\.


--
-- Data for Name: habilidades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.habilidades (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.38527+00	2026-11-11 01:21:47.385279+00	Python
2	2026-11-11 01:21:47.386958+00	2026-11-11 01:21:47.386966+00	Django
3	2026-11-11 01:21:47.3883+00	2026-11-11 01:21:47.388307+00	Laravel
4	2026-11-11 01:21:47.389985+00	2026-11-11 01:21:47.389992+00	JavaScript
5	2026-11-11 01:21:47.391407+00	2026-11-11 01:21:47.391413+00	React
6	2026-11-11 01:21:47.392776+00	2026-11-11 01:21:47.392782+00	SQL
7	2026-11-11 01:21:47.394149+00	2026-11-11 01:21:47.394155+00	PostgreSQL
8	2026-11-11 01:21:47.395564+00	2026-11-11 01:21:47.395571+00	MySQL
9	2026-11-11 01:21:47.397197+00	2026-11-11 01:21:47.397208+00	Redes
10	2026-11-11 01:21:47.398907+00	2026-11-11 01:21:47.398914+00	Soporte técnico
11	2026-11-11 01:21:47.400508+00	2026-11-11 01:21:47.400515+00	Mantenimiento de computadoras
12	2026-11-11 01:21:47.401915+00	2026-11-11 01:21:47.401927+00	Análisis de datos
13	2026-11-11 01:21:47.403173+00	2026-11-11 01:21:47.403179+00	Excel
14	2026-11-11 01:21:47.404439+00	2026-11-11 01:21:47.404445+00	Word
15	2026-11-11 01:21:47.405668+00	2026-11-11 01:21:47.405674+00	PowerPoint
16	2026-11-11 01:21:47.406956+00	2026-11-11 01:21:47.406962+00	Google Workspace
17	2026-11-11 01:21:47.408317+00	2026-11-11 01:21:47.408323+00	Atención al cliente
18	2026-11-11 01:21:47.409553+00	2026-11-11 01:21:47.409559+00	Ventas
19	2026-11-11 01:21:47.410772+00	2026-11-11 01:21:47.410778+00	Cajero
20	2026-11-11 01:21:47.412102+00	2026-11-11 01:21:47.412108+00	Contabilidad
21	2026-11-11 01:21:47.413461+00	2026-11-11 01:21:47.413468+00	Facturación
22	2026-11-11 01:21:47.415224+00	2026-11-11 01:21:47.415232+00	Archivo
23	2026-11-11 01:21:47.416976+00	2026-11-11 01:21:47.416983+00	Gestión de proyectos
24	2026-11-11 01:21:47.418622+00	2026-11-11 01:21:47.418629+00	Recursos Humanos
25	2026-11-11 01:21:47.420241+00	2026-11-11 01:21:47.420246+00	Liderazgo
26	2026-11-11 01:21:47.421558+00	2026-11-11 01:21:47.421563+00	Trabajo en equipo
27	2026-11-11 01:21:47.422937+00	2026-11-11 01:21:47.422943+00	Comunicación
28	2026-11-11 01:21:47.424179+00	2026-11-11 01:21:47.424184+00	Organización
29	2026-11-11 01:21:47.425395+00	2026-11-11 01:21:47.425401+00	Redacción
30	2026-11-11 01:21:47.426599+00	2026-11-11 01:21:47.426605+00	Electricidad
31	2026-11-11 01:21:47.427835+00	2026-11-11 01:21:47.427841+00	Plomería
32	2026-11-11 01:21:47.429224+00	2026-11-11 01:21:47.429232+00	Soldadura
33	2026-11-11 01:21:47.430485+00	2026-11-11 01:21:47.430491+00	Carpintería
34	2026-11-11 01:21:47.431734+00	2026-11-11 01:21:47.43174+00	Albañilería
35	2026-11-11 01:21:47.434328+00	2026-11-11 01:21:47.434336+00	Mecánica automotriz
36	2026-11-11 01:21:47.435808+00	2026-11-11 01:21:47.435814+00	Conducción de vehículos
37	2026-11-11 01:21:47.437061+00	2026-11-11 01:21:47.437066+00	Cocina
38	2026-11-11 01:21:47.438373+00	2026-11-11 01:21:47.438378+00	Panadería
39	2026-11-11 01:21:47.439762+00	2026-11-11 01:21:47.439769+00	Repostería
40	2026-11-11 01:21:47.441056+00	2026-11-11 01:21:47.441061+00	Peluquería
41	2026-11-11 01:21:47.442257+00	2026-11-11 01:21:47.442263+00	Costura
42	2026-11-11 01:21:47.443444+00	2026-11-11 01:21:47.44345+00	Primeros auxilios
43	2026-11-11 01:21:47.444701+00	2026-11-11 01:21:47.444707+00	Enfermería
44	2026-11-11 01:21:47.44596+00	2026-11-11 01:21:47.445966+00	Farmacología
45	2026-11-11 01:21:47.447343+00	2026-11-11 01:21:47.44735+00	Cuidado de personas
46	2026-11-11 01:21:47.448714+00	2026-11-11 01:21:47.448721+00	Docencia
47	2026-11-11 01:21:47.451339+00	2026-11-11 01:21:47.451349+00	Planificación de clases
48	2026-11-11 01:21:47.452951+00	2026-11-11 01:21:47.452957+00	Idiomas
49	2026-11-11 01:21:47.454181+00	2026-11-11 01:21:47.454187+00	Investigación
50	2026-11-11 01:21:47.4554+00	2026-11-11 01:21:47.455407+00	Fotografía
51	2026-11-11 01:21:47.45656+00	2026-11-11 01:21:47.456565+00	Diseño gráfico
52	2026-11-11 01:21:47.457711+00	2026-11-11 01:21:47.457716+00	Redes sociales
53	2026-11-11 01:21:47.458879+00	2026-11-11 01:21:47.458885+00	Marketing digital
\.


--
-- Data for Name: idiomas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.idiomas (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.460355+00	2026-11-11 01:21:47.46036+00	Español
2	2026-11-11 01:21:47.461816+00	2026-11-11 01:21:47.461824+00	Inglés
3	2026-11-11 01:21:47.463178+00	2026-11-11 01:21:47.463184+00	Quechua
4	2026-11-11 01:21:47.464375+00	2026-11-11 01:21:47.464381+00	Aymara
5	2026-11-11 01:21:47.465675+00	2026-11-11 01:21:47.465681+00	Portugués
6	2026-11-11 01:21:47.466881+00	2026-11-11 01:21:47.466887+00	Francés
7	2026-11-11 01:21:47.468239+00	2026-11-11 01:21:47.468245+00	Alemán
8	2026-11-11 01:21:47.469565+00	2026-11-11 01:21:47.46957+00	Italiano
9	2026-11-11 01:21:47.470857+00	2026-11-11 01:21:47.470863+00	Chino Mandarín
10	2026-11-11 01:21:47.472217+00	2026-11-11 01:21:47.472223+00	Japonés
\.


--
-- Data for Name: modalidades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modalidades (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.503021+00	2026-11-11 01:21:47.503032+00	Presencial
2	2026-11-11 01:21:47.505151+00	2026-11-11 01:21:47.50516+00	Remoto
3	2026-11-11 01:21:47.506891+00	2026-11-11 01:21:47.506899+00	Híbrido
\.


--
-- Data for Name: oferta_habilidades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oferta_habilidades (id, creado_en, actualizado_en, obligatoria, habilidad_id, oferta_id) FROM stdin;
1	2026-11-11 01:21:51.368041+00	2026-11-11 01:21:51.368062+00	t	1	1
2	2026-11-11 01:21:51.368053+00	2026-11-11 01:21:51.368065+00	t	6	1
3	2026-11-11 01:21:51.368056+00	2026-11-11 01:21:51.368067+00	t	2	1
4	2026-11-11 01:21:51.368059+00	2026-11-11 01:21:51.368069+00	f	12	1
5	2026-11-11 01:21:51.375129+00	2026-11-11 01:21:51.375143+00	t	6	2
6	2026-11-11 01:21:51.375136+00	2026-11-11 01:21:51.375145+00	t	2	2
7	2026-11-11 01:21:51.375139+00	2026-11-11 01:21:51.375148+00	f	12	2
8	2026-11-11 01:21:51.38035+00	2026-11-11 01:21:51.380358+00	f	12	3
\.


--
-- Data for Name: ofertas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ofertas (id, creado_en, actualizado_en, titulo, descripcion, requisitos_obligatorios, requisitos_deseables, anos_experiencia, municipio, salario_min, salario_max, a_tratar, beneficios, fecha_cierre, plazas, vistas, estado, motivo_revision, publicada_en, revisada_en, departamento_id, empresa_id, modalidad_id, revisada_por_id, tipo_contrato_id) FROM stdin;
1	2026-11-11 01:21:51.361119+00	2026-11-11 01:21:51.361132+00	Desarrollador Full Stack	Desarrollo de aplicaciones web para la plataforma de la Gobernación.	Experiencia en Python, SQL y desarrollo web.	Conocimientos de Django y Docker.	2	Oruro	6000.00	9000.00	f	Seguro de salud y capacitación.	2026-12-11	2	0	PUBLICADA		2026-11-11 01:21:51.359406+00	\N	4	1	3	\N	1
2	2026-11-11 01:21:51.371647+00	2026-11-11 01:21:51.371654+00	Analista de Datos	Análisis de información para la toma de decisiones.	Manejo de SQL y Excel avanzado.	Python para análisis de datos.	1	Oruro	4500.00	6500.00	f		2026-12-01	1	0	EN_REVISION_GADOR		\N	\N	4	1	3	\N	1
3	2026-11-11 01:21:51.377074+00	2026-11-11 01:21:51.377089+00	Pasante de Soporte Técnico	Apoyo en soporte técnico y mantenimiento de equipos.	Conocimientos básicos de redes y hardware.	Excel y atención al cliente.	0	Oruro	\N	\N	t		2026-11-26	1	0	BORRADOR		\N	\N	4	1	3	\N	1
\.


--
-- Data for Name: ofertas_guardadas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ofertas_guardadas (id, creado_en, actualizado_en, oferta_id, postulante_id) FROM stdin;
\.


--
-- Data for Name: ofertas_profesiones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ofertas_profesiones (id, oferta_id, profesion_id) FROM stdin;
1	1	1
2	2	1
3	3	1
\.


--
-- Data for Name: postulaciones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.postulaciones (id, creado_en, actualizado_en, estado, visto_en, oferta_id, postulante_id) FROM stdin;
\.


--
-- Data for Name: postulante_habilidades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.postulante_habilidades (id, creado_en, actualizado_en, nivel, habilidad_id, profile_id) FROM stdin;
\.


--
-- Data for Name: postulante_idiomas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.postulante_idiomas (id, creado_en, actualizado_en, nivel, idioma_id, profile_id) FROM stdin;
\.


--
-- Data for Name: postulante_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.postulante_profiles (id, creado_en, actualizado_en, ci, foto, direccion, fecha_nacimiento, presentacion, cv, profesion_id, user_id) FROM stdin;
1	2026-11-11 01:21:48.688358+00	2026-11-11 01:21:50.094409+00	7654321 OR			\N	Soy una persona comprometida con el aprendizaje continuo. Busco aportar en proyectos donde pueda combinar formación técnica, experiencia y trabajo en equipo.	postulantes/cv/cv-ejemplo_RZBIFu3.pdf	\N	3
\.


--
-- Data for Name: profesiones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profesiones (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.320377+00	2026-11-11 01:21:47.320392+00	Ingeniero de Sistemas
2	2026-11-11 01:21:47.322771+00	2026-11-11 01:21:47.322778+00	Ingeniero Informático
3	2026-11-11 01:21:47.32422+00	2026-11-11 01:21:47.324227+00	Ingeniero de Software
4	2026-11-11 01:21:47.325522+00	2026-11-11 01:21:47.325529+00	Técnico Superior en Sistemas Informáticos
5	2026-11-11 01:21:47.326756+00	2026-11-11 01:21:47.326761+00	Analista de Sistemas
6	2026-11-11 01:21:47.327945+00	2026-11-11 01:21:47.327951+00	Ingeniero Civil
7	2026-11-11 01:21:47.329275+00	2026-11-11 01:21:47.329281+00	Arquitecto
8	2026-11-11 01:21:47.330588+00	2026-11-11 01:21:47.330594+00	Técnico en Construcción
9	2026-11-11 01:21:47.331829+00	2026-11-11 01:21:47.331837+00	Electricista
10	2026-11-11 01:21:47.333386+00	2026-11-11 01:21:47.333394+00	Plomero
11	2026-11-11 01:21:47.334781+00	2026-11-11 01:21:47.334788+00	Soldador
12	2026-11-11 01:21:47.336223+00	2026-11-11 01:21:47.336229+00	Mecánico
13	2026-11-11 01:21:47.337544+00	2026-11-11 01:21:47.337549+00	Chofer
14	2026-11-11 01:21:47.338723+00	2026-11-11 01:21:47.338729+00	Médico
15	2026-11-11 01:21:47.339978+00	2026-11-11 01:21:47.339984+00	Enfermero
16	2026-11-11 01:21:47.341231+00	2026-11-11 01:21:47.341237+00	Odontólogo
17	2026-11-11 01:21:47.3425+00	2026-11-11 01:21:47.342506+00	Nutricionista
18	2026-11-11 01:21:47.344012+00	2026-11-11 01:21:47.344018+00	Psicólogo
19	2026-11-11 01:21:47.345562+00	2026-11-11 01:21:47.345568+00	Fisioterapeuta
20	2026-11-11 01:21:47.347057+00	2026-11-11 01:21:47.347063+00	Veterinario
21	2026-11-11 01:21:47.348592+00	2026-11-11 01:21:47.348598+00	Docente
22	2026-11-11 01:21:47.350059+00	2026-11-11 01:21:47.350067+00	Educador
23	2026-11-11 01:21:47.351456+00	2026-11-11 01:21:47.351462+00	Contador Público
24	2026-11-11 01:21:47.352885+00	2026-11-11 01:21:47.352893+00	Auditor
25	2026-11-11 01:21:47.354175+00	2026-11-11 01:21:47.35418+00	Administrador de Empresas
26	2026-11-11 01:21:47.355398+00	2026-11-11 01:21:47.355403+00	Abogado
27	2026-11-11 01:21:47.356659+00	2026-11-11 01:21:47.356664+00	Comunicador Social
28	2026-11-11 01:21:47.357905+00	2026-11-11 01:21:47.357911+00	Diseñador Gráfico
29	2026-11-11 01:21:47.359188+00	2026-11-11 01:21:47.359194+00	Especialista en Marketing
30	2026-11-11 01:21:47.360406+00	2026-11-11 01:21:47.360412+00	Especialista en Recursos Humanos
31	2026-11-11 01:21:47.361689+00	2026-11-11 01:21:47.361695+00	Secretaria
32	2026-11-11 01:21:47.363027+00	2026-11-11 01:21:47.363033+00	Atención al cliente
33	2026-11-11 01:21:47.36458+00	2026-11-11 01:21:47.364589+00	Chef
34	2026-11-11 01:21:47.366135+00	2026-11-11 01:21:47.366143+00	Cocinero
35	2026-11-11 01:21:47.368423+00	2026-11-11 01:21:47.368434+00	Panadero
36	2026-11-11 01:21:47.370014+00	2026-11-11 01:21:47.370021+00	Comerciante
37	2026-11-11 01:21:47.37157+00	2026-11-11 01:21:47.371578+00	Vendedor
38	2026-11-11 01:21:47.372999+00	2026-11-11 01:21:47.373006+00	Cajero
39	2026-11-11 01:21:47.374433+00	2026-11-11 01:21:47.37444+00	Agricultor
40	2026-11-11 01:21:47.375958+00	2026-11-11 01:21:47.375965+00	Ganadero
41	2026-11-11 01:21:47.377371+00	2026-11-11 01:21:47.377378+00	Minero
42	2026-11-11 01:21:47.378692+00	2026-11-11 01:21:47.378699+00	Personal de seguridad
43	2026-11-11 01:21:47.380762+00	2026-11-11 01:21:47.380775+00	Personal de limpieza
44	2026-11-11 01:21:47.382371+00	2026-11-11 01:21:47.382379+00	Otro
\.


--
-- Data for Name: registros_pendientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.registros_pendientes (creado_en, actualizado_en, id, ci, nombres, apellidos, celular, email, password_hash, expira_en, ip) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, codigo, nombre) FROM stdin;
1	SUPERADMIN	SuperAdmin GADOR
2	EMPRESA	Empresa
3	POSTULANTE	Postulante
\.


--
-- Data for Name: rubros; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rubros (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.473649+00	2026-11-11 01:21:47.473655+00	Minería
2	2026-11-11 01:21:47.475062+00	2026-11-11 01:21:47.475067+00	Tecnología
3	2026-11-11 01:21:47.476258+00	2026-11-11 01:21:47.476264+00	Comercio
4	2026-11-11 01:21:47.477419+00	2026-11-11 01:21:47.477424+00	Salud
5	2026-11-11 01:21:47.478615+00	2026-11-11 01:21:47.47862+00	Educación
6	2026-11-11 01:21:47.479889+00	2026-11-11 01:21:47.479895+00	Construcción
7	2026-11-11 01:21:47.481404+00	2026-11-11 01:21:47.481409+00	Gastronomía
8	2026-11-11 01:21:47.483302+00	2026-11-11 01:21:47.483312+00	Transporte
9	2026-11-11 01:21:47.485717+00	2026-11-11 01:21:47.485724+00	Servicios
10	2026-11-11 01:21:47.48746+00	2026-11-11 01:21:47.487467+00	Industria
11	2026-11-11 01:21:47.488762+00	2026-11-11 01:21:47.488769+00	Agricultura
12	2026-11-11 01:21:47.490033+00	2026-11-11 01:21:47.490039+00	Turismo
13	2026-11-11 01:21:47.491291+00	2026-11-11 01:21:47.491299+00	Banca y finanzas
14	2026-11-11 01:21:47.492714+00	2026-11-11 01:21:47.49272+00	Comunicación
15	2026-11-11 01:21:47.493876+00	2026-11-11 01:21:47.493882+00	Otro
\.


--
-- Data for Name: tipos_contrato; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipos_contrato (id, creado_en, actualizado_en, nombre) FROM stdin;
1	2026-11-11 01:21:47.495326+00	2026-11-11 01:21:47.495333+00	Indefinido
2	2026-11-11 01:21:47.496947+00	2026-11-11 01:21:47.496954+00	Plazo fijo
3	2026-11-11 01:21:47.498294+00	2026-11-11 01:21:47.4983+00	Pasantía
4	2026-11-11 01:21:47.500666+00	2026-11-11 01:21:47.500678+00	Consultoría
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, email, celular, celular_verificado, role_id) FROM stdin;
1	bcrypt_sha256$$2b$12$df3vz.Sg9OTQLvEjfL8zGOTRDMzIu1EPfKQ31K.aHIPH0AVmpnI56	\N	t			t	t	2026-11-11 01:21:48.020065+00	admin@gador.gob.bo	\N	t	1
3	bcrypt_sha256$$2b$12$JG9Jrj748UpJOQr.0Cdhn.1nCtIDoGXJXeqZ2ib1N9obycmcocbP6	\N	f			f	t	2026-11-11 01:21:48.466964+00	postulante@gador.gob.bo	\N	t	3
2	bcrypt_sha256$$2b$12$SlccbHOnf1ulRRTX2w.0V.uYvm17bhl7e3xL58N3ZIf9ZkAe41ww.	\N	f	Empresa	Aprobada	f	t	2026-11-11 01:21:48.248479+00	empresa@gador.gob.bo	+59170000010	t	2
4	bcrypt_sha256$$2b$12$hlPfErkeV7S/DCb6xfF3We960KH6BQKzdPQQKOyaT.ZNw9B0Y3hXq	\N	f	Empresa	Pendiente	f	t	2026-11-11 01:21:50.661106+00	empresa.pendiente@gador.gob.bo	+59170000011	t	2
\.


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: audit_auditlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_auditlog_id_seq', 10, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 108, true);


--
-- Name: codigos_otp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.codigos_otp_id_seq', 1, false);


--
-- Name: departamentos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departamentos_id_seq', 9, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 27, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 25, true);


--
-- Name: empresas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.empresas_id_seq', 2, true);


--
-- Name: experiencias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.experiencias_id_seq', 1, false);


--
-- Name: formaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formaciones_id_seq', 1, false);


--
-- Name: habilidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.habilidades_id_seq', 53, true);


--
-- Name: idiomas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.idiomas_id_seq', 10, true);


--
-- Name: modalidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modalidades_id_seq', 3, true);


--
-- Name: oferta_habilidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.oferta_habilidades_id_seq', 8, true);


--
-- Name: ofertas_guardadas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ofertas_guardadas_id_seq', 1, false);


--
-- Name: ofertas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ofertas_id_seq', 3, true);


--
-- Name: ofertas_profesiones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ofertas_profesiones_id_seq', 3, true);


--
-- Name: postulaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.postulaciones_id_seq', 1, false);


--
-- Name: postulante_habilidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.postulante_habilidades_id_seq', 1, false);


--
-- Name: postulante_idiomas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.postulante_idiomas_id_seq', 1, false);


--
-- Name: postulante_profiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.postulante_profiles_id_seq', 1, true);


--
-- Name: profesiones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.profesiones_id_seq', 44, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_seq', 3, true);


--
-- Name: rubros_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rubros_id_seq', 15, true);


--
-- Name: tipos_contrato_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipos_contrato_id_seq', 4, true);


--
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- Name: audit_auditlog audit_auditlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_auditlog
    ADD CONSTRAINT audit_auditlog_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: codigos_otp codigos_otp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.codigos_otp
    ADD CONSTRAINT codigos_otp_pkey PRIMARY KEY (id);


--
-- Name: departamentos departamentos_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_nombre_key UNIQUE (nombre);


--
-- Name: departamentos departamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departamentos
    ADD CONSTRAINT departamentos_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: empresas empresas_nit_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_nit_key UNIQUE (nit);


--
-- Name: empresas empresas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_pkey PRIMARY KEY (id);


--
-- Name: empresas empresas_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_user_id_key UNIQUE (user_id);


--
-- Name: experiencias experiencias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experiencias
    ADD CONSTRAINT experiencias_pkey PRIMARY KEY (id);


--
-- Name: formaciones formaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formaciones
    ADD CONSTRAINT formaciones_pkey PRIMARY KEY (id);


--
-- Name: habilidades habilidades_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habilidades
    ADD CONSTRAINT habilidades_nombre_key UNIQUE (nombre);


--
-- Name: habilidades habilidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habilidades
    ADD CONSTRAINT habilidades_pkey PRIMARY KEY (id);


--
-- Name: idiomas idiomas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idiomas
    ADD CONSTRAINT idiomas_nombre_key UNIQUE (nombre);


--
-- Name: idiomas idiomas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.idiomas
    ADD CONSTRAINT idiomas_pkey PRIMARY KEY (id);


--
-- Name: modalidades modalidades_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modalidades
    ADD CONSTRAINT modalidades_nombre_key UNIQUE (nombre);


--
-- Name: modalidades modalidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modalidades
    ADD CONSTRAINT modalidades_pkey PRIMARY KEY (id);


--
-- Name: oferta_habilidades oferta_habilidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferta_habilidades
    ADD CONSTRAINT oferta_habilidades_pkey PRIMARY KEY (id);


--
-- Name: ofertas_guardadas ofertas_guardadas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_guardadas
    ADD CONSTRAINT ofertas_guardadas_pkey PRIMARY KEY (id);


--
-- Name: ofertas ofertas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas
    ADD CONSTRAINT ofertas_pkey PRIMARY KEY (id);


--
-- Name: ofertas_profesiones ofertas_profesiones_oferta_id_profesion_id_f93c8bc8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_profesiones
    ADD CONSTRAINT ofertas_profesiones_oferta_id_profesion_id_f93c8bc8_uniq UNIQUE (oferta_id, profesion_id);


--
-- Name: ofertas_profesiones ofertas_profesiones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_profesiones
    ADD CONSTRAINT ofertas_profesiones_pkey PRIMARY KEY (id);


--
-- Name: postulaciones postulaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulaciones
    ADD CONSTRAINT postulaciones_pkey PRIMARY KEY (id);


--
-- Name: postulante_habilidades postulante_habilidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_habilidades
    ADD CONSTRAINT postulante_habilidades_pkey PRIMARY KEY (id);


--
-- Name: postulante_idiomas postulante_idiomas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_idiomas
    ADD CONSTRAINT postulante_idiomas_pkey PRIMARY KEY (id);


--
-- Name: postulante_profiles postulante_profiles_ci_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_profiles
    ADD CONSTRAINT postulante_profiles_ci_key UNIQUE (ci);


--
-- Name: postulante_profiles postulante_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_profiles
    ADD CONSTRAINT postulante_profiles_pkey PRIMARY KEY (id);


--
-- Name: postulante_profiles postulante_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_profiles
    ADD CONSTRAINT postulante_profiles_user_id_key UNIQUE (user_id);


--
-- Name: profesiones profesiones_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesiones
    ADD CONSTRAINT profesiones_nombre_key UNIQUE (nombre);


--
-- Name: profesiones profesiones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.profesiones
    ADD CONSTRAINT profesiones_pkey PRIMARY KEY (id);


--
-- Name: registros_pendientes registros_pendientes_celular_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_pendientes
    ADD CONSTRAINT registros_pendientes_celular_key UNIQUE (celular);


--
-- Name: registros_pendientes registros_pendientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_pendientes
    ADD CONSTRAINT registros_pendientes_pkey PRIMARY KEY (id);


--
-- Name: roles roles_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_codigo_key UNIQUE (codigo);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: rubros rubros_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rubros
    ADD CONSTRAINT rubros_nombre_key UNIQUE (nombre);


--
-- Name: rubros rubros_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rubros
    ADD CONSTRAINT rubros_pkey PRIMARY KEY (id);


--
-- Name: tipos_contrato tipos_contrato_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_contrato
    ADD CONSTRAINT tipos_contrato_nombre_key UNIQUE (nombre);


--
-- Name: tipos_contrato tipos_contrato_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_contrato
    ADD CONSTRAINT tipos_contrato_pkey PRIMARY KEY (id);


--
-- Name: oferta_habilidades unique_habilidad_por_oferta; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferta_habilidades
    ADD CONSTRAINT unique_habilidad_por_oferta UNIQUE (oferta_id, habilidad_id);


--
-- Name: postulante_habilidades unique_habilidad_por_postulante; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_habilidades
    ADD CONSTRAINT unique_habilidad_por_postulante UNIQUE (profile_id, habilidad_id);


--
-- Name: postulante_idiomas unique_idioma_por_postulante; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_idiomas
    ADD CONSTRAINT unique_idioma_por_postulante UNIQUE (profile_id, idioma_id);


--
-- Name: ofertas_guardadas unique_oferta_guardada_por_postulante; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_guardadas
    ADD CONSTRAINT unique_oferta_guardada_por_postulante UNIQUE (postulante_id, oferta_id);


--
-- Name: postulaciones unique_postulacion_por_oferta; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulaciones
    ADD CONSTRAINT unique_postulacion_por_oferta UNIQUE (oferta_id, postulante_id);


--
-- Name: users users_celular_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_celular_key UNIQUE (celular);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- Name: users_groups users_groups_user_id_group_id_fc7788e8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_group_id_fc7788e8_uniq UNIQUE (user_id, group_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_user_id_permission_id_3b86cbdf_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_permission_id_3b86cbdf_uniq UNIQUE (user_id, permission_id);


--
-- Name: audit_auditlog_fecha_3639eaad; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX audit_auditlog_fecha_3639eaad ON public.audit_auditlog USING btree (fecha);


--
-- Name: audit_auditlog_usuario_id_7754169a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX audit_auditlog_usuario_id_7754169a ON public.audit_auditlog USING btree (usuario_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: codigos_otp_celular_e9c792_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX codigos_otp_celular_e9c792_idx ON public.codigos_otp USING btree (celular, proposito, creado_en);


--
-- Name: codigos_otp_ip_3b5cc9_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX codigos_otp_ip_3b5cc9_idx ON public.codigos_otp USING btree (ip, proposito, creado_en);


--
-- Name: codigos_otp_registr_d04816_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX codigos_otp_registr_d04816_idx ON public.codigos_otp USING btree (registro_pendiente_id, proposito, creado_en);


--
-- Name: codigos_otp_registro_pendiente_id_9c14ca23; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX codigos_otp_registro_pendiente_id_9c14ca23 ON public.codigos_otp USING btree (registro_pendiente_id);


--
-- Name: codigos_otp_user_id_93000663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX codigos_otp_user_id_93000663 ON public.codigos_otp USING btree (user_id);


--
-- Name: codigos_otp_user_id_abc3cc_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX codigos_otp_user_id_abc3cc_idx ON public.codigos_otp USING btree (user_id, proposito, creado_en);


--
-- Name: departamentos_nombre_ee12a90a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX departamentos_nombre_ee12a90a_like ON public.departamentos USING btree (nombre varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: empresas_estado_2f40fdd1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX empresas_estado_2f40fdd1 ON public.empresas USING btree (estado);


--
-- Name: empresas_estado_2f40fdd1_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX empresas_estado_2f40fdd1_like ON public.empresas USING btree (estado varchar_pattern_ops);


--
-- Name: empresas_nit_5a5af0f1_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX empresas_nit_5a5af0f1_like ON public.empresas USING btree (nit varchar_pattern_ops);


--
-- Name: empresas_revisada_por_id_78b8567c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX empresas_revisada_por_id_78b8567c ON public.empresas USING btree (revisada_por_id);


--
-- Name: empresas_rubro_id_0ca0be2a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX empresas_rubro_id_0ca0be2a ON public.empresas USING btree (rubro_id);


--
-- Name: experiencias_profile_id_083d5d7f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX experiencias_profile_id_083d5d7f ON public.experiencias USING btree (profile_id);


--
-- Name: formaciones_profile_id_2a436406; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX formaciones_profile_id_2a436406 ON public.formaciones USING btree (profile_id);


--
-- Name: habilidades_nombre_c32cfed8_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX habilidades_nombre_c32cfed8_like ON public.habilidades USING btree (nombre varchar_pattern_ops);


--
-- Name: idiomas_nombre_7f8f4369_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idiomas_nombre_7f8f4369_like ON public.idiomas USING btree (nombre varchar_pattern_ops);


--
-- Name: modalidades_nombre_64734915_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX modalidades_nombre_64734915_like ON public.modalidades USING btree (nombre varchar_pattern_ops);


--
-- Name: oferta_habilidades_habilidad_id_a0ab4903; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX oferta_habilidades_habilidad_id_a0ab4903 ON public.oferta_habilidades USING btree (habilidad_id);


--
-- Name: oferta_habilidades_oferta_id_91954529; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX oferta_habilidades_oferta_id_91954529 ON public.oferta_habilidades USING btree (oferta_id);


--
-- Name: ofertas_departamento_id_aadaefa1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_departamento_id_aadaefa1 ON public.ofertas USING btree (departamento_id);


--
-- Name: ofertas_empresa_id_57a168b1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_empresa_id_57a168b1 ON public.ofertas USING btree (empresa_id);


--
-- Name: ofertas_estado_44ebe942; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_estado_44ebe942 ON public.ofertas USING btree (estado);


--
-- Name: ofertas_estado_44ebe942_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_estado_44ebe942_like ON public.ofertas USING btree (estado varchar_pattern_ops);


--
-- Name: ofertas_guardadas_oferta_id_687ff106; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_guardadas_oferta_id_687ff106 ON public.ofertas_guardadas USING btree (oferta_id);


--
-- Name: ofertas_guardadas_postulante_id_aa9b88fb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_guardadas_postulante_id_aa9b88fb ON public.ofertas_guardadas USING btree (postulante_id);


--
-- Name: ofertas_modalidad_id_2ce5f626; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_modalidad_id_2ce5f626 ON public.ofertas USING btree (modalidad_id);


--
-- Name: ofertas_profesiones_oferta_id_d43cdd60; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_profesiones_oferta_id_d43cdd60 ON public.ofertas_profesiones USING btree (oferta_id);


--
-- Name: ofertas_profesiones_profesion_id_c52380fe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_profesiones_profesion_id_c52380fe ON public.ofertas_profesiones USING btree (profesion_id);


--
-- Name: ofertas_revisada_por_id_af24498c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_revisada_por_id_af24498c ON public.ofertas USING btree (revisada_por_id);


--
-- Name: ofertas_tipo_contrato_id_b3721731; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ofertas_tipo_contrato_id_b3721731 ON public.ofertas USING btree (tipo_contrato_id);


--
-- Name: postulaciones_estado_f77dd568; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulaciones_estado_f77dd568 ON public.postulaciones USING btree (estado);


--
-- Name: postulaciones_estado_f77dd568_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulaciones_estado_f77dd568_like ON public.postulaciones USING btree (estado varchar_pattern_ops);


--
-- Name: postulaciones_oferta_id_37c23232; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulaciones_oferta_id_37c23232 ON public.postulaciones USING btree (oferta_id);


--
-- Name: postulaciones_postulante_id_b169e96a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulaciones_postulante_id_b169e96a ON public.postulaciones USING btree (postulante_id);


--
-- Name: postulante_habilidades_habilidad_id_f6f3cf3e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulante_habilidades_habilidad_id_f6f3cf3e ON public.postulante_habilidades USING btree (habilidad_id);


--
-- Name: postulante_habilidades_profile_id_e3309758; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulante_habilidades_profile_id_e3309758 ON public.postulante_habilidades USING btree (profile_id);


--
-- Name: postulante_idiomas_idioma_id_aa9f19ae; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulante_idiomas_idioma_id_aa9f19ae ON public.postulante_idiomas USING btree (idioma_id);


--
-- Name: postulante_idiomas_profile_id_37040d5a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulante_idiomas_profile_id_37040d5a ON public.postulante_idiomas USING btree (profile_id);


--
-- Name: postulante_profiles_ci_6b8b9fe3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulante_profiles_ci_6b8b9fe3_like ON public.postulante_profiles USING btree (ci varchar_pattern_ops);


--
-- Name: postulante_profiles_profesion_id_8e0c0516; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX postulante_profiles_profesion_id_8e0c0516 ON public.postulante_profiles USING btree (profesion_id);


--
-- Name: profesiones_nombre_2c6b85ce_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX profesiones_nombre_2c6b85ce_like ON public.profesiones USING btree (nombre varchar_pattern_ops);


--
-- Name: registros_p_ci_74e63d_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX registros_p_ci_74e63d_idx ON public.registros_pendientes USING btree (ci);


--
-- Name: registros_p_email_4de006_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX registros_p_email_4de006_idx ON public.registros_pendientes USING btree (email);


--
-- Name: registros_p_expira__59b079_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX registros_p_expira__59b079_idx ON public.registros_pendientes USING btree (expira_en);


--
-- Name: registros_pendientes_celular_a3c1a3e7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX registros_pendientes_celular_a3c1a3e7_like ON public.registros_pendientes USING btree (celular varchar_pattern_ops);


--
-- Name: roles_codigo_64af986f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX roles_codigo_64af986f_like ON public.roles USING btree (codigo varchar_pattern_ops);


--
-- Name: rubros_nombre_8ba97d42_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX rubros_nombre_8ba97d42_like ON public.rubros USING btree (nombre varchar_pattern_ops);


--
-- Name: tipos_contrato_nombre_8bb9a70d_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tipos_contrato_nombre_8bb9a70d_like ON public.tipos_contrato USING btree (nombre varchar_pattern_ops);


--
-- Name: users_celular_233cc330_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_celular_233cc330_like ON public.users USING btree (celular varchar_pattern_ops);


--
-- Name: users_email_0ea73cca_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_email_0ea73cca_like ON public.users USING btree (email varchar_pattern_ops);


--
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- Name: users_groups_user_id_f500bee5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_groups_user_id_f500bee5 ON public.users_groups USING btree (user_id);


--
-- Name: users_role_id_1900a745; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_role_id_1900a745 ON public.users USING btree (role_id);


--
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- Name: users_user_permissions_user_id_92473840; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_permissions_user_id_92473840 ON public.users_user_permissions USING btree (user_id);


--
-- Name: audit_auditlog audit_auditlog_usuario_id_7754169a_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_auditlog
    ADD CONSTRAINT audit_auditlog_usuario_id_7754169a_fk_users_id FOREIGN KEY (usuario_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: codigos_otp codigos_otp_registro_pendiente_i_9c14ca23_fk_registros; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.codigos_otp
    ADD CONSTRAINT codigos_otp_registro_pendiente_i_9c14ca23_fk_registros FOREIGN KEY (registro_pendiente_id) REFERENCES public.registros_pendientes(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: codigos_otp codigos_otp_user_id_93000663_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.codigos_otp
    ADD CONSTRAINT codigos_otp_user_id_93000663_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empresas empresas_revisada_por_id_78b8567c_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_revisada_por_id_78b8567c_fk_users_id FOREIGN KEY (revisada_por_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empresas empresas_rubro_id_0ca0be2a_fk_rubros_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_rubro_id_0ca0be2a_fk_rubros_id FOREIGN KEY (rubro_id) REFERENCES public.rubros(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: empresas empresas_user_id_cf30b035_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.empresas
    ADD CONSTRAINT empresas_user_id_cf30b035_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: experiencias experiencias_profile_id_083d5d7f_fk_postulante_profiles_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.experiencias
    ADD CONSTRAINT experiencias_profile_id_083d5d7f_fk_postulante_profiles_id FOREIGN KEY (profile_id) REFERENCES public.postulante_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: formaciones formaciones_profile_id_2a436406_fk_postulante_profiles_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formaciones
    ADD CONSTRAINT formaciones_profile_id_2a436406_fk_postulante_profiles_id FOREIGN KEY (profile_id) REFERENCES public.postulante_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oferta_habilidades oferta_habilidades_habilidad_id_a0ab4903_fk_habilidades_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferta_habilidades
    ADD CONSTRAINT oferta_habilidades_habilidad_id_a0ab4903_fk_habilidades_id FOREIGN KEY (habilidad_id) REFERENCES public.habilidades(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oferta_habilidades oferta_habilidades_oferta_id_91954529_fk_ofertas_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oferta_habilidades
    ADD CONSTRAINT oferta_habilidades_oferta_id_91954529_fk_ofertas_id FOREIGN KEY (oferta_id) REFERENCES public.ofertas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas ofertas_departamento_id_aadaefa1_fk_departamentos_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas
    ADD CONSTRAINT ofertas_departamento_id_aadaefa1_fk_departamentos_id FOREIGN KEY (departamento_id) REFERENCES public.departamentos(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas ofertas_empresa_id_57a168b1_fk_empresas_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas
    ADD CONSTRAINT ofertas_empresa_id_57a168b1_fk_empresas_id FOREIGN KEY (empresa_id) REFERENCES public.empresas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas_guardadas ofertas_guardadas_oferta_id_687ff106_fk_ofertas_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_guardadas
    ADD CONSTRAINT ofertas_guardadas_oferta_id_687ff106_fk_ofertas_id FOREIGN KEY (oferta_id) REFERENCES public.ofertas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas_guardadas ofertas_guardadas_postulante_id_aa9b88fb_fk_postulant; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_guardadas
    ADD CONSTRAINT ofertas_guardadas_postulante_id_aa9b88fb_fk_postulant FOREIGN KEY (postulante_id) REFERENCES public.postulante_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas ofertas_modalidad_id_2ce5f626_fk_modalidades_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas
    ADD CONSTRAINT ofertas_modalidad_id_2ce5f626_fk_modalidades_id FOREIGN KEY (modalidad_id) REFERENCES public.modalidades(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas_profesiones ofertas_profesiones_oferta_id_d43cdd60_fk_ofertas_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_profesiones
    ADD CONSTRAINT ofertas_profesiones_oferta_id_d43cdd60_fk_ofertas_id FOREIGN KEY (oferta_id) REFERENCES public.ofertas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas_profesiones ofertas_profesiones_profesion_id_c52380fe_fk_profesiones_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas_profesiones
    ADD CONSTRAINT ofertas_profesiones_profesion_id_c52380fe_fk_profesiones_id FOREIGN KEY (profesion_id) REFERENCES public.profesiones(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas ofertas_revisada_por_id_af24498c_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas
    ADD CONSTRAINT ofertas_revisada_por_id_af24498c_fk_users_id FOREIGN KEY (revisada_por_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ofertas ofertas_tipo_contrato_id_b3721731_fk_tipos_contrato_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ofertas
    ADD CONSTRAINT ofertas_tipo_contrato_id_b3721731_fk_tipos_contrato_id FOREIGN KEY (tipo_contrato_id) REFERENCES public.tipos_contrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulaciones postulaciones_oferta_id_37c23232_fk_ofertas_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulaciones
    ADD CONSTRAINT postulaciones_oferta_id_37c23232_fk_ofertas_id FOREIGN KEY (oferta_id) REFERENCES public.ofertas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulaciones postulaciones_postulante_id_b169e96a_fk_postulante_profiles_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulaciones
    ADD CONSTRAINT postulaciones_postulante_id_b169e96a_fk_postulante_profiles_id FOREIGN KEY (postulante_id) REFERENCES public.postulante_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulante_habilidades postulante_habilidad_profile_id_e3309758_fk_postulant; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_habilidades
    ADD CONSTRAINT postulante_habilidad_profile_id_e3309758_fk_postulant FOREIGN KEY (profile_id) REFERENCES public.postulante_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulante_habilidades postulante_habilidades_habilidad_id_f6f3cf3e_fk_habilidades_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_habilidades
    ADD CONSTRAINT postulante_habilidades_habilidad_id_f6f3cf3e_fk_habilidades_id FOREIGN KEY (habilidad_id) REFERENCES public.habilidades(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulante_idiomas postulante_idiomas_idioma_id_aa9f19ae_fk_idiomas_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_idiomas
    ADD CONSTRAINT postulante_idiomas_idioma_id_aa9f19ae_fk_idiomas_id FOREIGN KEY (idioma_id) REFERENCES public.idiomas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulante_idiomas postulante_idiomas_profile_id_37040d5a_fk_postulant; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_idiomas
    ADD CONSTRAINT postulante_idiomas_profile_id_37040d5a_fk_postulant FOREIGN KEY (profile_id) REFERENCES public.postulante_profiles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulante_profiles postulante_profiles_profesion_id_8e0c0516_fk_profesiones_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_profiles
    ADD CONSTRAINT postulante_profiles_profesion_id_8e0c0516_fk_profesiones_id FOREIGN KEY (profesion_id) REFERENCES public.profesiones(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: postulante_profiles postulante_profiles_user_id_c041dc85_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.postulante_profiles
    ADD CONSTRAINT postulante_profiles_user_id_c041dc85_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_user_id_f500bee5_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_user_id_f500bee5_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users users_role_id_1900a745_fk_roles_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_1900a745_fk_roles_id FOREIGN KEY (role_id) REFERENCES public.roles(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissions_user_id_92473840_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_user_id_92473840_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict eIxFf9EpuVu1Y8aOwlFz4JeeY2R9pP6RVplGdtFTtaVZoVMrO2T7gRptI6SxZyO

