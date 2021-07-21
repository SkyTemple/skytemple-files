UNFINISHED/POC/EXPERIMENTAL AND ALL DISCLAIMER

Only activates if PERFORMANCE flag 1 is set (the one that enables the team name). 

Currently not finished, there are some things I'm not sure about.
Mostly ensure that enemies never get PP boosts.
This should already be verified for accuracy and power.

This is only for fun.

Destroys save data, as the save structure has been altered for this.
To implement this, the move boosts feature (via Ginsengs) has been deleted.
In fact, move boosts data gives the space needed for moves exp. data, and the save data is incredibly flexible.

Bits Per Boost * Moves Per Moveset * Pokémon In Storage > Bits Per Move Exp. * Max # Of Moves
       7       *         4         *        555         >         15         *      1024

Move stats are stored BALANCE/mgrowth.bin
150 bytes per move
6 bytes * 25 levels
for each level: 
 - 2 bytes: exp to next level
 - 2 bytes: power bonus
 - 1 byte:  pp bonus
 - 1 byte:  accuracy bonus
 
All stats are additive, for example if level 0 is [25,0,0,0], level 1 is [33,1,1,0] and level 2 [40,1,1,1], 
then stats bonuses for level 2 are: 
25+33+40 = 98 exp. points to reach level 3
0+1+1 = 2 for power
0+1+1 = 2 for pp
0+1+0 = 1 for accuracy

Default config.: 
Normal moves use the same table as in GtI (available in the PMD spreadsheet). 
Status/Misc. moves use a null table.
Each time you use a move you get 3 exp. points, only if the move does not fail. 
Ginseng has been reworked to give 300 (1000 if lucky) exp. points to the topmost move. 

Note: Moves don't have proper stats. They just get boosts depending on their current exp. points.
Things like PP Boost, Accuracy Boost and Power Boosts would need to have another structure to store extra boosts, 
which would require to create and store another structure in the save data.

I.R.D.K.W.I.A.
