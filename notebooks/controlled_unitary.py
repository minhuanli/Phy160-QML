from qiskit.circuit import QuantumCircuit

def Controlled_Unitary(k):
    '''
    A utility function to create a controlled unitary with 2 control qubits, 2 target qubits
    
    Parameters
    ----------
    k:  int tuple, represents control qubit state 
        (k_1,k_2) are binary, 1 if x is applied 

    Return
    ------
    Circuit Object
    ''' 
    k_1,k_2 = k
    qc = QuantumCircuit(4)

    # get qc_nlocal circuit but for 2 qubits 
    # circ = UnitaryNlocal(N=2)

    gate = qc.to_gate
    if k_1 == 1:
        qc.x(0)
    if k_2 == 1:
        qc.x(1)
    qc.append(gate.control(2), [0,1,2,3])
    if k_1 == 1:
        qc.x(0)
    if k_2 == 1: 
        qc.x(1)
        
    return qc.to_gate()