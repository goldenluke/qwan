# QWAN — Quality Without a Name  
## A Variational Bio-Physical Model of Meta-Stable Structural Organization

---

## Overview

This project formalizes **Christopher Alexander’s “Quality Without a Name” (QWAN)** as a **meta-stable regime in dissipative systems**.

We propose that structural “aliveness” can be modeled as the minimization of a variational functional that balances:

- Free energy minimization  
- Configurational freedom  
- Structural coherence  
- Environmental complexity absorption  
- Persistence under dissipative flow  

The framework integrates:

- Thermodynamics (Gibbs free energy)
- Onsager’s irreversible processes
- Information-theoretic structure
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

$$
\Phi[x] =
\int_\Omega
\left[
\gamma G(x)
- \alpha H_s(x)
+ \beta I_s(x)
\right]
d\mathbf{r}
$$

Where:

- $G(x)$ → Local free energy term
- $H_s(x)$ → Structured configurational freedom
- $I_s(x)$ → Structural coherence
- $\alpha, \beta, \gamma > 0$ → Phenomenological scale-dependent parameters

---

## Operational Continuous Approximations

### Free Energy

$$
G(x) = \frac{1}{2}(x - x_0)^2
$$

### Structured Freedom (Entropy Proxy)

$$
H_s(x) = (x - \langle x \rangle_\sigma)^2
$$

Where $\langle x \rangle_\sigma$ is a Gaussian-smoothed local mean.

### Structural Coherence

$$
I_s(x) = |\nabla x|^2
$$

---

# Variational Dynamics

The system evolves according to:

$$
\frac{\partial x}{\partial t}
=
- L \frac{\delta \Phi}{\delta x}
+ F_{env}
$$

Where:

- $L$ is a positive-definite Onsager operator
- $F_{env}$ represents environmental forcing

Expanded form:

$$
\frac{\partial x}{\partial t}
=
- L
\left[
\gamma(x-x_0)
- \alpha \mathcal{D}_H(x)
+ \beta(-2\nabla^2 x)
\right]
+ F_{env}
$$

This defines a **dissipative variational field system**.

---

# Emergent Regimes

By varying parameters:

- $\alpha \gg \beta$ → Chaotic / disordered regime
- $\beta \gg \alpha$ → Rigid / homogeneous regime
- Intermediate region → Meta-stable structured patterns

The intermediate regime exhibits:

- Convergence of $\Phi$
- Stabilized intermediate freedom
- Stabilized intermediate coherence
- Increasing environment correlation
- Persistent structural organization

This region is identified as the **QWAN regime**.

---

# Integrated QWAN Condition

A system is in QWAN state if:

$$
\boxed{
\text{QWAN}(x^*)
\iff
\begin{cases}
\frac{\delta \Phi}{\delta x} = 0 \\
\frac{\delta^2 \Phi}{\delta x^2} > 0 \\
H_s \text{ intermediate} \\
I_s \text{ intermediate} \\
\frac{dA}{dt} \ge 0
\end{cases}
}
$$

---

# Computational Implementation

The repository includes:

- 2D scalar field simulation
- Gaussian coarse-graining operator
- Laplacian-based coherence dynamics
- Environmental forcing field
- GIF animation rendering
- Observable tracking:
  - Mean functional $\Phi$
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

It is a **regime-level structural description**.

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

MIT License (or specify your preferred license)

---

# Final Note

This project operationalizes an idea that has historically remained qualitative.

It proposes that structural “aliveness” may be modeled as:

> A variational minimum in a dissipative free-energy landscape balancing freedom and form.

This repository represents the first computational implementation of that hypothesis.
