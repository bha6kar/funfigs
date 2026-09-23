# Dependencies

We maintain five versioned skill entrypoints in this repository: `funfigs`, `funfigs-memory`, `docs`, `import-memory` and `morning`. Their instructions and engineering references are local. The engineering bundle contains 19 topic guides, 23 design-pattern recipes and supporting references, commands and agent definitions. Original docs, memory-import and morning workflows remain available as references with portable entrypoints. The morning workflow includes its local headline font and licence. Installation does not download another skill repository.

The installers require Python through uv. Particular tasks may require project-specific build tools, browser rendering or connected document, calendar and messaging services. Missing services are reported rather than simulated. Credentials stay in the host's own configuration.

Optional local-only directories for `docx`, `pdf`, `pptx`, `xlsx` and `skill-creator` are ignored by Git. Existing company skills remain separately managed. Neither category is included in a fresh clone or required by our core engineering workflow.
