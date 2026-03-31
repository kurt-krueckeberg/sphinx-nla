# Converstion Processs

## copy .adoc files

```
find ~/antora-nla/modules -name "*.adoc" -exec sh -c '
    # Extract the module name (the folder immediately after /modules/)
    module=$(echo "$1" | sed -n "s|.*/modules/\([^/]*\)/.*|\1|p")
    
    # Define the target directory in the Sphinx project
    target_dir="$HOME/sphinx-nla/source/$module"
    
    # Create the folder if it does not exist
    mkdir -p "$target_dir"
    
    # Copy the file
    cp "$1" "$target_dir/"
' _ {} \;
```

## Steps

- Run pdoc.sh--does pandoc convert to a markdown flavor similar to MyST.
- `migrate_to_myst.py` -- converted raw html tables to MyST `{list-table}`
  or `{eval-rst}` blocks
- `cleanup_script.py`--fixes the header levels (demoting those accidental
# titles), strips the 1237/ folder prefixes from the Table of Contents,
and forces the exact blank lines Sphinx needs to keep from crashing
- `final_cleanup.py`




