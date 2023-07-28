%------------------INPUT------------------%

% wall(R1,C1,R2,C2,R3,C3,R4,C4).    -> Indica che esiste un muro tra R1-C1 e R2-C2,R3-C3 e R4-C4.
% player(ID,R,C,WL,"G").            -> Indica il playe con id, poszione attuale(R,C), muri rimanenti(WL) e il goal
%                                      che può essere "W","E","N","S".
% myId(ID)                          -> Indica il proprio ID
% path(ID,R,C,W).                   -> Indica una cella nel perso minimo di un giocatore con il relativo costo del cammino

%------------------OUTPUT-----------------%

% muovi(ID,R,C)                     -> Spostiamo il giocatore con id in R,C
% newWall(R1,C1,R2,C2,R3,C3,R4,C4)  -> Piazziamo in muro con queste coordinate

%-----------------------------------------%

riga(0..8).
colonna(0..8).
cella(R,C):- riga(R),colonna(C).

destinazione("N",cella(0,C)) :- colonna(C).
destinazione("E",cella(R,8)) :- riga(R).
destinazione("W",cella(R,0)) :- riga(R).
destinazione("S",cella(8,C)) :- colonna(C).


% Creiamo muri singoli dai muri in input.
smallWall(R1,C1,R2,C2):- wall(R1,C1,R2,C2,_,_,_,_).
smallWall(R1,C1,R2,C2):- wall(_,_,_,_,R1,C1,R2,C2).
smallWall(R1,C1,R2,C2):- smallWall(R2,C2,R1,C1).

futureWall(R1,C1,R2,C2):- scegliMuro(R1,C1,R2,C2,_,_,_,_).
futureWall(R1,C1,R2,C2):- scegliMuro(_,_,_,_,R1,C1,R2,C2).
futureWall(R1,C1,R2,C2):- futureWall(R2,C2,R1,C1).

% Calcoliamo le adiacenze, escludento le celle tra le quali cè un muro
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R, C1 = C + 1, not smallWall(R,C,R1,C1).
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R, C1 = C - 1, not smallWall(R,C,R1,C1).
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R + 1, C1 = C, not smallWall(R,C,R1,C1).
adiacente(R, C, R1, C1) :- cella(R, C),cella(R1,C1), R1 = R - 1, C1 = C, not smallWall(R,C,R1,C1).
adiacente(R1, C1, R, C) :- adiacente(R, C, R1, C1).

% Generiamo le possibili mosse
newPos(R,C):- cella(R,C),player(ID,R1,C1,_,_),adiacente(R,C,R1,C1),myId(ID).
:- newPos(R1,C1),player(ID,R2,C2,_,_),R1 = R2, C1 = C2, myId(ID).

% Genera quadrati di celle adiacenti dove è possibile piazzare un muro verticale o orizzontale
% Verticali
newWall(R1,C1,R2,C2,R3,C3,R4,C4):- adiacente(R1,C1,R2,C2),adiacente(R3,C3,R4,C4),R1=R2,C1=C2+1,R3=R1+1,C1=C3,R4=R2+1,C2=C4,not wall(R4,C4,R2,C2,R3,C3,R1,C1).
% Orizzontale
newWall(R1,C1,R2,C2,R3,C3,R4,C4):- adiacente(R1,C1,R2,C2),adiacente(R3,C3,R4,C4),R1=R3,R1=R2+1,R2=R4,C1=C2,C3=C4,C3=C1+1,not wall(R4,C4,R2,C2,R3,C3,R1,C1).

% Regola per sceglire i muri
scegliMuro(R1,C1,R2,C2,R3,C3,R4,C4)|nonScegliMuro(R1,C1,R2,C2,R3,C3,R4,C4):- newWall(R1,C1,R2,C2,R3,C3,R4,C4),player(ID,_,_,WL,_),myId(ID),WL>0.

% Regola per sceglire se muoversi o no 
muovi(ID,R,C)|nonMuovi(ID,R,C) :- myId(ID),path(ID,R,C,_),newPos(R,C).

% Regole
numMuovi(X):- #count{ID,R,C : muovi(ID,R,C)} = X.
numPiazzaMuro(X):- #count{R1,C1,R2,C2,R3,C3,R4,C4 : scegliMuro(R1,C1,R2,C2,R3,C3,R4,C4)}=X.

:- numPiazzaMuro(X),X>1.
:- numMuovi(X),X>1.
:- numMuovi(X),X>0,numPiazzaMuro(Y),Y<>0.
:- numMuovi(X),X<>0,numPiazzaMuro(Y),Y>0.
:- numMuovi(X),numPiazzaMuro(Y),X=1,Y=1.
:- numMuovi(X),numPiazzaMuro(Y),X=0,Y=0.

% Calcoliamo le celle raggiungibili dai player una volta scelto un muro
raggiunti(cella(R1,C1),cella(R2,C2),1) :- adiacente(R1,C1,R2,C2),not futureWall(R1,C1,R2,C2).
raggiunti(cella(R1,C1),cella(R3,C3),W) :- raggiunti(cella(R1,C1),cella(R2,C2),K),not futureWall(R2,C2,R3,C3),player(ID,R1,C1,_,_),adiacente(R2,C2,R3,C3),W=K+1,W<89.   

% Troviamo il cammino minimo dopo la scelta di un muro
percorsoMinimo(cella(R,C),Cost) :- raggiunti(cella(R,C),_,Cost),Cost = #min{K : raggiunti(cella(R,C),cella(R2,C2),K), destinazione(G,cella(R2,C2)), player(_,R,C,_,G)}.

% Troviamo il cammino massimo dopo la scelta di un muro
percorsoMassimo(cella(R,C),Cost) :- raggiunti(cella(R,C),_,Cost),Cost = #max{K : raggiunti(cella(R,C),cella(R2,C2),K), destinazione(G,cella(R2,C2)), player(_,R,C,_,G)}.

% Ci assicuriamo che esistano almeno 2 cammini (uno per player) che portino all'obiettivo
% Impedisce di scegliere un muro che blocchi l'unica strada
:- numPiazzaMuro(1),#count{cella(R,C) : percorsoMinimo(cella(R,C),Cost)}<>2.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Preferiamo un muro tra il nemico e una cella nel cammino minimo
muroNemicoPath :- scegliMuro(R,C,RR,CC,R3,C3,R4,C4),myId(ID),player(EID,R,C,_,_),ID<>EID,
                path(EID,RR,CC,_).
muroNemicoPath :- scegliMuro(RR,CC,R,C,R3,C3,R4,C4),myId(ID),player(EID,R,C,_,_),ID<>EID,
                path(EID,RR,CC,_).
muroNemicoPath :- scegliMuro(R1,C1,R2,C2,R,C,RR,CC),myId(ID),player(EID,R,C,_,_),ID<>EID,
                path(EID,RR,CC,_).
muroNemicoPath :- scegliMuro(R1,C1,R2,C2,RR,CC,R,C),myId(ID),player(EID,R,C,_,_),ID<>EID,
                path(EID,RR,CC,_).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Preferiamo un muro tra due celle nel cammino minimo del nemico
muroPathPath :- scegliMuro(R,C,RR,CC,R3,C3,R4,C4),myId(ID),ID<>EID,
                path(EID,RR,CC,_),path(EID,R,C,_).
muroPathPath :- scegliMuro(RR,CC,R,C,R3,C3,R4,C4),myId(ID),ID<>EID,
                path(EID,RR,CC,_),path(EID,R,C,_).
muroPathPath :- scegliMuro(R1,C1,R2,C2,R,C,RR,CC),myId(ID),ID<>EID,
                path(EID,RR,CC,_),path(EID,R,C,_).
muroPathPath :- scegliMuro(R1,C1,R2,C2,RR,CC,R,C),myId(ID),ID<>EID,
                path(EID,RR,CC,_),path(EID,R,C,_).


% Preferisci muoverti se sei più vicino del nemico e lui ha finito i muri
:~ numPiazzaMuro(1),myId(ID),path(ID,_,_,W1),path(EID,_,_,WE),player(EID,_,_,EWL,_),
        ID<>EID,W1<WE,EWL=0. [1@8]

% Preferisci piazzare un muro se il nemico è a meno di 4 mosse dalla vittoria
:~ numMuovi(1),myId(ID),path(EID,_,_,WE),ID<>EID, WE<=4. [1@7]

% Preferisci muoverti se sei più vicino di 3 mosse 
:~ numPiazzaMuro(1),myId(ID),path(ID,_,_,W1), W1<=3. [1@6]

% Preferisci un muori che massimizzi il percorso avversario
:~ numPiazzaMuro(1),myId(ID),player(EID,RR,CC,_,_)
        ,ID<>EID,percorsoMassimo(cella(RR,CC),MaxCost),percorsoMinimo(cella(RR,CC),MinCost). [MaxCost-MinCost@5]

% Prefersci un muro che dia più fastio a me che all'avversario
:~ numPiazzaMuro(1),myId(ID),player(ID,R,C,_,_),player(EID,RR,CC,_,_)
        ,ID<>EID,percorsoMinimo(cella(R,C),MyCost),percorsoMinimo(cella(RR,CC),EnemyCost),MyCost>EnemyCost. [1@4]

% Preferisci muoverti se tu sei più vicino del nemico
:~ numPiazzaMuro(1),myId(ID),path(ID,_,_,W1),path(EID,_,_,W2),ID<>EID,W2>W1. [1@3]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Preferisci un muro che sta tra il nemico e il una cella sul suo cammino minimo
:~ numPiazzaMuro(1), not muroNemicoPath. [1@2]

% Preferisci un muro che sta sul path del nemico
:~ numPiazzaMuro(1), not muroPathPath. [1@1]


#show scegliMuro/8.
#show muovi/3.