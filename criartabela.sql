CREATE TABLE cliente (
	saldo		 FLOAT(8),
	gasto_total	 FLOAT(8),
	gasto_filmes	 FLOAT(8),
	gasto_series	 FLOAT(8),
	utilizador_email VARCHAR(512),
	PRIMARY KEY(utilizador_email)
);

CREATE TABLE artigos (
	id_artigo	 BIGINT,
	titulo	 VARCHAR(512),
	preco	 FLOAT(8),
	quantidade	 BIGINT,
	tempo_aluguer VARCHAR(512),
	tipo		 VARCHAR(512),
	genero	 VARCHAR(512),
	realizador	 VARCHAR(512),
	produtor	 VARCHAR(512),
	PRIMARY KEY(id_artigo)
);

CREATE TABLE administrador (
	utilizador_email VARCHAR(512),
	PRIMARY KEY(utilizador_email)
);

CREATE TABLE estatisticas (
	id_estatistica			 BIGINT,
	total_clientes			 BIGINT,
	total_artigos			 BIGINT,
	valor_total_artigos_alugados_agora FLOAT(8),
	total_aluguer			 FLOAT(8),
	total_mensagens_lidas		 BIGINT,
	total_mensagens_enviadas		 BIGINT,
	total_filmes			 FLOAT(8),
	total_series			 FLOAT(8),
	PRIMARY KEY(id_estatistica)
);

CREATE TABLE mensagens (
	id_mensagem			 BIGINT,
	mensagem			 VARCHAR(512),
	data				 TIMESTAMP,
	administrador_utilizador_email VARCHAR(512) NOT NULL,
	PRIMARY KEY(id_mensagem)
);

CREATE TABLE precos (
	id_alteracao			 BIGINT,
	novo_preco			 FLOAT(8),
	data_alteracao		 TIMESTAMP,
	administrador_utilizador_email VARCHAR(512) NOT NULL,
	artigos_id_artigo		 BIGINT NOT NULL,
	PRIMARY KEY(id_alteracao)
);

CREATE TABLE aluguer (
	id_operacao		 BIGINT,
	data_entrega		 TIMESTAMP,
	data_levamento		 TIMESTAMP,
	quantidade		 BIGINT,
	valor			 FLOAT(8),
	tempo_aluguer		 FLOAT(8),
	artigos_id_artigo	 BIGINT NOT NULL,
	cliente_utilizador_email VARCHAR(512) NOT NULL,
	PRIMARY KEY(id_operacao)
);

CREATE TABLE detalhes_artigos (
	ator VARCHAR(512),
	PRIMARY KEY(ator)
);

CREATE TABLE utilizador (
	nome	 VARCHAR(512),
	email	 VARCHAR(512),
	password VARCHAR(512),
	PRIMARY KEY(email)
);

CREATE TABLE mensagem_lida (
	mensagem_lida		 BOOL,
	mensagens_id_mensagem	 BIGINT,
	cliente_utilizador_email VARCHAR(512),
	PRIMARY KEY(mensagens_id_mensagem,cliente_utilizador_email)
);

CREATE TABLE cliente_mensagens (
	cliente_utilizador_email VARCHAR(512),
	mensagens_id_mensagem	 BIGINT,
	PRIMARY KEY(cliente_utilizador_email,mensagens_id_mensagem)
);

CREATE TABLE artigos_detalhes_artigos (
	artigos_id_artigo	 BIGINT,
	detalhes_artigos_ator VARCHAR(512),
	PRIMARY KEY(artigos_id_artigo,detalhes_artigos_ator)
);

ALTER TABLE cliente ADD CONSTRAINT cliente_fk1 FOREIGN KEY (utilizador_email) REFERENCES utilizador(email);
ALTER TABLE administrador ADD CONSTRAINT administrador_fk1 FOREIGN KEY (utilizador_email) REFERENCES utilizador(email);
ALTER TABLE mensagens ADD CONSTRAINT mensagens_fk1 FOREIGN KEY (administrador_utilizador_email) REFERENCES administrador(utilizador_email);
ALTER TABLE precos ADD CONSTRAINT precos_fk1 FOREIGN KEY (administrador_utilizador_email) REFERENCES administrador(utilizador_email);
ALTER TABLE precos ADD CONSTRAINT precos_fk2 FOREIGN KEY (artigos_id_artigo) REFERENCES artigos(id_artigo);
ALTER TABLE aluguer ADD CONSTRAINT aluguer_fk1 FOREIGN KEY (artigos_id_artigo) REFERENCES artigos(id_artigo);
ALTER TABLE aluguer ADD CONSTRAINT aluguer_fk2 FOREIGN KEY (cliente_utilizador_email) REFERENCES cliente(utilizador_email);
ALTER TABLE mensagem_lida ADD CONSTRAINT mensagem_lida_fk1 FOREIGN KEY (mensagens_id_mensagem) REFERENCES mensagens(id_mensagem);
ALTER TABLE mensagem_lida ADD CONSTRAINT mensagem_lida_fk2 FOREIGN KEY (cliente_utilizador_email) REFERENCES cliente(utilizador_email);
ALTER TABLE cliente_mensagens ADD CONSTRAINT cliente_mensagens_fk1 FOREIGN KEY (cliente_utilizador_email) REFERENCES cliente(utilizador_email);
ALTER TABLE cliente_mensagens ADD CONSTRAINT cliente_mensagens_fk2 FOREIGN KEY (mensagens_id_mensagem) REFERENCES mensagens(id_mensagem);
ALTER TABLE artigos_detalhes_artigos ADD CONSTRAINT artigos_detalhes_artigos_fk1 FOREIGN KEY (artigos_id_artigo) REFERENCES artigos(id_artigo);
ALTER TABLE artigos_detalhes_artigos ADD CONSTRAINT artigos_detalhes_artigos_fk2 FOREIGN KEY (detalhes_artigos_ator) REFERENCES detalhes_artigos(ator);

