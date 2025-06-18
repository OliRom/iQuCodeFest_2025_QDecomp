from bloch_sphere_core_in_progress import *

def student_example():
    initial_point = QUANTUM_STATES_Point3D["0"] # Point3D(0, 0, 1)
    operations = [
        BlochGate.Rx(np.pi / 3),
        BlochGate.H_gate(),
        BlochGate.Rz(np.pi / 2)
    ]
    return initial_point, operations


## --------------------------------------------------------

initial_point = Point3D(0, 0, 1)  # Default initial starting point for the Bloch sphere

# you have to change the path...
path_file_traj = '/Users/chei2402/Documents/github/BlochSphere/exercises_trajectories.pkl'
trajectories = load_data_from_pickle(path_file_traj)

def show_exos_traj_students():
    
    # todo: for trotter, change the num_inter number
    for trj_points_colors in trajectories:
        visualize_bloch_trajectory(trj_points_colors)
        # animate_bloch_trajectory(trj_points_colors) # some figure take time to be generated ...
    

# you cane use animate also

def main():
    show_exos_traj_students()

# Example usage to load and visualize the trajectories
if __name__ == "__main__":
    main()