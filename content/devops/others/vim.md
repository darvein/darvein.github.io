# Vim tips

# Content

- [Vim tips](#vim-tips)
- [Content](#content)
    - [Motions](#motions)
    - [Moving things around](#moving-things-around)
    - [Edits](#edits)
    - [Files](#files)
    - [Buffers](#buffers)
    - [Search](#search)
    - [Commands](#commands)
    - [Powerful plugins](#powerful-plugins)
        - [Git](#git)
        - [mkdx](#mkdx)
        - [Copilot](#copilot)
    - [Folding](#folding)

## Motions

- `ciw`: Change the inner word
- `dwi`: Delete current word and enter edit mode
- `d$` or `D`: delete all after current position
- `$`: go to the last char normal-mode
- `w` and `b`: move a word forward or backwards
- `daw`: delete from the current char til the first letter on next word
- `d9w`: delete 9 words
- `dap`: delete around paragraph
- `dd`: delete a line
- `2dd`: delete two lines
- `u` and `ctrl+o`: undo and redo editions
- `4gt`: Go to Tab number 4

more of this:
- `0`: go to beginning
- `$`: go the the endline
- `I`: Edit beginning line
- `A`: Edit end of the line
- `O`: Add blank line above
- `o`: Add blank line below
- `J`: Join bottom line to current
- `D`: Remove all to the end from current char
- `dd`: remove line
- `gg`: jump to first line
- `G`: jump to last line

## Moving things around
- Join (move) the line bellow at the end of the current: `gJ`
- Join lines by removing tabs and newlines (supports visualmode): `J`
- Split a long line in multiple sized lines: `%!fmt --width=75 --split-only`

## Edits
- `shift+I` will go to the first letter in the line and enter edit mode
- `shift+A` will go to the last letter in the line and enter edit mode

## Files
- gf - Edit existing file under cursor in same window
- C-W f - Edit existing file under cursor in split window
- C-W C-F - Edit existing file under cursor in split window
- C-W gf - Edit existing file under cursor in new tabpage

## Buffers
- C-W L - Moves a horizontal buffer to vertical
- `:sball` - Open all buffers horizontally splited

## Search
- `:g//#`: Incremental search and list matches with line numbers

## Commands
Deletions:
- `:.,$d` : From the current line to the end of the file.
- `:.,1d` : From the current line to the beginning of the file.
- `10,$d` : From the 10th line to the end of the file.

Deletions by search:
- `:g /word/d`: Delete lines that has word
- `:g!/word/d`: The opposite
- `:g/^$/d`: Delete blank lines

Copying and pasting
- `:364,757y` Copy range
- `:364,757t2` Copy and paste two lines after current
- `:364,757t.` Copy and paste in current line

## Powerful plugins
### Git
- Git blame

### mkdx
- `LEADER + I`: List headers in a buffer
- `LEADER + i`: Update TOC

### Copilot
- `:Copilot enable`, `:Copilot setup`

## Folding
- `zf#j` creates a fold from the cursor down # lines.
- `zf/string` creates a fold from the cursor to string .
- `zj` moves the cursor to the next fold.
- `zk` moves the cursor to the previous fold.
- `zo` opens a fold at the cursor.
- `zO` opens all folds at the cursor.
- `zm` increases the foldlevel by one.
- `zM` closes all open folds.
- `zr` decreases the foldlevel by one.
- `zR` decreases the foldlevel to zero -- all folds will be open.
- `zd` deletes the fold at the cursor.
- `zE` deletes all folds.
- `[z` move to start of open fold.
- `]z` move to end of open fold.

