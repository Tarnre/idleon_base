# PROJECT CONTEXT — GAMING MONTE CARLO (SOURCE OF TRUTH)

This document defines the mechanics, constraints, and assumptions specific to
the **gaming_monte_carlo** project.

It extends and overrides global rules defined in:
- `../../context/base_context.md`

All implementation must follow this file exactly.
If a rule is not written here, it does not exist for this project.

---

## PURPOSE

This project uses Monte Carlo simulation to evaluate success, failure, and
reset mechanics under energy costs. The goal is to measure outcomes such as
expected energy per success, variance, and risk trade-offs for different
investment strategies.

This is an **observational simulation**. It does not optimize or modify
mechanics at runtime.

---

## LOCKED: CORE ASSUMPTIONS

The following assumptions are fundamental and must not be changed.

- The system is evaluated via Monte Carlo simulation
- All randomness is sampled explicitly (no closed-form shortcuts)
- Attempts resolve sequentially
- State transitions occur once per attempt
- Energy accounting is deterministic
- Probabilities depend only on current state
- No external services are called during simulation execution
- Simulation behavior must be deterministic for a given RNG seed

---

## LOCKED: STATE MODEL

Each simulation trial maintains the following state variables:

- `k`  
  Current enhancement / investment level

- `attempts`  
  Number of attempts made in the current trial

- `energy_spent`  
  Total energy consumed during the trial

- `resets`  
  Number of reset events triggered

- `success`  
  Boolean indicating whether the trial has succeeded

Additional helper or derived variables may exist in code, but must not alter
the meaning or lifecycle of the above state variables.

---

## LOCKED: TERMINATION CONDITIONS

A trial terminates when **any** of the following conditions are met:

- A success occurs
- A configured maximum attempt count is reached
- A configured maximum energy budget is exceeded

Termination conditions must be explicit and deterministic.

---

## LOCKED: ATTEMPT RESOLUTION FLOW

Each attempt proceeds in the following exact order:

1. Pay attempt energy cost
2. Compute success probability from the current state
3. Roll for success  
   - If success occurs:
     - Set `success = True`
     - End the trial immediately
4. If failure occurs:
   - Roll for reset
   - If reset triggers:
     - Apply reset mechanics
     - Increment `resets`
5. Increment `attempts`
6. Continue to the next attempt if no termination condition is met

This order is invariant and must not be altered.

---

## LOCKED: RESET MECHANICS

On a reset event:

- Apply a **soft reset**:
  - `k = floor(0.7 * k)`
- `k` is never allowed to drop below 0
- Reset does **not** directly consume energy
- Reset does **not** terminate the trial
- Increment the `resets` counter

No additional reset effects exist unless explicitly defined in a TUNABLE
or NOTES section.

---

## TUNABLE: PROBABILITY FUNCTIONS

The functional forms may be adjusted, but must follow the LOCKED flow.

- Success probability:
  - `p_success = f(state)`
- Reset probability:
  - `p_reset = g(state)`

Rules:
- Functions must return values in the range `[0, 1]`
- Functions may depend only on current state variables
- Functions must be deterministic for a given state
- No probability may change mid-attempt

---

## TUNABLE: ENERGY COSTS

Energy costs may be tuned but must be applied consistently.

- Attempt energy cost:
  - `energy_spent += attempt_cost(state)`

- k-investment energy cost (if applicable):
  - Must be applied explicitly outside the attempt resolution flow

Energy costs must not:
- Be probabilistic
- Modify probabilities directly
- Depend on future state

---

## LOCKED: METRICS COLLECTION

The simulation must record the following metrics per run:

- Success rate
- Expected energy per success
- Attempts per trial
- Reset count per trial
- Maximum `k` reached
- Outcome distributions (not just averages)

Metrics are observational only and must not affect mechanics.

---

## REFERENCE MATERIAL (READ-ONLY)

This project may derive mechanics or parameter values from external reference
material, including:

- `references/IdleonToolbox/`

Rules for reference usage:
- Reference code is **read-only**
- No runtime dependency on reference material is allowed
- Any mechanic, formula, or assumption derived from references must be
  explicitly documented in this file before being implemented
- If a reference conflicts with this document, **this document wins**

---

## NOTES / EXPERIMENTAL

This section may be appended by Nyx with:
- Observations from simulation runs
- Edge cases discovered
- Proposed changes to LOCKED or TUNABLE rules

Proposals must not be implemented until this document is updated accordingly.
