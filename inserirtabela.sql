INSERT INTO utilizador
VALUES('António Silva','antoniosilva@gmail.com','$5$rounds=535000$2wYEUy1d2ETuGNOK$Tj4CdfuNbJc/Q38RHa6KruFijQG3fGqqy81GJlf3i70');

INSERT INTO utilizador
VALUES('Miguel Faro','miguelfaro@gmail.com','$5$rounds=535000$TzfNZeUoNcRve4gU$zvrhzOHnmVxnNANmlBUNOsTbAn.lOsSYZlgah343wp5');

INSERT INTO utilizador
VALUES('Pedro Marques','pedromarques@gmail.com','$5$rounds=535000$l.h57ZUTpK6OU5.p$LhmRU.1Fj5Mtn7WsNsBsC0utRcPCV0.weqoOiTUWzuC');

INSERT INTO administrador
VALUES('antoniosilva@gmail.com');

INSERT INTO cliente
VALUES('25.30','26.5','16.7','9.98','miguelfaro@gmail.com');

INSERT INTO cliente
VALUES('29.10','37.2','12.30','24.90','pedromarques@gmail.com');

INSERT INTO artigos 
VALUES('1','Venom','5.30','5','10','Filme','Ficao Cientifica','Ruben Flaisher','Marvel Studios');

INSERT INTO artigos 
VALUES('2','T-34','4.70','6','20','Filme','Guerra','Aleksey Sidorov','Mars Media Entertainment');

INSERT INTO artigos 
VALUES('3','Prison Break','8.30','10','50','Serie ','Acao','Paul Scheuring','Adelstein-Parouse Production');

INSERT INTO artigos
VALUES ('4','John Wick 1','7.40','10','20','Filme','Acao','Chad Stahelski','Summit Entertainment');


INSERT INTO artigos
VALUES ('5','John Wick 2','9.30','15','20','Filme','Acao','Chad Stahelski','Summit Entertainment');


INSERT INTO artigos
VALUES ('6','John Wick 3','11.00','15','20','Filme','Acao','Chad Stahelski','Summit Entertainment');

INSERT INTO artigos
VALUES ('7','Spartacus','15.56','40','60','Serie','Drama','Steven Deknight','Starz');

INSERT INTO artigos
VALUES ('8','Narcos','14.50','20','45','Serie','Drama','Chris Brancato','Gaumont International Television');

INSERT INTO artigos
VALUES ('9','Thor: Ragnarok','9.85','20','15','Filme','Ficao Cientifica','Eric Pearson','Marvel Studios');



INSERT INTO detalhes_artigos
VALUES('Tom Hardy');

INSERT INTO detalhes_artigos
VALUES('Alexander Petrov');

INSERT INTO detalhes_artigos
VALUES('Wentworth Miler');

INSERT INTO detalhes_artigos
VALUES('Keanu Reeves');

INSERT INTO detalhes_artigos
VALUES('Andy Whitfield');

INSERT INTO detalhes_artigos
VALUES('Wagner Moura');

INSERT INTO detalhes_artigos
VALUES('Chris Hemsworth');


INSERT INTO artigos_detalhes_artigos
VALUES('1','Tom Hardy');

INSERT INTO artigos_detalhes_artigos
VALUES('2','Alexander Petrov');

INSERT INTO artigos_detalhes_artigos
VALUES('3','Wentworth Miler');

INSERT INTO artigos_detalhes_artigos
VALUES('4','Keanu Reeves');

INSERT INTO artigos_detalhes_artigos
VALUES('5','Keanu Reeves');

INSERT INTO artigos_detalhes_artigos
VALUES('6','Keanu Reeves');

INSERT INTO artigos_detalhes_artigos
VALUES('7','Andy Whitfield');

INSERT INTO artigos_detalhes_artigos
VALUES('8','Wagner Moura');

INSERT INTO artigos_detalhes_artigos
VALUES('9','Chris Hemsworth');



INSERT INTO aluguer
VALUES('1','20/12/2020 20:45:23','21/12/2021 20:45:23','1','7.40','1','4','miguelfaro@gmail.com');

INSERT INTO aluguer
VALUES('2','25/12/2020 20:45:23','26/12/2021 20:45:23','1','9.30','1','5','miguelfaro@gmail.com');


INSERT INTO aluguer
Values('3','15/12/2020 15:30:00','30/12/2020 15:30:00','1','24.90','3','3','pedromarques@gmail.com');

INSERT INTO mensagens
VALUES('1','Bem vindo','14/12/2020 11:13:25','antoniosilva@gmail.com');

INSERT INTO mensagens
VALUES('2','Compra realizada com sucesso','20/12/2020 20:45:30','antoniosilva@gmail.com');

INSERT INTO mensagem_lida
VALUES('True','1','miguelfaro@gmail.com');

INSERT INTO mensagem_lida
VALUES('False','2','miguelfaro@gmail.com');

INSERT INTO cliente_mensagens
VALUES('miguelfaro@gmail.com','1');

INSERT INTO cliente_mensagens
VALUES('miguelfaro@gmail.com','2');


INSERT INTO precos
VALUES('1','8.30','15/12/2020 16:58:27','antoniosilva@gmail.com','3');

INSERT INTO estatisticas
VALUES('1','2','9','3','41.60','1','2','6','3');