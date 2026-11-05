# Legal bases: purpose before selection

For each operation, record data/data subjects, concrete purpose, necessity, candidate basis, provision, demonstrated requirements, alternatives, risks/safeguards, evidence and validation owner.

- **Contract / preliminary procedures:** demonstrate the relationship and necessity for the data subject's request; a contract does not automatically cover advertising or model training.
- **Legal or regulatory obligation:** identify the rule, obligated party, fields and period. Commercial preference is not a legal obligation.
- **Consent:** specific, informed, free, demonstrable and revocable under the law; refusal must not unnecessarily block functions. Generic consent does not regularize every operation.
- **Legitimate interest:** assess legitimate purpose, necessity, expectations, effects on rights, balancing and safeguards. Consult Article 10 and current guidance; do not apply Article 7 to sensitive data for convenience.
- **Other bases:** research concrete applicability, including protection of life, health protection, credit, research and regular exercise of rights. Do not select based on a field name.

Sensitive data requires Article 11 analysis; minors require Article 14 and current rules. Public-sector processing needs competence/public purpose and specific rules, not copied SaaS clauses. A provider's basis does not automatically determine its customer's basis.

When context or requirements are missing, keep `proposed_legal_basis: null`, an unresolved question and `REQUIRES_HUMAN_REVIEW`. Identify a reasoned proposal as proposed until competent review; do not create an automatic `email = consent` matrix.
