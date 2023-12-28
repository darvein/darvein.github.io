# Simple Workflow Service

## Basics

- task-oriented API, not like SQS which is a message-oriented API
- SWF ensures that tasks are assigned only once (not possible twices like SQS)
- SWF keps track of all events in an app (not like SQS, you need to implement your own app-level tracking)
- makes easy coordinations work between different componentes
- steps like: media processing, web app backends, business process workflows, analytics pipelines
- example: amazon shopping from order, cc check, ship order, completion and end
- needs workers and deciders (EC2 instances)
