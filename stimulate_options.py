import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def evaluate_perpetual_put(S, K, r, sigma):
    """Core ODE analytical solution engine for a Perpetual American Put."""
    gamma2 = - (2.0 * r) / (sigma ** 2)
    S_star = (2.0 * r) / (2.0 * r + sigma ** 2) * K
    
    # Handle scalar inputs for meshgrids structurally by always returning a tuple
    if np.isscalar(S):
        val = (K - S) if S < S_star else (K - S_star) * (S / S_star) ** gamma2
        return val, S_star
    
    # Vectorized execution for flat arrays
    V = np.zeros_like(S)
    exercise_zone = S < S_star
    continuation_zone = S >= S_star
    
    V[exercise_zone] = K - S[exercise_zone]
    V[continuation_zone] = (K - S_star) * (S[continuation_zone] / S_star) ** gamma2
    return V, S_star

# Baseline Configuration
K_value = 100.0
S_vec = np.linspace(20, 160, 100)

# =====================================================================
# VISUALIZATION 1: 3D VOLATILITY SURFACE ANALYSIS V(S, sigma)
# =====================================================================
sigma_vec = np.linspace(0.10, 0.70, 100)
S_mesh, sigma_mesh = np.meshgrid(S_vec, sigma_vec)
V_mesh_vol = np.zeros_like(S_mesh)

for i in range(sigma_mesh.shape[0]):
    for j in range(sigma_mesh.shape[1]):
        # Fixed r = 5% for the volatility surface matrix
        V_mesh_vol[i, j], _ = evaluate_perpetual_put(S_mesh[i, j], K_value, r=0.05, sigma=sigma_mesh[i, j])

fig1 = plt.figure(figsize=(11, 7.5))
ax1 = fig1.add_subplot(111, projection='3d')
surf1 = ax1.plot_surface(S_mesh, sigma_mesh * 100, V_mesh_vol, cmap='viridis', edgecolor='none', alpha=0.9)

ax1.set_title('Perpetual American Put Option: Volatility Surface Matrix $V(S, \\sigma)$', fontsize=12, fontweight='bold', pad=20)
ax1.set_xlabel('Underlying Spot Asset Price ($S$)', fontsize=10, labelpad=10)
ax1.set_ylabel('Annualized Volatility ($\\sigma$ %)', fontsize=10, labelpad=10)
ax1.set_zlabel('Option Contract Value ($V$)', fontsize=10, labelpad=10)

# FIXED: changed 'ax1=ax1' to 'ax=ax1'
fig1.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10, label='Contract Price ($)')

ax1.view_init(elev=28, azim=-125)
plt.tight_layout()
plt.savefig('volatility_surface_3d.png', dpi=300)
print("Saved: volatility_surface_3d.png")

# =====================================================================
# VISUALIZATION 2: 3D INTEREST RATE SURFACE ANALYSIS V(S, r)
# =====================================================================
r_vec = np.linspace(0.01, 0.15, 100)
S_mesh_r, r_mesh = np.meshgrid(S_vec, r_vec)
V_mesh_r = np.zeros_like(S_mesh_r)

for i in range(r_mesh.shape[0]):
    for j in range(r_mesh.shape[1]):
        # Fixed sigma = 25% for the interest rate surface matrix
        V_mesh_r[i, j], _ = evaluate_perpetual_put(S_mesh_r[i, j], K_value, r=r_mesh[i, j], sigma=0.25)

fig2 = plt.figure(figsize=(11, 7.5))
ax2 = fig2.add_subplot(111, projection='3d')
surf2 = ax2.plot_surface(S_mesh_r, r_mesh * 100, V_mesh_r, cmap='plasma', edgecolor='none', alpha=0.9)

ax2.set_title('Perpetual American Put Option: Discount Rate Surface Matrix $V(S, r)$', fontsize=12, fontweight='bold', pad=20)
ax2.set_xlabel('Underlying Spot Asset Price ($S$)', fontsize=10, labelpad=10)
ax2.set_ylabel('Continuous Interest Rate ($r$ %)', fontsize=10, labelpad=10)
ax2.set_zlabel('Option Contract Value ($V$)', fontsize=10, labelpad=10)

# FIXED: changed 'ax2=ax2' to 'ax=ax2'
fig2.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10, label='Contract Price ($)')

ax2.view_init(elev=25, azim=-55)
plt.tight_layout()
plt.savefig('interest_surface_3d.png', dpi=300)
print("Saved: interest_surface_3d.png")

plt.show()