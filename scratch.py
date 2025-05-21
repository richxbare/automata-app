import streamlit as st
st.set_page_config(layout="wide")
import time
import graphviz
from PIL import Image

# DFA definitions (2 DFAs)
dfa1_transitions = {
    '1': {'a': '21', 'b': '25'},
    '2': {'a': '9', 'b': '12'},
    '3': {'a': '13', 'b': '14'},
    '4': {'a': '15', 'b': '16'},
    '5': {'a': '17', 'b': '14'},
    '6': {'a': '15', 'b': '18'},
    '7': {'a': '19', 'b': '10'},
    '8': {'a': '35', 'b': '19'},
    '9': {'a': '19', 'b': '51'},
    '10': {'a': '2', 'b': '19'},
    '11': {'a': '19', 'b': '44'},
    '12': {'a': '13', 'b': '19'},
    '13': {'a': '19', 'b': '12'},
    '14': {'a': '4', 'b': '19'},
    '15': {'a': '19', 'b': '34'},
    '16': {'a': '45', 'b': '19'},
    '17': {'a': '19', 'b': '3'},
    '18': {'a': '17', 'b': '19'},
    '19': {'a': '19', 'b': '20'},
    '20': {'a': '20', 'b': '22'},
    '21': {'a': '29'},
    '22': {'a': '23', 'b': '24'},
    '23': {'a': '23', 'b': '26'},
    '24': {'a': '27', 'b': '28'},
    '25': {'b': '29'},
    '26': {'a': '30', 'b': '28'},
    '27': {'a': '23', 'b': '30'},
    '28': {'a': '30', 'b': '30'},
    '29': {'a': '31', 'b': '32'},
    '30': {'a': '30', 'b': '30'},
    '31': {'a': '33', 'b': '34'},
    '32': {'a': '35', 'b': '36'},
    '33': {'a': '37', 'b': '34'},
    '34': {'a': '38', 'b': '36'},
    '35': {'a': '33', 'b': '39'},
    '36': {'a': '35', 'b': '40'},
    '37': {'a': '41', 'b': '42'},
    '38': {'a': '43', 'b': '44'},
    '39': {'a': '45', 'b': '46'},
    '40': {'a': '47', 'b': '48'},
    '41': {'a': '41', 'b': '49'},
    '42': {'a': '50', 'b': '36'},
    '43': {'a': '37', 'b': '51'},
    '44': {'a': '2', 'b': '46'},
    '45': {'a': '43', 'b': '3'},
    '46': {'a': '4', 'b': '40'},
    '47': {'a': '33', 'b': '5'},
    '48': {'a': '6', 'b': '48'},
    '49': {'a': '7', 'b': '8'},
    '50': {'a': '9', 'b': '10'},
    '51': {'a': '11', 'b': '8'}
}
dfa1_start = '1'
dfa1_accept = ['30']

dfa2_transitions = {
    '1': {'0': '15', '1': '15'},
    '2': {'0': '7', '1': '2'},
    '3': {'0': '8', '1': '9'},
    '4': {'0': '5', '1': '2'},
    '5': {'0': '10', '1': '11'},
    '6': {'0': '8', '1': '11'},
    '7': {'0': '10', '1': '9'},
    '8': {'0': '12', '1': '13'},
    '9': {'0': '6', '1': '12'},
    '10': {'0': '12', '1': '14'},
    '11': {'0': '16', '1': '12'},
    '12': {'0': '12', '1': '12'},
    '13': {'0': '26', '1': '12'},
    '14': {'0': '3', '1': '12'},
    '15': {'0': '16', '1': '17'},
    '16': {'0': '18', '1': '17'},
    '17': {'0': '16', '1': '19'},
    '18': {'0': '20', '1': '21'},
    '19': {'0': '22', '1': '23'},
    '20': {'0': '24', '1': '25'},
    '21': {'0': '26', '1': '27'},
    '22': {'0': '28', '1': '29'},
    '23': {'0': '30', '1': '31'},
    '24': {'0': '24', '1': '32'},
    '25': {'0': '26', '1': '4'},
    '26': {'0': '18', '1': '33'},
    '27': {'0': '22', '1': '2'},
    '28': {'0': '20', '1': '32'},
    '29': {'0': '16', '1': '4'},
    '30': {'0': '28', '1': '33'},
    '31': {'0': '30', '1': '2'},
    '32': {'0': '3', '1': '4'},
    '33': {'0': '6', '1': '4'}
}
dfa2_start = '1'
dfa2_accept = ['12']

# CFGs
cfgs = {
    'CFG 1': """
    S  → aaY | bbY  
    X  → aX | bX | λ  
    Y  → XabaZ | XbabZ | XbbbZ | XaaaZ  
    Z  → abN | baN  
    N  → bbC | aaC  
    C  → B b B b B D  
    B  → aB | λ  
    D  → babX | bbaX | bbbX | abaX
    """,
    'CFG 2': """
    S -> 1A | 0A
    A -> X11YC | X00YC
    X -> 1X | 0X | λ
    Y -> 11Y | 00Y | λ
    C -> 11D | 10D | 00D | 01D
    D -> 1Z0VM
    Z -> 1Z | λ
    V -> 0V | λ
    F -> 00F | λ
    J -> 11F | λ
    M -> FMI | JMI
    I -> 11YX | 00YX
    """
}


def validate_input(string, start, accept_states, transitions):
    current = start
    trace = [current]  # record states for tracing
    for char in string:
        if char in transitions[current]:
            current = transitions[current][char]
            trace.append(current)
        else:
            return False, trace
    return current in accept_states, trace


def visualize_dfa(transitions, start_state, accept_states, highlight_state=None):
    dot = graphviz.Digraph()

    dot.attr(rankdir='LR')



    for state in transitions:
        if state == highlight_state:
            dot.node(state, shape='circle', style='filled', fillcolor='lightgreen')
        elif state in accept_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state, shape='circle')

    dot.node('', shape='none')
    dot.edge('', start_state)

    for from_state, paths in transitions.items():
        for symbol, to_state in paths.items():
            dot.edge(from_state, to_state, label=symbol)
    return dot



st.title("🧑‍💻 Regex DFA Simulator")
selected_dfa = st.selectbox("Choose a DFA", ["DFA 1", "DFA 2"])

if selected_dfa == "DFA 1":
    st.text("Regular Expression: (aa+bb)(a+b)*(aba+bab+bbb+aaa)(ab+ba)(bb+aa)(a+b)*(a*ba*ba*)(bab+bba+bbb+aba)(a+b)*")
    transitions, start, accepts = dfa1_transitions, dfa1_start, dfa1_accept
    selected_cfg = 'CFG 1'
    selected_pda = './image/pda1.png'
else:
    st.text("Regular Expression: (1+0)(1+0)* (11+00)(11+00)* (1+0)(0+1)(11*00*)((00)* + (11)*)(11+00)(11+00)*(1+0)*")
    transitions, start, accepts = dfa2_transitions, dfa2_start, dfa2_accept
    selected_cfg = 'CFG 2'
    selected_pda = './image/pda2.png'

# Display initial DFA
placeholder = st.empty()
placeholder.graphviz_chart(visualize_dfa(transitions, start, accepts))

user_input = st.text_input("Enter a string:")

if st.button("Simulate DFA Trace"):
    if user_input:
        result, trace = validate_input(user_input, start, accepts, transitions)

        # Animate inside the same placeholder
        for state in trace:
            dot = visualize_dfa(transitions, start, accepts, highlight_state=state)
            placeholder.graphviz_chart(dot)
            time.sleep(0.5)  # pause between steps

        if result:
            st.success("✅ ACCEPTED")
        else:
            st.error("❌ REJECTED")

if st.button("Show CFG"):
    st.code(cfgs[selected_cfg], language="text")

if st.button("Show PDA"):
    try:
        img = Image.open(selected_pda)

        max_width = 600
        w_percent = (max_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img_resized = img.resize((max_width, h_size), Image.LANCZOS)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img_resized, use_container_width=False)

    except Exception as e:
        st.error(f"Error loading image: {e}")



