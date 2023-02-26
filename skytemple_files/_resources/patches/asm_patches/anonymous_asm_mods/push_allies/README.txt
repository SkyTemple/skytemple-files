EXPERIMENTAL DISCLAIMER

Push Allies

A method to allow the leader to push allies.

How does it work?

Same as in PSMD: 
- Pressing a direction where an ally is will result in pushing it in that direction.
- Holding B while pressing a direction will exchange places with that ally (original behaviour).

Currently, pushing does not deplete your belly more than an usual turn.

When pushing an ally, the game will check several directions, in that order:
- Straight in line
- A bit to the right
- A bit to the left
- Completely to the right
- Completely to the left

e.g.: If pushing to the right, the game will check right, bottom-right, top-right, bottom, top in that order.
The 3 other directions are not checked (you can't push towards your direction).

If another ally is present in one checked direction, the game will try to push it first in said direction, 
before confirming if the other ally can, or continuing checks with the next available direction if it can't

e.g. Player tries to push Ally 1 to the right. When checking Ally 1 detects Ally 2 bottom-right -> Ally 1 tries to push Ally 2 to the bottom right.

You can't push more than 3 other allies at the same time (this is most of a counter-measure to infinite recursion).

Map Examples

Legend:
X = Wall
. = Empty
0 = Player
1 = Ally 1
2 = Ally 2
3 = Ally 3
E = Enemy

Room 1
Before    After-
XXXXXX    XXXXXX
X.....    X.....
X.01..    X..01.
X.....    X.....
X.....    X.....
Player tries to push Ally 1 to the right (Empty)
-> success, Ally 1 pushed to the right

Room 2
Before    After-
XXXXXX    XXXXXX
X.....    X.....
X.01E.    X..0E.
X.....    X...1.
X.....    X.....
Player tries to push Ally 1 to the right, but there is one enemy
Ally 1 can be pushed to the bottom-right
-> success, Ally 1 pushed to the bottom-right

Room 3
Before    After-
XXXXXX    XXXXXX
X.....    X...1.
X.01E.    X..0E.
X...E.    X...E.
X.....    X.....
Player tries to push Ally 1 to the right, but there is one enemy
Ally 1 cannot be pushed to the bottom-right (enemy)
Ally 1 can be pushed to the top-right
-> success, Ally 1 pushed to the top-right

Room 4
Before    After-
XXXXXX    XXXXXX
X...E.    X...E.
X.01E.    X..0E.
X...E.    X..1E.
X.....    X.....
Player tries to push Ally 1 to the right, but there is one enemy
Ally 1 cannot be pushed to the bottom-right (enemy)
Ally 1 cannot be pushed to the top-right (enemy)
Ally 1 can be pushed to the bottom
-> success, Ally 1 pushed to the bottom

Room 5
Before    After-
XXXXXX    XXXXXX
X...E.    X..1E.
X.01E.    X..0E.
X..EE.    X..EE.
X.....    X.....
Player tries to push Ally 1 to the right, but there is one enemy
Ally 1 cannot be pushed to the bottom-right (enemy)
Ally 1 cannot be pushed to the top-right (enemy)
Ally 1 cannot be pushed to the bottom (enemy)
Ally 1 can be pushed to the top
-> success, Ally 1 pushed to the top

Room 6
Before    After-
XXXXXX    XXXXXX
X..EE.    X..EE.
X.01E.    X.01E.
X..EE.    X..EE.
X.....    X.....
Player tries to push Ally 1 to the right, but there is one enemy
Ally 1 cannot be pushed to the bottom-right (enemy)
Ally 1 cannot be pushed to the top-right (enemy)
Ally 1 cannot be pushed to the bottom (enemy)
Ally 1 cannot be pushed to the top (enemy)
-> failure, nothing happens (still player's turn)

Corridors 1
Before    After-
XXXXXX    XXXXXX
XXX3..    XXX23.
.012XX    ..01XX
XXXXXX    XXXXXX
XXXXXX    XXXXXX
Player tries to push Ally 1 to the right (Ally 2)
Ally 1 tries to push Ally 2 to the right (wall)
Ally 2 can only be pushed to the top (Ally 3)
Ally 2 tries to push Ally 3 to the top (wall)
Ally 3 can only be pushed to the right (empty)
-> success, Ally 3 pushed to the right, Ally 2 to the top, Ally 1 to the right

Corridors 2
Before    After-
XXXXXX    XXXXXX
XXX3E.    XXX3E.
.012XX    .012XX
XXXXXX    XXXXXX
XXXXXX    XXXXXX
Same steps as in Corridors 1, but
Ally 3 cannot be pushed to the right either (enemy)
-> failure, nothing happens (still player's turn)
