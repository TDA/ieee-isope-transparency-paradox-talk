# The Transparency Paradox
## Calibrating AI Provenance to Privacy Expectations

Sai Prashanth Chandramouli
Meta Platforms, Inc.

### Abstract

Cryptographic provenance can help verifiers assess claims about the origin and editing history of digital media, while exposing information beyond their integrity needs. A newsroom may need to inspect a source's evidence privately; but publishing that evidence can reveal identity, location, or workflow. We examine this transparency paradox through a purpose-bound disclosure framework. A June 2026 synthetic corpus of one million outputs from ten public AI tools provides deployment context: more than 14% carried conformant C2PA packets with readable AI provenance. We distinguish validation, disclosure, and propagation, and define four disclosure tiers ranging from an AI-involvement signal to a restricted provenance chain. We explain how existing C2PA mechanisms can support these policies, then develop newsroom and platform workflows that publish narrow attestations while governing access to richer evidence. The contribution is a practical framework for matching disclosures to a verifier's task and the privacy expectations of the people represented in the record.

**Index Terms** - AI provenance, C2PA, contextual integrity, data minimization, selective disclosure, privacy expectations

### I Introduction

AI-generated and AI-edited media create several integrity questions. A platform may need an AI label, a reader may seek context about AI usage, and a newsroom may need to authenticate a confidential source while validating whether AI was used to manipulate the evidence. These tasks differ in the evidence they require and in the audiences entitled to receive it. A single file can pass through all three contexts, carrying metadata accumulated before its eventual audience is known.

The Coalition for Content Provenance and Authenticity (C2PA) specifies signed claims about an asset's creation and processing [1]. Depending on implementation choices, a workflow may include or inherit creator, device, time, location, or action information. Personal identifiers and rich EXIF metadata are not universally required by C2PA. The privacy question is therefore which information a workflow records, retains, and reveals, rather than whether the standard inevitably discloses it.

We call the resulting tension the **transparency paradox**: evidence useful for private verification can become harmful or misleading when exposed to another audience. The framework developed here separates three decisions: whether a record validates, whether particular claims may be disclosed, and what information should propagate with the asset. This distinction follows contextual integrity, which evaluates information flows through their actors, attributes, and transmission conditions [2]. We develop an operational policy for four disclosure tiers and apply it to publication and resharing.

### II Provenance and Empirical Motivation

#### A What validation establishes

A provenance reader should distinguish packet presence, successful parsing, signature validation, asset binding, and signer trust under the applicable policy [1]. These checks support different conclusions. A readable action claim does not establish a trusted signature. A valid signature does not establish that every statement is true, that the history is complete, or that a depicted event occurred. Even a trusted AI-use assertion does not by itself establish fraud or a policy violation.

Absence of provenance is likewise inconclusive. A file may originate outside a participating workflow, lose metadata during processing, or lack a recoverable record. When evidence is absent or inadequate, an AI-involvement interface should display unknown or insufficient evidence. It must not turn a missing or invalid manifest into an assertion that no AI was involved.

#### B The reported June 2026 corpus

A June 2026 audit constructed a synthetic, non-user-data corpus through public-facing APIs and web applications such as OpenAI ChatGPT, Google Gemini, and Meta AI. It comprised 1,000,000 generated outputs across image, video, and text workflows, with 100,000 outputs per tool across ten public AI tools. More than 14% carried conformant C2PA packets with readable AI provenance. This aggregate observation establishes the presence of provenance-bearing outputs at meaningful scale in the sampled public workflows.

The statistic describes packet conformance and readable AI claims, not a reported rate of trusted signatures, validated content bindings, or source-identifying metadata. Equal sample sizes per selected tool do not estimate the prevalence of provenance across all generated media or weight tools by their real-world usage. Text workflows in the corpus also do not imply that every plain-text output can embed a C2PA manifest. Supporting audit artifacts and the full tool inventory are not available for public release. We make no tool-level comparisons or quantitative claim about privacy harm from this aggregate result.

#### C Public reconstruction procedure

An independent researcher can reconstruct the disclosed sampling design through public tools. Select ten commonly used generation or editing systems spanning the three modalities, and record each product version, collection surface, date, and export format. Prepare modality-appropriate synthetic prompts and editing inputs without user data, document generation settings, and collect 100,000 exported outputs per system. Preserve the original exported assets before downstream conversion or stripping. Record failed requests and exports separately and state the denominator used for each rate.

Inspect each supported asset using a pinned C2PA reader or validator. Record packet presence, parsing and conformance, readable AI-use assertions, signature validation, content binding, and signer trust as separate fields; document software versions and trust policy. Compute the packet-and-readable-AI-claim rate across the generated-output denominator, then report stronger validation outcomes separately. Preserve missing, malformed, unsupported, and unverifiable states rather than interpreting them as evidence of no AI use. This procedure reconstructs the disclosed design, not the exact June 2026 prompts or tool inventory; later measurements can differ as products and export paths change.

For a public inspection method, the open-source c2patool emits a JSON manifest and validation report [3]:

```bash
c2patool --version
c2patool sample.jpg > sample.c2pa.json
```

The accompanying Python helper applies this inspection to explicit file paths and emits one JSON record per asset [4]. It retains the raw report, tool version, and validation results, and identifies two standard trained-AI source types in the active manifest's action assertions. Missing or unrecognized claims remain unknown. This conservative marker check is not a general AI detector or a claim-conformance certification. Even a tool result labeled Valid can coexist with an untrusted signer; use the separate signature, binding, and trust results when making an integrity decision.

### III Verifiers and Privacy Expectations

#### A Different actors need different claims

The creator, the person depicted, the original source, and the signer may be different people or organizations. Creators make attribution choices, sources may require confidentiality, and depicted people can face exposure of their identity or location. A creator who chooses to attach attribution cannot necessarily authorize disclosure about another person. The signer warrants a stated claim under its process; the verifier needs scoped authority to receive supporting information. A receiving system must identify whose information each field describes as well as what the field contributes to its task.

The verifier's question determines the relevant claim. Personal scam defense may use an AI-use signal as one input to further assessment, but that signal cannot establish whether a message is deceptive. A platform's labeling task may require a content category. Newsroom interpretation may require the type of edit; source authentication may require restricted access to richer evidence. An internal audit can justify additional access only under its applicable authority and purpose. These are contextual starting points for policy, not universal sufficiency guarantees.

#### B The newsroom paradox

Consider an illustrative whistleblower photograph. Its provenance may describe digital capture and routine color adjustment while also carrying optional creator, location, capture-time, or device metadata. These fields can help correlate a confidential source. The scenario is a design example, not an observed disclosure incident or evidence that C2PA mandates those fields.

Publishing the rich record can endanger the source. Removing the record can lead an audience to mistake missing credentials for evidence of fabrication. Routine editorial processing can also be misread as material manipulation when an interface displays an edit without context. The newsroom needs a way to preserve its verification conclusion while limiting public disclosure of the evidence behind that conclusion. Verification and publication therefore require separate decisions even when both concern the same asset.

### IV Purpose Bound Disclosure Tiers

Table I defines Tier 0 through Tier 3. A tier specifies an authorized view of available provenance, rather than a demand to collect every listed field. Broader disclosure requires a task-specific justification; a verifier should omit even a tier's example fields when they do not contribute to that task.

**Table I. Disclosure tiers and contextual uses**

| Tier | Authorized view | Example task and boundary |
| --- | --- | --- |
| 0 | Binary AI-involvement claim | Personal scam assessment. Preserve unknown when evidence is absent or inadequate. |
| 1 | Category and coarse time window | General platform labeling, such as AI-generated image, Q2 2026. Omit time if category alone suffices. |
| 2 | Tool class and action type | Newsroom interpretation or contextual labeling, such as generative fill. An action label does not establish scene truth. |
| 3 | Available recorded provenance chain, potentially including tool identifiers and inherited metadata | Restricted source authentication or internal audit. Access remains bounded by authority, relevance, and retention. |

#### A Define the question and select the view

First specify the integrity decision, its recipient, and the evidence needed to make it. A generic request for transparency is too broad to authorize a release. Then choose the least revealing view that can support the decision. The four tiers summarize common views; they are not a total ordering of privacy risk. A coarse timestamp can still identify a source in a small event, and a distinctive tool class can reveal a workflow. Sensitivity must be assessed in context.

Selection should also separate the claim from its validation status. A platform can expose a narrow AI-use claim and indicate whether it has verified the relevant signature and binding without displaying the source's identity. If evidence is inadequate, the system should represent uncertainty or request authorized additional evidence instead of silently escalating disclosure or issuing a stronger conclusion.

#### B Enforce access and govern escalation

Implement the selected view at a system boundary, not only in its interface. Parse incoming manifests defensively, apply relevant validation and trust policies, and avoid copying unnecessary metadata into downstream services or logs. Authenticate recipients of restricted evidence, enforce the purpose and retention period, and record the reason for any richer access. A technically valid record does not grant permission to expose it.

Escalation should identify the requester, the required additional claims, the applicable authority, and the access duration. It need not release an entire chain when only one part is relevant. Audit records themselves should be minimized: logging a full confidential manifest to demonstrate authorized access recreates the exposure that the policy was intended to prevent.

### V Realizing the Policy with C2PA

C2PA provides privacy building blocks, while the purpose and audience policy remains a workflow responsibility [1], [5]. The tiers do not claim a new cryptographic protocol or an evaluated implementation. They specify which authorized view a deployment should create using suitable mechanisms.

At creation, omit optional assertions that no intended verifier needs. Richer optional assertions can be stored remotely with repository access governed separately; the specification and SDK support remote assertion structures [1], [6]. Required validation information must remain available as specified. A public reference is not an access-control mechanism. Repository identifiers, retrieval requests, and response behavior also require review for disclosure or correlation risks.

For known recipients, C2PA guidance describes custom encrypted assertions [5]. Encryption can restrict access to assertion contents but still requires key distribution, recipient authorization, and a policy for onward disclosure. It is not a complete solution for an open-ended audience. Implementers must also preserve whichever information is necessary for the relevant verification operation.

An update manifest can redact or replace assertions through supported mechanisms, as illustrated in the open-source SDK [7]. Its documented redaction path excludes action and hard-binding assertions. Changes must follow the standard's signing and update rules; deleting bytes from a signed assertion and treating the original claim as unchanged is not equivalent. Redaction in a new view does not remove prior copies. Access controls must cover retained originals and any recovery service as well as the newly published view.

After private verification, a newsroom or other verifier can sign a new minimal attestation expressing its own bounded conclusion. That attestation must be bound to the published asset and avoid indirectly restoring the source's identity through ingredient manifests, public repository links, or persistent identifiers. A recipient then trusts the new attester for that stated conclusion. The minimal public attestation does not confer independent access to the underlying evidence or prove that the original record was complete.

### VI Workflows for Publication and Resharing

#### A Private intake and public attestation

A newsroom begins with a restricted intake boundary. When source authentication requires Tier 3 evidence, authorized staff inspect the available chain and record the relevant validation outcomes. They evaluate source claims using editorial judgment and other available evidence. An action history alone cannot determine whether a scene is accurate or an edit is materially misleading.

The editorial decision produces a narrower statement: for example, that the newsroom verified the source through its process and found only specified routine processing in the reviewed record. The wording should identify the scope of the review rather than promise more than its evidence establishes. A signed public view can carry Tier 1 context with an explanatory action statement when necessary, while omitting source identifiers. The original record remains restricted for an authorized accountability process with a defined retention policy.

This design relocates trust to an accountable publisher. Its benefit depends on the publisher's process and on readers understanding the attestation's limits. Interfaces should distinguish an attested editorial conclusion, unavailable evidence, and failed validation. Treating these states as interchangeable would reproduce the trust problem that selective disclosure seeks to address.

#### B Platforms and unknown downstream viewers

Open-internet distribution usually reaches recipients unknown at creation. A narrow claim can travel with, or be recovered for, the asset while richer evidence remains with its creator or a governed repository. Platforms should evaluate embedded and referenced information together so that a safe-looking label does not accompany an openly accessible rich chain.

When a transformation changes asset bytes, the platform must create the relevant new binding and manifest or issue its own accurately scoped attestation. Update manifests apply to supported changes that leave the digital content unchanged [5]. The platform should preserve the authorized public view without widening upstream disclosure. These choices require both technical and policy checks: a public proof that disappears under ordinary resharing offers limited usefulness, while a recoverable proof that exposes a stable source identifier undermines privacy.

### VII Scope and Limitations

The framework has not been evaluated for verification accuracy, user comprehension, privacy outcomes, or operational cost. The synthetic corpus motivates deployment relevance but does not validate tier effectiveness or quantify real-user harm. Future evaluation should examine whether each workflow's minimum view preserves its integrity decision and whether restricted evidence remains protected across publication and resharing.

### VIII Conclusion

AI provenance should support the verifier's integrity question while respecting the privacy expectations of creators, sources, and other people represented in the record. Separating validation, disclosure, and propagation makes those responsibilities explicit. The four tiers offer practitioners a starting point for choosing an authorized view, and existing C2PA mechanisms support several ways to implement it. Restricted verification, narrow public attestation, and governed escalation can preserve useful evidence without routinely releasing the underlying identifying metadata.

### Acknowledgments

OpenAI Codex was used to expand and organize the author's original abstract, slides, and speaker notes; draft and revise the Abstract and Sections I-VIII; and prepare the Section II.C command example, accompanying inspection helper, and reference formatting. The audit figures originated in the author's supplied material.

### References

[1] Coalition for Content Provenance and Authenticity, "C2PA Technical Specification," version 2.4. [Online]. Available: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html

[2] H. Nissenbaum, "Privacy as contextual integrity," Washington Law Review, vol. 79, no. 1, pp. 119-158, 2004. [Online]. Available: https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/

[3] Content Authenticity Initiative, "c2patool," open-source C2PA command-line tool. [Online]. Available: https://github.com/contentauth/c2patool

[4] S. P. Chandramouli, "Sample C2PA inspection method," accompanying code, 2026. [Online]. Available: https://github.com/TDA/ieee-isope-transparency-paradox-talk/tree/codex/isope-extended-abstract/submission

[5] Coalition for Content Provenance and Authenticity, "C2PA Implementation Guidance," version 2.4. [Online]. Available: https://spec.c2pa.org/specifications/specifications/2.4/guidance/Guidance.html

[6] Content Authenticity Initiative, "Cloud data assertion," c2pa-rs source code. [Online]. Available: https://github.com/contentauth/c2pa-rs/blob/main/sdk/src/assertions/cloud_data.rs

[7] Content Authenticity Initiative, "Redacting assertions," c2pa-rs documentation. [Online]. Available: https://github.com/contentauth/c2pa-rs/blob/main/docs/redaction.md
