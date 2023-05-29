
from AFD import AFD
from Alfabeto import Alfabeto
import re
from visual_automata.fa.nfa import VisualNFA, NFA
import visual_automata
nfa = VisualNFA(
    states={"q0", "q1", "q2"},
    input_symbols={"0", "1"},
    transitions={
        "q0": {"": {"q2"}, "1": {"q1"}},
        "q1": {"1": {"q2"}, "0": {"q0", "q2"}},
        "q2": {},
    },
    initial_state="q0",
    final_states={"q0"},
)
nfaprueba = VisualNFA(
states={"q0", "q1", "q2"},
input_symbols={"0", "1"},
transitions={
"q0": {"": {"q2"}, "1": {"q1"}},
"q1": {"1": {"q2"}, "0": {"q0", "q2"}},
"q2": {},
},
initial_state="q0",
final_states={"q0"},
)

big_nfa = VisualNFA(
    states={"q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"},
    input_symbols={"A", "C", "G", "T"},
    transitions={
        "q1": {"A": {"q7"}, "C": {"q4"}, "G": {"q4", "q2"}, "T": {"q4"}},
        "q2": {"A": {"q3", "q6"}, "C": {"q2", "q4"}, "G": {"q3", "q6"}, "T": {"q6"}},
        "q3": {"A": {"q8"}, "C": {"q8"}, "T": {"q8"}},
        "q4": {"A": {"q5"}, "C": {"q4"}, "G": {"q5"}, "T": {"q2", "q4", "q5"}},
        "q5": {"A": {"q3", "q8"}, "C": {"q3", "q8"}, "G": {"q8"}, "T": {"q3", "q8"}},
        "q6": {"A": {"q8"}, "C": {"q8"}, "G": {"q8"}, "T": {"q8"}},
        "q7": {"A": {"q7", "q8"}, "C": {"q7", "q8"}, "G": {"q8"}, "T": {"q3", "q8"}},
        "q8": {}},
    initial_state="q1",
    final_states={"q8"}
)

big_nfa.table
big_nfa.show_diagram("CGC")
