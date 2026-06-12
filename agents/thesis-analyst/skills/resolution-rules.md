# Skill: resolution rules — writing questions that resolve themselves

A cell is only as good as its resolution rule. The rule must let a stranger
(or an agent) settle the forecast from public sources with zero judgment.

## The rule must name
1. The exact series/table/line: agency, dataset id, series id, geography,
   seasonal adjustment. ("BLS CPI-U, CUUR0000SA0" not "inflation".)
2. The period and print: FIRST PRINT unless the cell says otherwise.
   `resolutionPolicy: first_print` means later revisions are irrelevant.
3. The rounding convention (match the agency's published precision).
4. Where it appears: the release page or data portal URL pattern
   (resolutionSourceUrl points at the release series page, not a news story).
5. For conditionals: the conditioning event, its evaluation date, who/what
   determines it (statute in effect, court order, published guidance), and
   the policy when the condition fails (mark unresolved — never resolve a
   conditional whose condition failed).

## resolutionDate
Always the agency's scheduled release date, verified THIS RUN from the
official calendar (see the data skills for calendar URLs). Never inferred
from typical cadence. If the calendar gives a window, use the scheduled
date and note the window in the rule.

## Anti-patterns (rejected in review)
- "as published by the government" (which series? which print?)
- resolution sources that themselves aggregate (news, FRED for resolution —
  FRED is a fetch mirror, the agency print is the resolver)
- conditions that require judgment ("if the policy is substantially
  delayed") — tie to checkable artifacts (enacted statute, docketed order).
