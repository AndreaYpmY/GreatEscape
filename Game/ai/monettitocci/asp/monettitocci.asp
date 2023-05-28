% --- INPUT ---
% wall(R1,C1,R2,C2,R3,C3,R4,C4)                             ? Indica che c'è un muro tra le cell {R1,C1,R2,C2} e le cell {R3,C3,R4,C4}
% player(ID,cell(R,C),WL,G)                                 ? Indica che il giocatore con id=ID si trova nella cell(R,C), ha ancora a disposizione WL muri ed ha come obiettivo la prima riga in direzione G (N,S,W,E)
% myId(ID)                                                  ? Indica il proprio ID
% minDistance(ID,cell(R1,C1),cell(R2,C2),Cost)              ? Indica che il percorso del giocatore ID tra cell(R1,C1) e cell(R2,C2), ha distanza minima Cost
% costLimit(ID,CL)                                          ? Indica il costo più alto tra i cammini minimi per ogni giocatore, utilizzato per evitare di generare cammini troppo lunghi
%
% --- OUTPUT ---
% newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4))  ? Indica un nuovo muro in tra le cell {R1,C1,R2,C2} e le cell {R3,C3,R4,C4}
% newPos(cell(R,C))                                         ? Indica la nuova posizione del giocatore (corrente)                  

row(0..8).
col(0..8).

cell(R,C) :- row(R), col(C).

%player(1,cell(8,4),10,"N"). player(2,cell(3,8),10,"W"). costLimit(1,10). costLimit(2,40). myId(1). wall(cell(3,4),cell(3,3),cell(4,4),cell(4,3)). wall(cell(6,3),cell(5,3),cell(6,4),cell(5,4)). wall(cell(2,2),cell(1,2),cell(2,3),cell(1,3)).

singleWall(Cell1,Cell2) :- wall(Cell1,Cell2,_,_).
singleWall(Cell1,Cell2) :- wall(_,_,Cell1,Cell2).
singleWall(Cell2,Cell1) :- singleWall(Cell1,Cell2).

% Dato un obiettivo, segno tutte le celle di arrivo
goalPos("N",cell(0,C)) :- col(C).
goalPos("S",cell(8,C)) :- col(C).
goalPos("W",cell(R,0)) :- row(R).
goalPos("E",cell(R,8)) :- row(R).


adjacent(cell(R1,C),cell(R2,C)) :- cell(R1,C), cell(R2,C), not singleWall(cell(R1,C),cell(R2,C)), |Delta|=1, Delta=R1-R2.
adjacent(cell(R,C1),cell(R,C2)) :- cell(R,C1), cell(R,C2), not singleWall(cell(R,C1),cell(R,C2)), |Delta|=1, Delta=C1-C2.

% Guess
-newPos(cell(NR,NC)) | newPos(cell(NR,NC)) :- cell(NR,NC), adjacent(cell(OR,OC),cell(NR,NC)), player(ID,cell(OR,OC),_,_), myId(ID).
-newSingleWall(cell(R1,C1),cell(R2,C2)) | newSingleWall(cell(R1,C1),cell(R2,C2)) :- cell(R1,C1), cell(R2,C2), adjacent(cell(R1,C1),cell(R2,C2)), R1>R2.
-newSingleWall(cell(R1,C1),cell(R2,C2)) | newSingleWall(cell(R1,C1),cell(R2,C2)) :- cell(R1,C1), cell(R2,C2), adjacent(cell(R1,C1),cell(R2,C2)), C1>C2.

% Check
%% Segno il numero di nuove posizioni e nuovi muri
newPositionNum(X) :- #count{Cell : newPos(Cell)}=X.
newSingleWallNum(X) :- #count{Cell1,Cell2 : newSingleWall(Cell1,Cell2)}=X.
thereIsANewWall :- newSingleWallNum(X), X=2.

%% Non è possibile che venga restituita più di una nuova posizione
:- newPositionNum(X), X>1.

%% Non è possibile che venga restituito un numero di pezzi di muro che sia diverso da 0 o 2
:- newSingleWallNum(X), X>2.
:- newSingleWallNum(X), X=1.

%% Non è possibile che, nel caso in cui venga restituita una nuova posizione, il numero di nuovi muri non sia zero
:- newPositionNum(1), not newSingleWallNum(0).

%% Non è possibile che, nel caso in cui vengano restituiti due nuovi muri, il numero di nuove posizioni non sia zero
:- newSingleWallNum(2), not newPositionNum(0).

%% Non è possibile che non si restituiscano nuove posizioni e nuovi muri
:- newPositionNum(0), newSingleWallNum(0).

%% Non è possibile piazzare nuovi muri se non ne sono rimasti, quindi che non ci sia una nuova posizione nell'AS
:- newPositionNum(0), player(ID,_,0,_), myId(ID).

%% Non è possibile che la nuova posizione sia una cella già occupata (si è deciso di permetterlo)
% busy(cell(R,C)) :- player(_,cell(R,C),_,_).
% :- newPos(Cell), busy(Cell).

% Non è possibile muoversi attraverso un muro
:- player(ID,Cell1,_,_), singleWall(Cell1,Cell2), newPos(Cell2), myId(ID).

%% Non è possibile che, se non ci sono nuove posizioni (quindi sono stati generati dei muri), questi ultimi non siano adiacenti
newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4)) :- newSingleWall(cell(R1,C1),cell(R2,C2)), newSingleWall(cell(R3,C3),cell(R4,C4)), R1=R3, R2=R4, R1<>R2, DC13=C1-C3, DC24=C2-C4, C1<C3, C2<C4, DC13=DC24, |DC13|=1, |DC24|=1.     % Verticale
newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4)) :- newSingleWall(cell(R1,C1),cell(R2,C2)), newSingleWall(cell(R3,C3),cell(R4,C4)), C1=C3, C2=C4, C1<>C2, DR13=R1-R3, DR24=R2-R4, R1<R3, R2<R4, DR13=DR24, |DR13|=1, |DR24|=1.     % Orizzontale
:- newPositionNum(0), #count{R1,C1,R2,C2,R3,C3,R4,C4 : newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4))}<>1.

% Non è possibile che venga generato un nuovo muro che si incroci con uno già esistente
:- newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4)), wall(cell(R5,C5),cell(R6,C6),cell(R7,C7),cell(R8,C8)), R1=R8, C1=C8, R2=R6, C2=C6, R3=R7, C3=C7, R4=R5, C4=C5.

%% Non è possibile che venga generato un nuovo muro esattamente uguale ad uno già presente
:- newWall(Cell1,Cell2,Cell3,Cell4), wall(Cell1,Cell2,Cell3,Cell4).

%% Non è possibile che ci sia un muro sovrapposto (di una coppia di celle) all'altro 
:- newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4)), wall(cell(R5,C5),cell(R6,C6),cell(R7,C7),cell(R8,C8)), R3=R5, C3=C5, R4=R6, C4=C6.
:- newWall(cell(R1,C1),cell(R2,C2),cell(R3,C3),cell(R4,C4)), wall(cell(R5,C5),cell(R6,C6),cell(R7,C7),cell(R8,C8)), R1=R7, C1=C7, R2=R8, C2=C8.

%% Non è possibile che, in presenza di nuovi muri, non ci sia almeno un percorso (minimo) per ogni giocatore (in questo caso 2)
:- thereIsANewWall, #count{Cell1 : minPathCost(Cell1,Cost)}<>2.

%% Segno tutte le celle che entrambi i giocatori possono raggiungere dalla loro posizione
reaches(Cell1,Cell2,1) :- adjacent(Cell1,Cell2), player(_,Cell1,_,_), not newSingleWall(Cell1,Cell2), not newSingleWall(Cell2,Cell1).
reaches(Cell1,Cell3,Cost) :- reaches(Cell1,Cell2,K), player(ID,Cell1,_,_), not newSingleWall(Cell2,Cell3), not newSingleWall(Cell3,Cell2), adjacent(Cell2,Cell3), costLimit(ID,CL), Cost=K+1, Cost<CL+20.  % Faccio in modo che calcoli percorsi lunghi al massimo CL+10, per velocizzare le operazioni, dove CL è il massimo tra i cammini minimi di un giocatore verso ogni cella obiettivo raggiungibile

%% A questo punto segno il numero minimo di passi che ogni giocatore deve sostenere per raggiungere l'obiettivo
minPathCost(Cell1,Cost) :- reaches(Cell1,_,Cost), Cost = #min{K : reaches(Cell1,Cell2,K), goalPos(G,Cell2), player(_,Cell1,_,G)}.

%% Segno la distanza minima che mi separa dall'avversario (potrebbe servire)
%minDistanceToOpponent(Dist) :- Dist=#min{Cost : reaches(Cell1,Cell2,Cost), player(MyID,Cell1,_,_), player(OppID,Cell2,_,_), myID(MyID), MyID<>OppID}.

% Optimize
%% Non vorrei stare ai lati della griglia, così da avere la possibilità di fare più mosse
%%% Se il mio obiettivo è andare a Nord, oppure Sud, pago tante quante sono le caselle che mi separano dal centro delle colonne
%%% Se il mio obiettivo è andare a Ovest, oppure Est, pago tante quante sono le caselle che mi separano dal centro delle righe
:~ newPos(cell(R,C)), player(ID,_,_,"N"), myId(ID), X=4-C, |X|=Z. [Z@1]
:~ newPos(cell(R,C)), player(ID,_,_,"S"), myId(ID), X=4-C, |X|=Z. [Z@1]
:~ newPos(cell(R,C)), player(ID,_,_,"W"), myId(ID), X=4-R, |X|=Z. [Z@1]
:~ newPos(cell(R,C)), player(ID,_,_,"E"), myId(ID), X=4-R, |X|=Z. [Z@1]

%% Non vorrei essere lontano dalla cella "obiettivo" più vicina
%%% Pago tante quante sono le celle che, dopo la nuova mossa, mi separeranno dall'obiettivo
:~ newPos(Cell), minDistance(ID,Cell,_,Cost), myId(ID). [Cost@2]                            % Se genero newPos

%% Non vorrei che l'avversario sia vicino al suo obiettivo e contemporaneamente, non vorrei ostacolarmi più di tanto
%%% Pago tanto quanto sarà la differenza tra quanto perdo io e quanto perde lui, se io perdo più di lui, pago di più
:~ thereIsANewWall, myId(MyID), player(MyID,MyPos,_,_), player(OppID,OppPos,_,_), OppID<>MyID, minDistance(MyID,MyPos,_,MyCostWithoutWall), minDistance(OppID,OppPos,_,OppCostWithoutWall), minPathCost(MyPos,MyCostWithWall), minPathCost(OppPos,OppCostWithWall), MyCost=MyCostWithWall-MyCostWithoutWall, OppCost=OppCostWithWall-OppCostWithoutWall, TotalCost=(MyCost-OppCost)+(81*2). [TotalCost@3]

%% Non vorrei che l'avversario sia a meno di 9* passi dal suo obiettivo e contemporaneamente mi siano rimasti muri (*si può cambiare questo valore più o meno aggressivo in attacco, in questo caso comincia ad attaccare)
:~ newPos(Cell), myId(MyID), player(MyID,_,MyWallsLeft,_), player(OppID,OppPos,_,_), OppID<>MyID, minDistance(OppID,OppPos,_,OppCost), OppCost<9, MyWallsLeft>0. [1@4]

%% Non vorrei piazzare un muro se l'avversario ne ha molti più di me
%%% Pago cifra fissa se la differenza di muri tra me ed il mio avversario è superiore a 3* (*si può cambiare questo valore per renderlo più difensivo in apertura o meno)
:~ thereIsANewWall, player(MyID,_,MyWallsLeft,_), myId(MyID), player(OppID,_,OppWallsLeft,_), MyID<>OppID, Diff=OppWallsLeft-(MyWallsLeft-1), Diff>3. [1@5]

%% Non vorrei muovermi se il cammino minimo dell'avversario è più corto di 3 (È utile soprattutto quando l'avversario non piazza mai muri e quindi arriva molto velocemente verso l'obiettivo)
:~ newPos(Cell), myId(MyID), OppID<>MyID, player(OppID,OppPos,_,_), minPathCost(OppPos,OppCost), OppCost<3. [1@7]

%% Non vorrei piazzare assolutamente muri se l'avversario li ha terminati e sono meno distante di lui dall'obiettivo
%%% Pago cifra fissa se l'avversario ha terminato i muri ed io risulto più vicino di lui (ancora prima di aver piazzato il muro, per questo uso minDistance)
:~ thereIsANewWall, myId(MyID), player(MyID,MyPos,_,_), player(OppID,OppPos,0,_), MyID<>OppID, minDistance(MyID,MyPos,_,MyCost), minDistance(OppID,OppPos,_,OppCost), MyCost<OppCost. [1@8]

%% Non vorrei assolutamente piazzare muri se, dopo averlo fatto, l'avversario sarà sempre alla stessa distanza (utile quando l'avversario è entrato in un corridoio in cui non possono essere piazzati più muri)
:~ thereIsANewWall, myId(MyID), OppID<>MyID, player(OppID,OppPos,_,_), minDistance(OppID,OppPos,_,OppCost), minPathCost(OppPos,OppCost). [1@9]

#show newPos/1.
#show newWall/4.