from qiskit.circuit import QuantumCircuit, QuantumRegister, ParameterVector
from qiskit.circuit.library import NLocal
from qiskit.circuit.library.standard_gates import RYGate, RZGate, RXGate
from qiskit import ClassicalRegister, QuantumRegister
from qiskit.providers.aer import AerSimulator
from qiskit import transpile, assemble

import numpy as np


#__all__ = ['UnitaryNlocal4', 'UnitaryNlocal2', 'CU2Nlocal', 'UniformControl2']

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

    qc_nlocal = NLocal(num_qubits=2, rotation_blocks=rot,reps=reps, name=name, 
                       parameter_prefix=parameter_prefix,
                       entanglement_blocks=ent, entanglement='linear',
                       skip_final_rotation_layer=True, insert_barriers=True)
    return qc_nlocal

def CU2Nlocal(controlbit=[1,1], reps=2, name='Ut', parameter_prefix='CU2_x'):
    '''
    A utility function to create a parameterized Nlocal circuit 
    as an approximation of the controlled 2-qubits Unitaries on any 
    type of active control bits
    
    Parameters
    ----------
    controlbit: list of binary, default [1,1]
        What state of the control qubits will activate the unitary 
    
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
    # Rotation Block
    params = ParameterVector('r', 4)

    qr=QuantumRegister(3, name='q')
    circ1=QuantumCircuit(3) 
    CCRY=RYGate(params[0]).control(2) 
    CCRZ=RZGate(params[1]).control(2)
    circ1.append(CCRY, qr)
    circ1.append(CCRZ, qr)

    qr=QuantumRegister(3, name='q')
    circ2=QuantumCircuit(3) 
    CCRY=RYGate(params[2]).control(2) 
    CCRZ=RZGate(params[3]).control(2)
    circ2.append(CCRY, qr)
    circ2.append(CCRZ, qr)

    rot = QuantumCircuit(4)
    rot.append(circ1, [0,1,2])
    rot.append(circ2, [0,1,3])

    # entanglement block:
    params = ParameterVector('e', 4)
    ent = QuantumCircuit(4)

    qr=QuantumRegister(4, name='q')
    circ1=QuantumCircuit(4)
    C3RX=RXGate(params[0]).control(3)
    circ1.append(C3RX, qr)

    qr=QuantumRegister(4, name='q')
    circ2=QuantumCircuit(4)
    C3RX=RXGate(params[1]).control(3)
    circ2.append(C3RX, qr)

    qr=QuantumRegister(4, name='q')
    circ3=QuantumCircuit(4)
    C3RX=RXGate(params[2]).control(3)
    circ3.append(C3RX, qr)

    qr=QuantumRegister(4, name='q')
    circ4=QuantumCircuit(4)
    C3RX=RXGate(params[3]).control(3)
    circ4.append(C3RX, qr)

    ent.append(circ1,[0,1,2,3])
    ent.append(circ2,[0,1,3,2])
    ent.append(circ3,[0,1,2,3])
    ent.append(circ4,[0,1,3,2])

    qc_nlocal = NLocal(num_qubits=4, rotation_blocks=rot, reps=reps, name=name, 
                       parameter_prefix=parameter_prefix,
                       entanglement_blocks=ent, entanglement='linear',
                       skip_final_rotation_layer=True, insert_barriers=True)
    
    before = QuantumCircuit(2)
    after = QuantumCircuit(2)
    
    if controlbit[0] == 0:
        before.x(0)
        after.x(0)
    if controlbit[1] == 0:
        before.x(1)
        after.x(1)
    
    CU2 = QuantumCircuit(4)
    CU2.append(before,[0,1])
    CU2.barrier()
    CU2.append(qc_nlocal,[0,1,2,3])
    CU2.barrier()
    CU2.append(after, [0,1])
    
    return CU2

def UniformControl2(reps=3, name='Ut', parameter_prefix='Ut_x'):
    '''
    Create a Uniformly controlled 2-qubits Unitaries
    '''
    CU11 = CU2Nlocal(controlbit=[1,1], reps=reps, name=name+'_1', parameter_prefix=parameter_prefix+'_1')
    CU01 = CU2Nlocal(controlbit=[0,1], reps=reps, name=name+'_2', parameter_prefix=parameter_prefix+'_2')
    CU10 = CU2Nlocal(controlbit=[1,0], reps=reps, name=name+'_3', parameter_prefix=parameter_prefix+'_3')
    CU00 = CU2Nlocal(controlbit=[0,0], reps=reps, name=name+'_4', parameter_prefix=parameter_prefix+'_4')
    
    UCU2 = QuantumCircuit(4)
    UCU2.append(CU11, [0,1,2,3])
    UCU2.barrier()
    UCU2.append(CU01, [0,1,2,3])
    UCU2.barrier()
    UCU2.append(CU10, [0,1,2,3])
    UCU2.barrier()
    UCU2.append(CU00, [0,1,2,3])
    
    return UCU2


def Create_BBQC4():
    Up = UnitaryNlocal2(reps=2, name=r"$U_p$", parameter_prefix=r"$U_px$")
    Ut2 = UniformControl2(reps=2, name=r"$U_t^{(2)}$", parameter_prefix=r"$U_t^{(2)}x$")
    Uo1 = UnitaryNlocal4(reps=3, name=r"$U_o^{(1)}$", parameter_prefix=r"$U_o^{(1)}$")
    Ut3 = UniformControl2(reps=2, name=r"$U_t^{(3)}$", parameter_prefix=r"$U_t^{(3)}x$")
    Uo2 = UnitaryNlocal4(reps=3, name=r"$U_o^{(2)}$", parameter_prefix=r"$U_o^{(2)}$")
    Uo3 = UnitaryNlocal4(reps=3, name=r"$U_o^{(3)}$", parameter_prefix=r"$U_o^{(3)}$")
    Uo4 = UnitaryNlocal4(reps=3, name=r"$U_o^{(4)}$", parameter_prefix=r"$U_o^{(4)}$")
    Ut4 = UniformControl2(reps=2, name=r"$U_t^{(4)}$", parameter_prefix=r"$U_t^{(4)}x$")
    BBQC = QuantumCircuit(QuantumRegister(16), ClassicalRegister(8))
    BBQC.append(Up, [0,1])
    BBQC.append(Ut2, [0,1,4,5])
    BBQC.append(Ut3, [4,5,8,9])
    BBQC.append(Ut4, [8,9,12,13])
    BBQC.append(Uo1, [0,1,2,3])
    BBQC.append(Uo2, [4,5,6,7])
    BBQC.append(Uo3, [8,9,10,11])
    BBQC.append(Uo4, [12,13,14,15])
    BBQC.measure([2,3,6,7,10,11,14,15], [0,1,2,3,4,5,6,7])
    return BBQC

def convert_str(genelist):
    output = ""
    for i in genelist:
        if i == 0:
            output += '00'
        if i == 1:
            output += '01'
        if i == 2:
            output += '10'
        if i == 3:
            output += '11'
    return output
    
def measure_result(BBQC, simulator, x, n_shots=1000):
    value_dict = dict(zip(BBQC.parameters, x))
    tcirc = transpile(BBQC, simulator)
    qobj = assemble(tcirc, shots=n_shots, parameter_binds = [value_dict])
    result = simulator.run(qobj).result()
    return result.get_counts()

def NLL(counts, databatch, n_shots=1000):
    NLL = 0.
    for i in databatch:
        temp = counts.get(i)
        if temp is None:
            NLL += 2*np.log2(n_shots)
        else:
            NLL += -np.log2(temp/n_shots)
    return NLL/len(databatch)

def gradient(x, databatch, BBQC, simulator, n_shots=1000, eps=0.2):
    epsilon = eps*2*np.pi*np.random.uniform(size=BBQC.num_parameters)
    countsplus = measure_result(BBQC, simulator, x+epsilon, n_shots=n_shots)
    countsminus = measure_result(BBQC, simulator, x-epsilon, n_shots=n_shots)
    counts = measure_result(BBQC, simulator, x, n_shots=n_shots)
    NLL_plus = NLL(countsplus, databatch)
    NLL_minus = NLL(countsminus, databatch)
    FD_dfdx = (NLL_plus - NLL_minus)/2*epsilon
    NLL_x =  NLL(counts, databatch)
    return FD_dfdx, NLL_x

def training(initial_x, traindata, BBQC, similator, batchsize=8, n_steps=50, loss_track=[], alpha=0.01):
    N = len(traindata)
    x = initial_x
    for i in range(n_steps):
        I = np.random.choice(N, size=batchsize)
        databatch = traindata[I]
        dfdx, NLL_x = gradient(x, databatch, BBQC, simulator)
        loss_track.append(NLL_x)
        x = x - alpha * dfdx  
    return x, loss_track