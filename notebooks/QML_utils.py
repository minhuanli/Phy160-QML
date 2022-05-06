from qiskit.circuit import QuantumCircuit, ParameterVector
from qiskit.circuit.library import NLocal

__all__ = ['UnitaryNlocal4', 'UnitaryNlocal2', 'Controlled_Unitary']

def UnitaryNlocal4(reps=3, name='U4', parameter_prefix='u4_x'):
    '''
    A utility function to create a parameterized Nlocal circuit 
    as an approximation of the N-qubits Unitaries
    
    Parameters
    ----------
    reps: Int, default 3
        How often the rotation blocks and entanglement blocks are repeated. 
        Circuit with more layers should have higher expressive power, 
        but might be hard to optimize
    
    name: str, default 'U4'
        name of the output circuit
        
    parameter_prefix: str, default 'u4_x'
        prefix for the parameters, to avoid conflict when compose
        
    Return
    ------
    Qiskit BlueprintCircuit, the Nlocal citcuit
    '''
    # rotation block:
    rot = QuantumCircuit(2)
    params = ParameterVector('r', 4)
    rot.ry(params[0], 0)
    rot.rz(params[1], 0)
    rot.ry(params[2], 1)
    rot.rz(params[3], 1)

    # entanglement block:
    ent = QuantumCircuit(3)
    params = ParameterVector('e', 3)
    ent.crx(params[0], 0, 1)
    ent.crx(params[1], 1, 2)
    ent.crx(params[2], 0, 2)

    qc_nlocal = NLocal(num_qubits=4, rotation_blocks=rot, reps=reps, name=name,
                       parameter_prefix=parameter_prefix,
                       entanglement_blocks=ent, entanglement='linear',
                       skip_final_rotation_layer=True, insert_barriers=True)
    
    return qc_nlocal


def UnitaryNlocal2(reps=2, name='U2', parameter_prefix='u2_x'):
    '''
    A utility function to create a parameterized Nlocal circuit 
    as an approximation of the 2-qubits Unitaries
    
    Parameters
    ----------
    reps: Int, default 2
        How often the rotation blocks and entanglement blocks are repeated. 
        Circuit with more layers should have higher expressive power, 
        but might be hard to optimize
    
    name: str, default 'U2'
        name of the output circuit
        
    parameter_prefix: str, default 'u2_x'
        prefix for the parameters, to avoid conflict when compose
        
        
    Return
    ------
    Qiskit BlueprintCircuit, the Nlocal citcuit
    '''
    # rotation block:
    rot = QuantumCircuit(2)
    params = ParameterVector('r', 4)
    rot.ry(params[0], 0)
    rot.rz(params[1], 0)
    rot.ry(params[2], 1)
    rot.rz(params[3], 1)

    # entanglement block:
    ent = QuantumCircuit(2)
    params = ParameterVector('e', 4)
    ent.crx(params[0], 0, 1)
    ent.crx(params[1], 1, 0)
    ent.crx(params[2], 0, 1)
    ent.crx(params[3], 1, 0)

    qc_nlocal = NLocal(num_qubits=2, rotation_blocks=rot,reps=2, name=name, 
                       parameter_prefix=parameter_prefix,
                       entanglement_blocks=ent, entanglement='linear',
                       skip_final_rotation_layer=True, insert_barriers=True)
    return qc_nlocal