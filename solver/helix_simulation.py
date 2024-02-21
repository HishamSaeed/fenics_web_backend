from fenics import *


def solve_helix_simulation(simulation):
    t_end =  simulation.t_end
    dt = simulation.dt
    k = 300
    u_in = simulation.u_in
    u_out = simulation.u_out

    xml_file =  "./solver/" +  simulation.mesh_file_name
    mesh = Mesh(xml_file)
    fd = MeshFunction('size_t', mesh, "./solver/helix_mesh_facet_region.xml")

    V = FunctionSpace(mesh, 'P', 1)

    bc1 = DirichletBC(V, Constant(u_in), fd, 13)
    bc2 = DirichletBC(V, Constant(u_out), fd, 14)
    bc = [bc1, bc2]

    u = TrialFunction(V)
    v = TestFunction(V)
    u_n = Function(V)

    F = u*v*dx + dt*k*dot(grad(u), grad(v))*dx - u_n*v*dx
    a, L = lhs(F), rhs(F)

    u = Function(V)
    t = simulation.t_start
    vtkfile = File('output/output.pvd')

    num_steps = int(t_end/dt)
    for n in range(num_steps):
        t += dt
        solve(a == L, u, bc)
        u_n.assign(u)
        vtkfile << (u, t)
    
if __name__ == "__main__":
    solve_helix_simulation()