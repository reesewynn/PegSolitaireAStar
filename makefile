Solitaire:
	echo "#!/bin/bash" > Solitaire
	echo "python3 solitaire.py \"\$$@\"" >> Solitaire
	chmod u+x Solitaire

	echo "#!/bin/bash" > Solitaire_Solver
	echo "python3 solitaire_solver.py \"\$$@\"" >> Solitaire_Solver
	chmod u+x Solitaire_Solver

clean:
	rm Solitaire
	rm Solitaire_Solver