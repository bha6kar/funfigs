# Finish

We use this workflow to complete an existing implementation, not to expand the product. For a finish review we report gaps without editing; when asked to finish the work, we implement relevant corrections within the agreed scope.

We first identify the intended user journey and its acceptance criteria. We inspect the actual entrypoints, tests and running interface where available. We do not invent missing requirements or claim visual verification from source inspection alone.

We exercise the states relevant to the product:

- First run: missing configuration, dependencies, credentials, initial data and onboarding.
- Empty and partial data: meaningful guidance without pretending a failed fetch is an empty result.
- Loading and failure: progress, cancellation, timeouts, retry and recovery without duplicate side effects.
- Defaults: useful initial values, persistence across restarts and predictable reset behaviour.
- Interaction: keyboard access, focus, labels, validation, narrow screens and reduced-motion preferences where applicable.
- Wording: clear actions, accurate errors, units, dates, time zones and no placeholder copy.
- Delivery: documented setup, migrations, compatibility and rollback where the change requires them.

We select only applicable checks. A CLI needs useful exit codes and stderr, not a loading skeleton. A service needs recoverable failure handling, not an onboarding screen.

We fix blockers before cosmetic polish, preserve existing design conventions and add focused regression coverage. We do not publish, deploy, alter live data or send messages merely because a task says "finish". We leave unresolved product choices explicit.
