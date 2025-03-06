IFS=$'\n'

echo "Installing ctfd challs"
for name in `git diff --name-only --diff-filter=A HEAD~1`
do
    if [[ $name != *"challenge.yml" ]]; then
        continue
    fi
    dir="$(dirname "${name}")"
    echo "Found $dir"
    python3 -m ctfcli challenge add "$dir"
    python3 -m ctfcli challenge install "$dir"
done
echo "Installing done"
