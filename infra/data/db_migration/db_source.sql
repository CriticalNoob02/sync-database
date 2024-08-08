DROP TABLE IF EXISTS dados_enviar_ref;
CREATE TABLE dados_enviar_ref (
	id SERIAL PRIMARY key,
	nome varchar(500) NOT NULL
);

DROP TABLE IF EXISTS dados_enviar;
CREATE TABLE dados_enviar (
	nome varchar(500) NOT null,
	nu_aleatorio integer
);

INSERT INTO dados_enviar_ref(id, nome)
VALUES
(1, 'testes1'),
(2, 'asdsdsad'),
(3, 'dashhfgd'),
(4, 'bfghfg'),
(5, 'nbtyjh'),
(6, 'sdzfsdf'),
(7, 'dcas'),
(8, 'xccvvb'),
(9, 'ujkuyk'),
(10, 'vfdret'),
(11, 'asqs'),
(12, 'awqwq'),
(13, 'cvcvcv'),
(111, 'zxzx'),
(19, 'zxddzx'),
(18, 'zxasdasddzx'),
(17, 'zxcxzcczzx'),
(16, 'fyrtyhrt'),
(999, 'nvbnvbv'),
(90, 'zxvnvbnvnvzx'),
(30, 'nbvnnvb'),
(20, 'tyhtyh'),
(15, 'xccvxcv')
;

INSERT INTO dados_enviar(nome, nu_aleatorio)
VALUES
('testes1', 10),
('fsdfsdf', 14),
('fsdfsdf', null),
('fsd', null),
('fsdcxvxcv', null),
('fshbbd', null),
('fsffdfd', null),
('fsasddd', 1233),
('fszxczxcd', null),
('ssadd', 14),
('fszxczxcd', 12),
('fszxczxcd', 12),
('aaa', 22),
('ssss', 21),
('ddd', null),
('vvv', 112),
('gggg', 112),
('bbb', 1)
;
