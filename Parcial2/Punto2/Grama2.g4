grammar Grama2;

CREATE : 'CREATE' ;
TABLE : 'TABLE' ;
INSERT : 'INSERT' ;
INTO : 'INTO' ;
VALUES : 'VALUES' ;
SELECT : 'SELECT' ;
FROM : 'FROM' ;
WHERE : 'WHERE' ;
UPDATE : 'UPDATE' ;
SET : 'SET' ;
DELETE : 'DELETE' ;
DROP : 'DROP' ;
AND : 'AND' ;
OR : 'OR' ;
TRUE : 'TRUE' ;
FALSE : 'FALSE' ;
ID : [a-zA-Z][a-zA-Z0-9_]* ;
NUMBER : [0-9]+ ('.' [0-9]+)? ;
STRING : '\'' ~[']* '\'' ;
EQ : '=' ;
NE : '!=' ;
GT : '>' ;
LT : '<' ;
GE : '>=' ;
LE : '<=' ;
SEMICOLON : ';' ;
COMMA : ',' ;
LPAREN : '(' ;
RPAREN : ')' ;
WS : [ \t\n\r]+ -> skip ;

programa
    : sentencia SEMICOLON programa
    | sentencia SEMICOLON
    ;

sentencia
    : create
    | read
    | update
    | delete
    ;

create
    : CREATE TABLE ID LPAREN listaCampos RPAREN
    | INSERT INTO ID LPAREN listaCampos RPAREN VALUES LPAREN listaValores RPAREN
    ;

read
    : SELECT listaCampos FROM ID (WHERE condicion)?
    ;

update
    : UPDATE ID SET listaAsignaciones (WHERE condicion)?
    ;

delete
    : DELETE FROM ID (WHERE condicion)?
    | DROP TABLE ID
    ;

listaCampos
    : ID (COMMA ID)*
    ;

listaValores
    : valor (COMMA valor)*
    ;

listaAsignaciones
    : asignacion (COMMA asignacion)*
    ;

asignacion
    : ID EQ valor
    ;

condicion
    : condicionSimple
    | condicion AND condicion
    | condicion OR condicion
    | LPAREN condicion RPAREN
    ;

condicionSimple
    : ID operador valor
    ;

operador
    : EQ
    | NE
    | GT
    | LT
    | GE
    | LE
    ;

valor
    : NUMBER
    | STRING
    | TRUE
    | FALSE
    ;
