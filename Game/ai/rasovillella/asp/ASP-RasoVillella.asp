riga(0..8).
colonna(0..8).

cella(R,C):- riga(R),colonna(C).

smallWall(R1,C1,R2,C2):- wall(R1,C1,R2,C2,_,_,_,_).
smallWall(R1,C1,R2,C2):- wall(_,_,_,_,R1,C1,R2,C2).
smallWall(R1,C1,R2,C2):- smallWall(R2,C2,R1,C1).

adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R, C1 = C + 1, not smallWall(R,C,R1,C1).
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R, C1 = C - 1, not smallWall(R,C,R1,C1).
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R + 1, C1 = C, not smallWall(R,C,R1,C1).
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R - 1, C1 = C, not smallWall(R,C,R1,C1).

%--------------------MOVIMENTI POSSIBILI--------------------%
newPos(R,C):- cella(R,C),player(ID,R1,C1,_,_),adiacente(R,C,R1,C1),myId(ID).
:- newPos(R1,C1),player(ID,R2,C2,_,_),R1 = R2, C1 = C2, myId(ID).

muovi(ID,R,C)|nonMuovi(ID,R,C):-newPos(R,C),myId(ID),path(ID,R,C,_).

:- #count{ID,R,C : muovi(ID,R,C)} != 1.
:~ nonMuovi(ID,R,C),myId(ID). [5@6,R,C]

#show muovi/3.

