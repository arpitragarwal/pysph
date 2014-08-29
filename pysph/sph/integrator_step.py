"""Integrator steps for different schemes.

Implement as many stages as needed.
"""


###############################################################################
# `IntegratorStep` class
###############################################################################
class IntegratorStep(object):
    """Subclass this and implement the methods ``stage1`` and ``stage2``.
    Use the same conventions as the equations.
    """
    def initialize(self):
        pass
    def stage1(self):
        pass
    def stage2(self):
        pass


###############################################################################
# `EulerStep` class
###############################################################################
class EulerStep(IntegratorStep):
    """Fast but inaccurate integrator. Use this for testing"""
    def initialize(self):
        pass
    def stage1(self, d_idx, d_u, d_v, d_w, d_au, d_av, d_aw, d_x, d_y,
                  d_z, d_rho, d_arho, dt=0.0):
        d_u[d_idx] += dt*d_au[d_idx]
        d_v[d_idx] += dt*d_av[d_idx]
        d_w[d_idx] += dt*d_aw[d_idx]

        d_x[d_idx] += dt*d_u[d_idx]
        d_y[d_idx] += dt*d_v[d_idx]
        d_z[d_idx] += dt*d_w[d_idx]

        d_rho[d_idx] += dt*d_arho[d_idx]

###############################################################################
# `WCSPHStep` class
###############################################################################
class WCSPHStep(IntegratorStep):
    """Standard Predictor Corrector integrator for the WCSPH formulation

    Use this integrator for WCSPH formulations. In the predictor step,
    the particles are advanced to `t + dt/2`. The particles are then
    advanced with the new force computed at this position.

    This integrator can be used in PEC or EPEC mode.

    The same integrator can be used for other problems. Like for
    example solid mechanics (see SolidMechStep)

    """
    def initialize(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho):
        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_rho0[d_idx] = d_rho[d_idx]

    def stage1(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, d_au, d_av,
                   d_aw, d_ax, d_ay, d_az, d_arho, dt=0.0):
        dtb2 = 0.5*dt
        d_u[d_idx] = d_u0[d_idx] + dtb2*d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dtb2*d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dtb2*d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dtb2 * d_ax[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dtb2 * d_ay[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dtb2 * d_az[d_idx]

        # Update densities and smoothing lengths from the accelerations
        d_rho[d_idx] = d_rho0[d_idx] + dtb2 * d_arho[d_idx]

    def stage2(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, d_au, d_av,
                   d_aw, d_ax, d_ay, d_az, d_arho, dt=0.0):

        d_u[d_idx] = d_u0[d_idx] + dt*d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dt*d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dt*d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dt * d_ax[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dt * d_ay[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dt * d_az[d_idx]

        # Update densities and smoothing lengths from the accelerations
        d_rho[d_idx] = d_rho0[d_idx] + dt * d_arho[d_idx]

###############################################################################
# `WCSPHTVDRK3` Integrator
###############################################################################
class WCSPHTVDRK3Step(IntegratorStep):
    r"""TVD RK3 stepper for WCSPH

    This integrator requires :math:`2` stages for the storage of the
    acceleration variables. 

    """
    def initialize(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho):
        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_rho0[d_idx] = d_rho[d_idx]

    def stage1(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
               d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, 
               d_au, d_av, d_aw, d_ax, d_ay, d_az, d_arho,
               dt=0.0):

        # update velocities
        d_u[d_idx] = d_u0[d_idx] + dt * d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dt * d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dt * d_aw[d_idx]

        # update positions
        d_x[d_idx] = d_x0[d_idx] + dt * d_ax[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dt * d_ay[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dt * d_az[d_idx]

        # update density
        d_rho[d_idx] = d_rho0[d_idx] + dt * d_arho[d_idx]

    def stage2(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
               d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, d_au, d_av,
               d_aw, d_ax, d_ay, d_az, d_arho, dt=0.0):

        # update velocities
        d_u[d_idx] = 0.75*d_u0[d_idx] + 0.25*( d_u[d_idx] + dt * d_au[d_idx] )
        d_v[d_idx] = 0.75*d_v0[d_idx] + 0.25*( d_v[d_idx] + dt * d_av[d_idx] )
        d_w[d_idx] = 0.75*d_w0[d_idx] + 0.25*( d_w[d_idx] + dt * d_aw[d_idx] )

        # update positions
        d_x[d_idx] = 0.75*d_x0[d_idx] + 0.25*( d_x[d_idx] + dt * d_ax[d_idx] )
        d_y[d_idx] = 0.75*d_y0[d_idx] + 0.25*( d_y[d_idx] + dt * d_ay[d_idx] )
        d_z[d_idx] = 0.75*d_z0[d_idx] + 0.25*( d_z[d_idx] + dt * d_az[d_idx] )

        # Update density
        d_rho[d_idx] = 0.75*d_rho0[d_idx] + 0.25*( d_rho[d_idx] + dt * d_arho[d_idx] )

    def stage3(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
               d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, d_au, d_av,
               d_aw, d_ax, d_ay, d_az, d_arho, dt=0.0):

        oneby3 = 1./3.
        twoby3 = 2./3.

        # update velocities
        d_u[d_idx] = oneby3*d_u0[d_idx] + twoby3*( d_u[d_idx] + dt * d_au[d_idx] )
        d_v[d_idx] = oneby3*d_v0[d_idx] + twoby3*( d_v[d_idx] + dt * d_av[d_idx] )
        d_w[d_idx] = oneby3*d_w0[d_idx] + twoby3*( d_w[d_idx] + dt * d_aw[d_idx] )

        # update positions
        d_x[d_idx] = oneby3*d_x0[d_idx] + twoby3*( d_x[d_idx] + dt * d_ax[d_idx] )
        d_y[d_idx] = oneby3*d_y0[d_idx] + twoby3*( d_y[d_idx] + dt * d_ay[d_idx] )
        d_z[d_idx] = oneby3*d_z0[d_idx] + twoby3*( d_z[d_idx] + dt * d_az[d_idx] )

        # Update density
        d_rho[d_idx] = oneby3*d_rho0[d_idx] + twoby3*( d_rho[d_idx] + dt * d_arho[d_idx] )

###############################################################################
# `SolidMechStep` class
###############################################################################
class SolidMechStep(IntegratorStep):
    """Predictor corrector Integrator for solid mechanics problems"""
    def initialize(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho,
                   d_s00, d_s01, d_s02, d_s11, d_s12, d_s22,
                   d_s000, d_s010, d_s020, d_s110, d_s120, d_s220,
                   d_e0, d_e):
        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_rho0[d_idx] = d_rho[d_idx]
        d_e0[d_idx] = d_e[d_idx]

        d_s000[d_idx] = d_s00[d_idx]
        d_s010[d_idx] = d_s01[d_idx]
        d_s020[d_idx] = d_s02[d_idx]
        d_s110[d_idx] = d_s11[d_idx]
        d_s120[d_idx] = d_s12[d_idx]
        d_s220[d_idx] = d_s22[d_idx]

    def stage1(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                  d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, d_au, d_av,
                  d_aw, d_ax, d_ay, d_az, d_arho, d_e, d_e0, d_ae,
                  d_s00, d_s01, d_s02, d_s11, d_s12, d_s22,
                  d_s000, d_s010, d_s020, d_s110, d_s120, d_s220,
                  d_as00, d_as01, d_as02, d_as11, d_as12, d_as22,
                  dt=0.0):
        dtb2 = 0.5*dt
        d_u[d_idx] = d_u0[d_idx] + dtb2*d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dtb2*d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dtb2*d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dtb2 * d_ax[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dtb2 * d_ay[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dtb2 * d_az[d_idx]

        # Update densities and smoothing lengths from the accelerations
        d_rho[d_idx] = d_rho0[d_idx] + dtb2 * d_arho[d_idx]
        d_e[d_idx] = d_e0[d_idx] + dtb2 * d_ae[d_idx]

        # update deviatoric stress components
        d_s00[d_idx] = d_s000[d_idx] + dtb2 * d_as00[d_idx]
        d_s01[d_idx] = d_s010[d_idx] + dtb2 * d_as01[d_idx]
        d_s02[d_idx] = d_s020[d_idx] + dtb2 * d_as02[d_idx]
        d_s11[d_idx] = d_s110[d_idx] + dtb2 * d_as11[d_idx]
        d_s12[d_idx] = d_s120[d_idx] + dtb2 * d_as12[d_idx]
        d_s22[d_idx] = d_s220[d_idx] + dtb2 * d_as22[d_idx]

    def stage2(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                  d_u0, d_v0, d_w0, d_u, d_v, d_w, d_rho0, d_rho, d_au, d_av,
                  d_aw, d_ax, d_ay, d_az, d_arho, d_e, d_ae, d_e0,
                  d_s00, d_s01, d_s02, d_s11, d_s12, d_s22,
                  d_s000, d_s010, d_s020, d_s110, d_s120, d_s220,
                  d_as00, d_as01, d_as02, d_as11, d_as12, d_as22,
                  dt=0.0):

        d_u[d_idx] = d_u0[d_idx] + dt*d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dt*d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dt*d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dt * d_ax[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dt * d_ay[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dt * d_az[d_idx]

        # Update densities and smoothing lengths from the accelerations
        d_rho[d_idx] = d_rho0[d_idx] + dt * d_arho[d_idx]
        d_e[d_idx] = d_e0[d_idx] + dt * d_ae[d_idx]

        # update deviatoric stress components
        d_s00[d_idx] = d_s000[d_idx] + dt * d_as00[d_idx]
        d_s01[d_idx] = d_s010[d_idx] + dt * d_as01[d_idx]
        d_s02[d_idx] = d_s020[d_idx] + dt * d_as02[d_idx]
        d_s11[d_idx] = d_s110[d_idx] + dt * d_as11[d_idx]
        d_s12[d_idx] = d_s120[d_idx] + dt * d_as12[d_idx]
        d_s22[d_idx] = d_s220[d_idx] + dt * d_as22[d_idx]

###############################################################################
# `TransportVelocityStep` class
###############################################################################
class TransportVelocityStep(IntegratorStep):
    """Integrator defined in 'A transport velocity formulation for
    smoothed particle hydrodynamics', 2013, JCP, 241, pp 292--307

    For a predictor-corrector style of integrator, this integrator
    should operate only in PEC mode.

    """
    def initialize(self):
        pass

    def stage1(self, d_idx, d_u, d_v, d_au, d_av, d_uhat, d_auhat, d_vhat,
                  d_avhat, d_x, d_y, dt=0.0):
        dtb2 = 0.5*dt

        # velocity update eqn (14)
        d_u[d_idx] += dtb2*d_au[d_idx]
        d_v[d_idx] += dtb2*d_av[d_idx]

        # advection velocity update eqn (15)
        d_uhat[d_idx] = d_u[d_idx] + dtb2*d_auhat[d_idx]
        d_vhat[d_idx] = d_v[d_idx] + dtb2*d_avhat[d_idx]

        # position update eqn (16)
        d_x[d_idx] += dt*d_uhat[d_idx]
        d_y[d_idx] += dt*d_vhat[d_idx]

    def stage2(self, d_idx, d_u, d_v, d_au, d_av, d_vmag2, dt=0.0):
        dtb2 = 0.5*dt

        # corrector update eqn (17)
        d_u[d_idx] += dtb2*d_au[d_idx]
        d_v[d_idx] += dtb2*d_av[d_idx]

        # magnitude of velocity squared
        d_vmag2[d_idx] = d_u[d_idx]*d_u[d_idx] + d_v[d_idx]*d_v[d_idx]

###############################################################################
# `AdamiVerletStep` class
###############################################################################
class AdamiVerletStep(IntegratorStep):
    """Verlet time integration described in `A generalized wall
    boundary condition for smoothed particle hydrodynamics` 2012, JCP,
    231, pp 7057--7075

    This integrator can operate in either PEC mode or in EPEC mode as
    described in the paper.

    """
    def initialize(self):
        pass

    def stage1(self, d_idx, d_u, d_v, d_au, d_av, d_x, d_y, dt=0.0):
        dtb2 = 0.5*dt

        # velocity predictor eqn (14)
        d_u[d_idx] += dtb2*d_au[d_idx]
        d_v[d_idx] += dtb2*d_av[d_idx]

        # position predictor eqn (15)
        d_x[d_idx] += dtb2*d_u[d_idx]
        d_y[d_idx] += dtb2*d_v[d_idx]

    def stage2(self, d_idx, d_u, d_v, d_au, d_av, d_x, d_y, d_rho, d_arho,
               d_vmag2, dt=0.0):
        dtb2 = 0.5*dt

        # velocity corrector eqn (18)
        d_u[d_idx] += dtb2*d_au[d_idx]
        d_v[d_idx] += dtb2*d_av[d_idx]

        # position corrector eqn (17)
        d_x[d_idx] += dtb2*d_u[d_idx]
        d_y[d_idx] += dtb2*d_v[d_idx]

        # density corrector eqn (16)
        d_rho[d_idx] += dt * d_arho[d_idx]

        # magnitude of velocity squared
        d_vmag2[d_idx] = d_u[d_idx]*d_u[d_idx] + d_v[d_idx]*d_v[d_idx]

###############################################################################
# `GasDFluidStep` class
###############################################################################
class GasDFluidStep(IntegratorStep):
    """Predictor Corrector integrator for Gas-dynamics"""
    def initialize(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z, d_h,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_e, d_e0, d_h0,
                   d_converged, d_omega):
        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_e0[d_idx] = d_e[d_idx]

        d_h0[d_idx] = d_h[d_idx]

        # set the converged attribute to 0 at the beginning of a Group
        d_converged[d_idx] = 0

        # likewise, we set the default omega (grad-h) terms to 1 at
        # the beginning of this Group.
        d_omega[d_idx] = 1.0

    def stage1(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                  d_u0, d_v0, d_w0, d_u, d_v, d_w, d_e0, d_e, d_au, d_av,
                  d_aw, d_ae, dt=0.0):
        dtb2 = 0.5*dt

        d_u[d_idx] = d_u0[d_idx] + dtb2 * d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dtb2 * d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dtb2 * d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dtb2 * d_u[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dtb2 * d_v[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dtb2 * d_w[d_idx]

        # update thermal energy
        d_e[d_idx] = d_e0[d_idx] + dtb2 * d_ae[d_idx]

    def stage2(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_e0, d_e, d_au, d_av,
                   d_aw, d_ae, dt=0.0):

        d_u[d_idx] = d_u0[d_idx] + dt * d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dt * d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dt * d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dt * d_u[d_idx]
        d_y[d_idx] = d_y0[d_idx] + dt * d_v[d_idx]
        d_z[d_idx] = d_z0[d_idx] + dt * d_w[d_idx]

        # Update densities and smoothing lengths from the accelerations
        d_e[d_idx] = d_e0[d_idx] + dt * d_ae[d_idx]

###############################################################################
# `TwoStageRigidBodyStep` class
###############################################################################        
class TwoStageRigidBodyStep(IntegratorStep):
    """Simple rigid-body motion

    At each stage of the integrator, the prescribed velocity and
    accelerations are incremented by dt/2. 

    Note that the time centered velocity is used for updating the
    particle positions. This ensures exact motion for a constant
    acceleration.
    
    """
    def initialize(self, d_idx, d_x, d_y, d_z, d_x0, d_y0, d_z0,
                   d_u, d_v, d_w, d_u0, d_v0, d_w0):

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]
        
    def stage1(self, d_idx, d_x, d_y, d_z, d_x0, d_y0, d_z0,
               d_u, d_v, d_w, d_u0, d_v0, d_w0, d_ax, d_ay, d_az, 
               dt=0.0):

        dtb2 = 0.5*dt

        d_u[d_idx] = d_u0[d_idx] + dtb2 * d_ax[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dtb2 * d_ay[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dtb2 * d_az[d_idx]

        # positions are updated based on the time centered velocity
        d_x[d_idx] = d_x0[d_idx] + dtb2 * 0.5 * (d_u[d_idx] + d_u0[d_idx])
        d_y[d_idx] = d_y0[d_idx] + dtb2 * 0.5 * (d_v[d_idx] + d_v0[d_idx])
        d_z[d_idx] = d_z0[d_idx] + dtb2 * 0.5 * (d_w[d_idx] + d_w0[d_idx])

    def stage2(self, d_idx, d_x, d_y, d_z, d_x0, d_y0, d_z0,
               d_u, d_v, d_w, d_u0, d_v0, d_w0, d_ax, d_ay, d_az,
               dt=0.0):

        d_u[d_idx] = d_u0[d_idx] + dt * d_ax[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dt * d_ay[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dt * d_az[d_idx]

        # positions are updated based on the time centered velocity
        d_x[d_idx] = d_x0[d_idx] + dt * 0.5 * (d_u[d_idx] + d_u0[d_idx])
        d_y[d_idx] = d_y0[d_idx] + dt * 0.5 * (d_v[d_idx] + d_v0[d_idx])
        d_z[d_idx] = d_z0[d_idx] + dt * 0.5 * (d_w[d_idx] + d_w0[d_idx])

###############################################################################
# `OneStageRigidBodyStep` class
###############################################################################
class OneStageRigidBodyStep(IntegratorStep):
    """Simple one stage rigid-body motion """
    def initialize(self, d_idx, d_x, d_y, d_z, d_x0, d_y0, d_z0,
                   d_u, d_v, d_w, d_u0, d_v0, d_w0):

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]

    def stage1(self, d_idx, d_x, d_y, d_z, d_x0, d_y0, d_z0,
               d_u, d_v, d_w, d_u0, d_v0, d_w0, d_ax, d_ay, d_az, 
               dt=0.0):
        pass

    def stage2(self, d_idx, d_x, d_y, d_z, d_x0, d_y0, d_z0,
               d_u, d_v, d_w, d_u0, d_v0, d_w0, d_ax, d_ay, d_az,
               dt=0.0):

        # update velocities
        d_u[d_idx] += dt * d_ax[d_idx]
        d_v[d_idx] += dt * d_ay[d_idx]
        d_w[d_idx] += dt * d_az[d_idx]

        # upadte positions using time-centered velocity
        d_x[d_idx] += dt * 0.5 * (d_u[d_idx] + d_u0[d_idx])
        d_y[d_idx] += dt * 0.5 * (d_v[d_idx] + d_v0[d_idx])
        d_z[d_idx] += dt * 0.5 * (d_w[d_idx] + d_w0[d_idx])


###############################################################################
# `VerletSymplecticWCSPHStep` class
###############################################################################        
class VerletSymplecticWCSPHStep(IntegratorStep):
    """Symplectic second order integrator described in the review
    paper by Monaghan:

    J. Monaghan, "Smoothed Particle Hydrodynamics", Reports on
    Progress in Physics, 2005, 68, pp 1703--1759 [JM05]

    Notes:

    This integrator should run in PEC mode since in the first stage,
    the positions are updated using the current velocity. The
    accelerations are then computed to advance to the full time step
    values.

    This version of the integrator does not update the density. That
    is, the summation density is used instead of the continuity
    equation.

    """
    def stage1(self, d_idx, d_x, d_y, d_z, d_u, d_v, d_w, dt=0.0):

        dtb2 = 0.5 * dt

        # Eq. (5.39) in [JM05]
        d_x[d_idx] += dtb2 * d_u[d_idx]
        d_y[d_idx] += dtb2 * d_v[d_idx]
        d_z[d_idx] += dtb2 * d_w[d_idx]

    def stage2(self, d_idx, d_x, d_y, d_z, d_ax, d_ay, d_az,
               d_u, d_v, d_w, d_au, d_av, d_aw, dt=0.0):

        dtb2 = 0.5 * dt

        # Eq. (5.40) in [JM05]
        d_u[d_idx] += dt * d_au[d_idx]
        d_v[d_idx] += dt * d_av[d_idx]
        d_w[d_idx] += dt * d_aw[d_idx]

        # Eq. (5.41) in [JM05] using XSPH velocity correction
        d_x[d_idx] += dtb2 * d_ax[d_idx]
        d_y[d_idx] += dtb2 * d_ay[d_idx]
        d_z[d_idx] += dtb2 * d_az[d_idx]
