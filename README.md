# skillfirst-css-parser
A Python CSS parser that extracts structured CSS information into JSON
The CSS parser extracts selectors and their declarations, including property names, values, and `!important` flags, into structured JSON. This makes CSS styling rules easier for other programs to inspect and process. I used `tinycss2` to parse CSS syntax and added a rule to detect empty declaration values. I tested the edge case `padding: ;` and verified that the parser reports a warning while continuing to process valid declarations.
