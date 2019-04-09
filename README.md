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

The setting FAST should be set to True when one wants to run the fast partition refinement algorithm. This is used 
for 'threepaths'-type graphs.

The setting TREE_CHECK should be set to True when running the program with tree-type graphs. When running other types 
graphs, it may be True or False, as it will have to effect on the execution of the program.

The setting TWIN_CHECK should be set to True when running the program with cographs. When running other types of graphs,
it may be True or False, as it will have to effect on the execution of the program.
