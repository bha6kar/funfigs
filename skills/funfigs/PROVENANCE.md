# Source provenance

The bundled engineering reference library uses source version 6.3.0, commit `6ce37b9fcf79fe81e43aafa900acb4e3af215330`.

The source manifest declares MIT. The supplied checkout has no standalone LICENSE file. We retain the source's book references and do not invent a missing copyright notice. This package includes third-party reference material.

All 80 Markdown files under the source's skills, references, commands, agents and docs directories are included. This comprises all 19 skill guides, their checklists, all 23 Gang of Four pattern recipes, shared references, four workflow commands, two agent definitions and the source standards document.

Packaging changes: nested SKILL.md files become GUIDE.md to avoid registering duplicate skills; textual references to those filenames are updated. Em dashes and directional arrows are normalised. Each source has a reference-material header. The root SKILL.md and workflows.md provide our adaptation rules. Upstream model, commit and reporting prescriptions remain historical reference material and are superseded by those rules.

The upstream docs/code-standards.md describes the upstream repository. We derive standards for a different project from that project's actual code.

We use the Funfigs namespace for bundled command references and example working directories. This is a local naming adaptation, not a claim of authorship of the source material. Source versions, book references and licence notices remain unchanged.

Supporting workflow sources: [research](upstream/commands/research.md), [plan](upstream/commands/plan.md), [build](upstream/commands/build.md), [debug](upstream/commands/debug.md), [build agent](upstream/agents/build-agent.md), [review agent](upstream/agents/post-gate-agent.md). These describe the upstream implementation, not required execution steps for our adapted workflows.
