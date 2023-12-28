# Chromium architecture

## highlights
- renderer
- host
- each chrome instance has its own renderes and processes
  - same domains can use the same process

## Chrome components
- V8
- ChromeOS
- Chrome Sandbox
- JIT
- Blink (instead of Webkit)

## notes
- if a tab crashes basically shows a sad face which says the previous process is gone and the sad face is a new one, plz
  don't F5
