# Requirements

Depending on your setup, you might need different tools to develop on argos. We try to list them here.

## Mac OS

### Gnu Sed

You will need to have gnu-sed installed. "sed" installed by default on MacOS machines differ from the gnu version (It's used for some post-documentation-generation hooks)

```bash

brew install gnu-sed

# This will explain how to add it to your path (to replace the default one)
brew info gnu-sed
```