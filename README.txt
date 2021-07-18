Kevin lane
Semantics Analyzer

This is my parser which tests for both semantic and syntactic correctness
in a program written in CLite.  In addition to syntactic correctness, the
type rules implemented are the following: no duplicate variables can be
declared, variables must be declared before their use, and variable type must
match the type of the value assigned to it.  This is achieved by maintaining a
symbol table.  Any time a variable is declared, it checks the symbol table to
see if a duplicate exists.  Any time a variable is referenced, it checks to 
see if the variable is in the symbol table.  And any time an a variable is
assigned a value, the variable type is compared to the value type.

This also ensures the semantic correctness of expressions.  Boolean 
addition/subtraction and multiplication/divison are not allowed in this 
version of CLite, regardless of what type of variable the boolean is adding or 
multiplying.  This is because Python interprets True as 1 and False as 0; it 
does not make sense that booleans can be multiplied or added to one another, 
even though it is correct according to Python.  This also does not allow
unlike types to be compared to one another (whether through &&, ||, relations,
or equalities), EXCEPT if the two types are an int and a float.

This also functionally prints out the expressions inside print statements.
Furthermore, while the program checks for the syntactic and semantic 
correctness through the whole program, it does not execute statements (such as
print statements and assignment statements) that appear inside if statements 
with conditions that are false.  This is achieved by using a global variable
executeIf.  Every time a new statement is reached, it is assumed that 
executeIf is true.  If it happens to be an if statement, then executeIf is
the result of that expression AND executeIf.  This accounts for nested if
statements.  It also takes an instance variable of executeIf here, as that
refers to executeIf of the non-nested statement.  ExecuteIf is assigned that 
instance variable after the statement within the if statement is passed.  In 
other words, it accounts for this scenario:

if true:
	if false:
		do something
	do something

It also accounts for else by setting executeIf to not executeIf.  