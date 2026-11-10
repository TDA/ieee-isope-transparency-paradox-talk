# ISoPE 2026 extended paper

This folder contains an expanded paper based on the submitted abstract, the final conference slides, and all 12 slides' speaker notes. It develops the verifier and creator taxonomy, the four disclosure tiers, C2PA implementation choices, and newsroom and platform workflows. The only empirical figures are those already reported in the presentation. Section II.C gives an independent public reconstruction procedure; it does not claim to reproduce the confidential audit's exact tool inventory, prompts, or software.

## Files

- `The-Transparency-Paradox-Extended-Abstract.docx`: editable paper.
- `The-Transparency-Paradox-Extended-Abstract.pdf`: rendered reading copy.
- `extended-paper.md`: editable text source with references.
- `inspect_c2pa.py`: sample Python helper for public C2PA inspection.

The draft is four pages including references, within the published limit. The Word and PDF files use provisional IEEE conference formatting: US Letter, two columns, Times New Roman, 10-point body text. Times New Roman and Courier New are embedded in the PDF. The public call says the IEEE template is "to be provided" and does not publish an organizer-specific download. Use any template supplied in the author acceptance email or submission portal as the final formatting authority.

## Verified submission requirements

Checked on 9 November 2026 against the [official call for presentations](https://ieee-isope.org/call-for-presentations/) and [conference homepage](https://ieee-isope.org/).

| Item | Published requirement |
| --- | --- |
| Deadline | Tuesday, 10 November 2026 |
| Cutoff time and time zone | Not specified on the inspected public pages |
| Length | Up to four pages, including tables and figures, excluding references |
| Format | IEEE template, described as "to be provided" |
| Extended-paper word limit | None stated; the 1,000-word rule applies to the initial presentation abstract |
| Submission route | [EasyChair ISoPE 2026](https://easychair.org/conferences/?conf=isope2026) is the linked portal; the November upload workflow is not described publicly |
| Publication conditions | Original, unpublished, and not under concurrent review elsewhere |
| Notification | 2 December 2026 |
| Camera-ready paper | 15 December 2026, described as optional |
| Copyright instructions | To follow acceptance |
| New experiments or data | No requirement stated |

Authors can instead choose to have their original abstract included as open-access front matter in the proceedings. The formatted paper option is optional.

The [public program](https://ieee-isope.org/program-2026/) lists the presented title and Sai Prashanth Chandramouli as its author. Neither the public call nor the program settles whether November paper review requires anonymization. The July organizer message about initial abstract reviewing described double-blind review; verify the November instruction in the author email or portal.

## Author review before submission

1. The author listing is confirmed: Sai Prashanth Chandramouli, Meta Platforms, Inc., matching the final abstract and slides. Add any contact details required by the organizer's template or upload form.
2. Review the aggregate audit wording. The draft retains the presented June 2026 figures: 1,000,000 outputs, ten tools, 100,000 outputs per tool, and more than 14% with conformant C2PA packets and readable AI provenance. It does not infer that this was a trusted-signature rate or a measured privacy-leak rate.
3. Review the public reconstruction procedure for accuracy and permitted disclosure. Supporting audit artifacts and the complete sample roster are described as unavailable for public release. The named tool examples supplied during drafting have not been published as an exhaustive sampled-tool list.
4. Apply any organizer-issued template, anonymity instruction, exact cutoff, and upload requirement. The public pages do not specify these details. The paper is a draft for author review, not a submission confirmation.
5. Confirm originality and any required citation to prior published work. Earlier abstract versions mention related PEPR work without a complete bibliographic reference; the paper cites verified standards and contextual-integrity scholarship and makes no claim that prior work is unpublished.

## IEEE AI disclosure

[IEEE submission policies](https://conferences.ieeeauthorcenter.ieee.org/author-ethics/guidelines-and-policies/submission-policies/) require acknowledgment of AI-generated content, identifying the system, affected sections, and degree of use. The draft includes an acknowledgment of OpenAI Codex drafting and revising the Abstract and Sections I-VIII from the author's supplied material, plus the command example, accompanying helper, and reference formatting. It does not assert that author review has already occurred.

## Public C2PA inspection example

Install the public [c2patool](https://github.com/contentauth/c2patool). On macOS, its documented Homebrew installation is:

```bash
brew install c2patool
```

Other platforms can use the project's [prebuilt releases](https://github.com/contentauth/c2patool/releases). Record the installed version, then inspect an exported asset using the default summary format:

```bash
c2patool --version
c2patool output.jpg > output.c2pa.json
```

The sample helper uses Python 3's standard library and invokes the installed tool. Run from the repository root:

```bash
python3 submission/inspect_c2pa.py output.jpg clip.mp4 > inspection.jsonl
```

The helper accepts explicit file paths, one or more, and emits one JSON record per file. It does not recursively scan folders. Optional arguments are `--tool /path/to/c2patool`, `--settings /path/to/settings.json`, and `--timeout 60`. It was checked with c2patool 0.27.15, a public repository sample, an unsigned synthetic image, and error/schema cases.

Key output fields:

| Field | Meaning |
| --- | --- |
| `inspection_status` | `readable_manifest`, `no_manifest_reported`, `inspection_error`, or `unrecognized_report` |
| `ai_claim` | `present` for a recognized trained-AI source type in the active manifest; otherwise `unknown` |
| `explicit_ai_source_types` | Recognized IPTC `trainedAlgorithmicMedia` or `compositeWithTrainedAlgorithmicMedia` URI values |
| `reported_validation` | The tool's separate validation status, result, and state fields, when present |
| `tool_report` | Full JSON summary returned by c2patool |
| `c2patool_version` | Version used for the inspection |

This is a conservative provenance inspection example, not a general AI detector. It does not certify manifest conformance or signer trust. It does not infer no AI from missing evidence, scan arbitrary text for tool names, or treat an earlier ingredient's AI marker as an explicit active-manifest claim. A tool-level `Valid` state can coexist with an untrusted signer; inspect the detailed success and failure codes for signature, content binding, and signer trust separately. The summary JSON format is used; `--detailed` produces a different structure and is not passed by the helper.

c2patool settings govern trust and network behavior, including possible retrieval of remote provenance. The helper preserves its raw report, which can contain identifying metadata; apply the paper's disclosure policy to these outputs. Use synthetic test assets when sharing reproducibility results. The script alone does not recreate the confidential audit or compute the published greater-than-14-percent threshold.

## Source and reference decisions

The original abstract was supplied by the author; the presentation source is `The-Transparency-Paradox-ISOPE-2026-Submission.pptx` in the repository. Raw speaker-note transcripts, private audit records, and older drafting options are not part of this delivery.

The manuscript uses C2PA specification and guidance version 2.4, matching the presentation's technical references. The newsroom, private-photo, and academic-integrity cases are illustrative. The disclosure tiers are a proposed policy framework, not a newly implemented or experimentally validated cryptographic protocol. The paper includes the verified EU AI Act Article 50 context. It omits the slides' California statutory example because the current primary statutory text could not be verified during drafting.
