# Start Ticket

Look up ticket $ARGUMENTS in Jira using the get_sprint_scope tool.

1. Confirm the ticket is in the current sprint. If it isn't, warn me and stop.
2. Pull the acceptance criteria from the ticket.
3. Use get_contracts to find any API contracts relevant to this ticket's domain.
4. Use get_module_boundaries to identify what modules this ticket touches and what import rules apply.
5. Use get_adjacent_work to check what other tickets are in progress that touch the same services.

Then present a summary:

**Ticket:** [ID] — [Summary]
**Acceptance Criteria:** [list]
**Relevant Contracts:** [list files]
**Modules I Can Touch:** [list with import rules]
**Adjacent Work:** [list tickets that might conflict]
**Suggested Test File:** [path where tests should go]

Ask me to confirm before proceeding. Once confirmed, I'll write the test suite as the specification.
