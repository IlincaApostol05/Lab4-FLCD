# Lab4-FLCD
I read from 2 json files.In the first part of the project I check if the automaton is deterministic.I have functions(__display_) for printing the states/alphabet/transitions/final-states.
I also have a function that checks for an input sequence(__check) and prints a corresponding message(valid/invalid).

1.constant_name-json:
states = { letter | digit | _ | initial }
letter = "A"|"B"|..|"Z"|"a"|"b"..|"z" 
digit = "0"|"1"|..|"9" 
_: "_"
initial = "A"|"B"|..|"Z"|"a"|"b"..|"z" 
final_states = { letter | digit | _  }

2.integer_name-json:
states = { sign | nonzerodigit | zero | initial }
sign="+"|"-"
non_zero_digit = "1"|"2"|..|"9"
zero = "0"
alphabet = "-"|"+"|"1"|..|"9" 
final_states = { digit | zero | nonzerodigit }


