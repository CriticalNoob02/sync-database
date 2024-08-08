drop table if exists dados_receber_ref;
create table dados_receber_ref (
	id SERIAL PRIMARY key,
	id_origem int8 NOT NULL,
	nome varchar(500) NOT NULL
);

drop table if exists dados_receber;
create table dados_receber (
	id SERIAL PRIMARY key,
	nome varchar(500) NOT null,
	nu_aleatorio integer
);

