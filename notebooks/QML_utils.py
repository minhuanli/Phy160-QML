from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit.circuit.library import NLocal

def UnitaryNlocal(reps=3, N=4):
    '''
    A utility function to create a parameterized Nlocal circuit 
    as an approximation of the N-qubits Unitaries
    
    Parameters
    ----------
    reps: Int, default 3
        How often the rotation blocks and entanglement blocks are repeated. 
        Circuit with more layers should have higher expressive power, 
        but might be hard to optimize
    
    N: Int, default 4
        Number of qubits where the unitary applied to
        
    Return
    ------
    Qiskit BlueprintCircuit, the Nlocal circuit
    '''
    # rotation block:
    rot = QuantumCircuit(2)
    params = ParameterVector('r', 4)
    rot.ry(params[0], 0)
    rot.rz(params[0], 0)
    rot.ry(params[2], 1)
    rot.rz(params[3], 1)

    # entanglement block:
    ent = QuantumCircuit(3)
    params = ParameterVector('e', 3)
    ent.crx(params[0], 0, 1)
    ent.crx(params[1], 1, 2)
    ent.crx(params[2], 0, 2)

    qc_nlocal = NLocal(num_qubits=4, rotation_blocks=rot, reps=reps, 
                       entanglement_blocks=ent, entanglement='linear',
                       skip_final_rotation_layer=True, insert_barriers=True)
    
    return qc_nlocal