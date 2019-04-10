# Mod7 Graph project
##Main programme
The programme can be started by running main.py. At the top of this file, 
one can find the variable FILENAME and the class Settings.

To select a file to run the algorithm on, set FILENAME (at the top of main.py) 
to "graphs/~filename~" (include the .gr or .grl).


##Options
To run just the GI problem (not the #Aut problem), change the setting AUTOMORPHISM to False at the top of main.py.

To run the #Aut problem, change the setting AUTOMORPHISM to True.

The settings PREPROCESSING should always be set to True, unless one wants to compare the program's execution 
time with and without preprocessing.

The setting DIHEDRAL_COMPLETE_CHECK should also always be set to True, unless one wants to compare the execution time 
of dihedral or complete graphs when using the basic algorithm to the execution time using the 
algorithm designed specifically for diherdral and complete graphs.

The setting FAST_REFINEMENT should be set to True when one wants to run the fast partition refinement algorithm. This 
is used for 'threepaths'-type graphs.

The setting TREE_CHECK should be set to True when running the program with tree-type graphs. When running other types 
graphs, it may be True or False, as it will have to effect on the execution of the program, since it will check if the 
graph has a tree-shape.

The setting TWIN_CHECK should be set to True when running the program with cographs. When TWIN_CHECK is True, 
ALGEBRA_GROUPS and FAST_REFINEMENT should both be set to False. When either ALGEBRA_GROUPS or FAST_REFINEMENT is True,
TWIN_CHECK should be set to False, as it will have to effect on the execution of the program when the graph contains 
twin groups. Also, with big tree graphs, TWIN_CHECK should be set to False, since it slows down when running with main.
Running it with week4 on its own, it executes fast. (To do this: replace the graph name in the directory and replace the
numbers for which graphs you want to compare. Then execute file week4.py)

