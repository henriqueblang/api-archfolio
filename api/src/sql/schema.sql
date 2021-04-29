CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- DROP SCHEMA geocast;

CREATE SCHEMA geocast;

-- DROP SEQUENCE geocast.camadas_id_seq;

CREATE SEQUENCE geocast.camadas_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE geocast.feicoes_id_seq;

CREATE SEQUENCE geocast.feicoes_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE geocast.projetos_id_seq;

CREATE SEQUENCE geocast.projetos_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;

-- geocast.empresas definition

-- Drop table

-- DROP TABLE geocast.empresas;

CREATE TABLE geocast.empresas (
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	empresa varchar(50) NULL,
	CONSTRAINT empresas_pk PRIMARY KEY (id),
	CONSTRAINT empresas_un UNIQUE (empresa)
);

-- geocast.projetos definition

-- Drop table

-- DROP TABLE geocast.projetos;

CREATE TABLE geocast.projetos (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	empresa_fk uuid NOT NULL,
	nome_projeto varchar(60) NULL,
	grupo_de_acesso varchar(20) NULL,
	CONSTRAINT projetos_pk PRIMARY KEY (id),
	CONSTRAINT projetos_un UNIQUE (empresa_fk, nome_projeto),
	CONSTRAINT projetos_fk FOREIGN KEY (empresa_fk) REFERENCES geocast.empresas(id) ON DELETE CASCADE
);


-- geocast.camadas definition

-- Drop table

-- DROP TABLE geocast.camadas;

CREATE TABLE geocast.camadas (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	projeto_fk int4 NOT NULL,
	nome_camada varchar(20) NULL,
	ordem_da_camada int4 NULL,
	nivel_dtb varchar(20) NULL,
	cor_da_camada varchar(8) NULL,
    public boolean NOT NULL DEFAULT FALSE,
	CONSTRAINT camadas_pk PRIMARY KEY (id),
	CONSTRAINT camadas_un UNIQUE (projeto_fk, nome_camada),
	CONSTRAINT camadas_fk FOREIGN KEY (projeto_fk) REFERENCES geocast.projetos(id) ON DELETE CASCADE
);


-- geocast.feicoes definition

-- Drop table

-- DROP TABLE geocast.feicoes;

CREATE TABLE geocast.feicoes (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	camada_fk int4 NOT NULL,
	nome_feicao varchar(20) NULL,
	parametros jsonb NULL,
	shape jsonb NULL,
	imagem_raster bytea NULL,
	coordenada_ancora point NULL,
	cod_dtb_ibge varchar(16) NULL,
	pino_raster point NULL,
	cor_da_feicao varchar(8) NULL,
	data_criacao timestamp(0) NOT NULL DEFAULT NOW(),
	data_eliminacao timestamp(0) NULL,
	CONSTRAINT feicoes_pk PRIMARY KEY (id),
	CONSTRAINT feicoes_un UNIQUE (camada_fk, nome_feicao),
	CONSTRAINT feicoes_un_2 UNIQUE (camada_fk, shape),
	CONSTRAINT feicoes_fk FOREIGN KEY (camada_fk) REFERENCES geocast.camadas(id) ON DELETE CASCADE
);


-- geocast.series definition

-- Drop table

-- DROP TABLE geocast.series;

CREATE TABLE geocast.series (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	feicao_fk int4 NULL,
	nome_dependente varchar(40) NULL,
	nome_explicativo varchar(40) NULL,
	cor_da_serie varchar(8) NULL,
	CONSTRAINT series_pk PRIMARY KEY (id),
	CONSTRAINT series_fk FOREIGN KEY (feicao_fk) REFERENCES geocast.feicoes(id) ON DELETE CASCADE
);


-- geocast.observacoes definition

-- Drop table

-- DROP TABLE geocast.observacoes;

CREATE TABLE geocast.observacoes (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	series_fk int4 NULL,
	val_dependente varchar(50) NULL,
	val_explicativo varchar(50) NULL,
	CONSTRAINT observacoes_pk PRIMARY KEY (id),
	CONSTRAINT observacoes_fk FOREIGN KEY (series_fk) REFERENCES geocast.series(id) ON DELETE CASCADE
);
