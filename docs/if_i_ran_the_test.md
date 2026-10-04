# If I ran the test — first ask whether the policy is randomizable

**Design discussion, not an experiment or an estimate from this dataset.**

## Question, estimand and outcomes

Could raising fully electric Cat A eligibility from 97 to 110kW change the **market-equilibrium B−A premium gap**, holding the quota regime comparable? The target would be the intention-to-treat difference in a prespecified market-period average B−A gap under assigned 110kW versus retained 97kW eligibility, over a fixed follow-up horizon. This is a different statistical target from this repo's before/after medians. Primary outcome: the market-period gap in S$. Secondary outcomes: A/B level premiums, eligible EV registrations, bidder switching and wait times. Do not substitute gap improvement for EV adoption or welfare. Prespecify a policy-relevant minimum effect, horizon and outcome priority before seeing results.

## Unit and feasibility: the hard part

An eligibility rule changes an auction market, not an isolated person's web page. Buyers/dealers bid against each other, move between A/B and may use Open-category permits. Randomizing **individual buyers or vehicles** would affect shared clearing prices for controls, violating no-interference assumptions. It could estimate an access-assignment effect on selected individuals, not the whole-market equilibrium effect above. A/B are not independent randomization units; auctions repeatedly sample the same connected market.

In a hypothetical setting with genuinely separated, comparable permit markets, randomize **whole markets** to the two policies, block on predetermined quota/supply regime, and keep follow-up calendar periods aligned. Independent replication is the market, not each bid or exercise. Prespecify cluster-level or randomization-based inference; block effects and within-market repeated observations enter the analysis. Audit whether bidders can migrate across clusters. If they can, define spillover/saturation estimands or abandon the isolated-market assumption rather than silently counting contaminated controls.

**Singapore provides one national shared market, not a set of independent clusters.** Creating separate experimental markets would change the auction itself, entail legal/equity constraints, and may not answer the existing-market question. No ready-to-run cluster allocation schedule is justified here.

A whole-market randomized switchback over time is another *candidate*, not a clean default. Dealers can delay orders, bids/COEs can carry forward, and vehicles have long purchase lead times; announcement and treatment carryover undermine washout. Randomization across quota/calendar blocks and a credible washout would be necessary. Time blocks, not bids, would be replicates; serial dependence and carryover must be modeled. If policy reversals or sufficient washout are infeasible, reject this design. A simulated isolated-auction sandbox could test mechanisms without real buyer harm, but would not establish the real-market policy effect.

## Power intuition without invented inputs

No baseline SD, intracluster correlation, serial autocorrelation, minimum meaningful effect or feasible independent-market count is supplied. Therefore no numerical power or sample-size claim is defensible. Start with historical/pilot market-period variability, the chosen effect threshold and interference/carryover assumptions; simulate the actual blocked assignment and analysis. More independent markets/blocks and lower residual variance improve power; many bids within a single market cannot replace missing independent policy units. Longer follow-up trades information against carryover and regime drift. Prespecify interim monitoring/stopping rules and account for multiplicity; do not keep collecting until a preferred sign becomes significant.

## Safeguards and missing evidence

Require legal/regulator approval, public-interest/equity review, transparent eligibility communication, protections against unexpected purchase-cost shocks, stable total quota commitments and a rollback/stop protocol. Do not change real eligibility as a portfolio exercise. Protect bid/registration identities, restrict linkage access, and audit assignment compliance, migration, model availability and concurrent incentives. Keep assignment logs, versioned preregistration and a blinded analysis specification; report deviations, uncertainty and spillovers.

The public CSV has aggregated exercise-category quotas/bids/premiums. It contains **no randomized assignment, independent markets, individual bid values, power/model bands, buyer linkage or untreated counterfactual**. This dataset cannot implement the experiment, estimate its power reliably, or turn A/B into a difference-in-differences treatment/control pair. Better microdata would help describe mechanisms but would not create randomization after the fact. [LTA's eligibility circular](https://onemotoring.lta.gov.sg/content/dam/onemotoring/pdf/Circulars%20to%20ESAs/2022/VRL_04_2022.pdf) establishes the boundary, not assignment.
