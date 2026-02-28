# QWAN — Quality Without a Name  
## A Variational Bio-Physical Model of Meta-Stable Structural Organization

---

## Overview

This project formalizes Christopher Alexander’s “Quality Without a Name” (QWAN) as a meta-stable regime in dissipative systems.

We propose that structural “aliveness” can be modeled as the minimization of a functional that balances:

- Free energy minimization  
- Configurational freedom  
- Structural coherence  
- Environmental complexity absorption  
- Persistence under dissipative flow  

The framework integrates ideas from:

- Thermodynamics (Gibbs free energy)
- Onsager’s irreversible processes
- Information-theoretic structure (continuous proxies)
- Variational field dynamics
- Evolutionary persistence criteria

This repository contains:

- The theoretical formalization
- A variational derivation
- A computational 2D field simulation
- A proof-of-concept dynamical model
- A conceptual research program

---

# Core Theoretical Model

We define a structural functional:

Φ[x] = ∫Ω [ γ G(x) − α H_s(x) + β I_s(x) ] d r

Where:

- G(x) → Local free energy term
- H_s(x) → Structured configurational freedom
- I_s(x) → Structural coherence
- α, β, γ > 0 → Phenomenological scale-dependent parameters

---

## Operational Continuous Approximations

### Free Energy

G(x) = 1/2 (x − x₀)²

### Structured Freedom (Entropy Proxy)

H_s(x) = (x − ⟨x⟩_σ)²

Where ⟨x⟩_σ is a Gaussian-smoothed local mean.

### Structural Coherence

I_s(x) = |∇x|²

These are continuous structural proxies, not exact Shannon entropies or mutual information.

---

# Variational Dynamics

The system evolves according to:

∂x/∂t = − L (δΦ/δx) + F_env

Where:

- L is a positive-definite Onsager operator
- F_env represents environmental forcing

Expanded form:

∂x/∂t =
− L [ γ(x − x₀)
      − α D_H(x)
      + β (−2 ∇²x) ]
+ F_env

This defines a dissipative variational field system.

---

# Emergent Regimes

By varying parameters:

- α >> β → chaotic / disordered regime  
- β >> α → rigid / homogeneous regime  
- Intermediate region → meta-stable structured patterns  

The intermediate regime exhibits:

- Convergence of Φ  
- Stabilized intermediate freedom  
- Stabilized intermediate coherence  
- Increasing environment correlation  
- Persistent structural organization  

This region is identified as the QWAN regime.

---

# Integrated QWAN Condition

A system is in QWAN state if:

- δΦ/δx = 0  
- δ²Φ/δx² > 0  
- H_s is intermediate (not maximal)  
- I_s is intermediate (not maximal)  
- dA/dt ≥ 0 (increasing environment alignment)

---

# Computational Implementation

The repository includes:

- 2D scalar field simulation
- Gaussian coarse-graining operator
- Laplacian-based coherence dynamics
- Environmental forcing field
- GIF animation rendering
- Observable tracking:
  - Mean functional Φ
  - Energy term
  - Freedom term
  - Coherence term
  - Environment correlation

---

# What This Project Is

- A variational bio-physical formalization
- A phenomenological structural theory
- A computational proof-of-concept
- A bridge between architecture, physics, and biology
- A research program in progress

---

# What This Project Is Not

- A fundamental law of nature
- A symmetry-derived principle
- A microscopic derivation of life
- A metaphysical claim about essence
- A complete theory of biological meaning

It is a regime-level structural description.

---

# Research Directions

- Full parametric phase diagram
- Real mutual information implementation
- Microscopic derivation of parameters
- Application to metabolic networks
- Extension to stochastic thermodynamics
- Coupling with replicator dynamics
- Renormalization analysis across scales

---

# Installation

```bash
pip install numpy matplotlib scipy pillow
```

Run:

```bash
python qwan_simulation.py
```

Output:

```
qwan_simulacao.gif
```

---

# License

None. Just copy and use.

---

# Final Note

This project operationalizes an idea that has historically remained qualitative.

It proposes that structural “aliveness” may be modeled as:

A variational minimum in a dissipative free-energy landscape balancing freedom and form.

This repository represents a first computational implementation of that hypothesis.
