#!tm
#states
q0
q1
q2
q3
q4
q5
#initial
q0
#accepting
q5
#inputAlphabet
a-b
#tapeAlphabet
A-B
#transitions
q0:a?q1:A:>
q0:b?q3:B:>
q0:A?q0:A:>
q0:B?q0:B:>
q0:!?q5:!:-
q1:a?q1:a:>
q1:B?q1:B:>
q1:b?q2:B:<
q2:a?q2:a:<
q2:A?q0:A:>
q2:B?q2:B:<
q3:a?q4:A:<
q3:b?q3:b:>
q3:A?q3:A:>
q4:b?q4:b:<
q4:A?q4:A:<
q4:B?q0:B:>