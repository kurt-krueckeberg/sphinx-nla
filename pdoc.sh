# Final robust version of pdoc.sh to avoid "No such file or directory" errors
for file in source/*/*.adoc; do
    # Check if the file actually exists to avoid passing empty strings to pandoc
    [ -e "$file" ] || continue
    
    echo "Converting: $file"
    # Disable all markdown table formats so Pandoc leaves them as <table> tags
    # Note the '-' before each extension to disable it
    pandoc -f asciidoc -t markdown-pipe_tables-multiline_tables-grid_tables-simple_tables --wrap=none "$file" -o "${file%.adoc}.md"
done
