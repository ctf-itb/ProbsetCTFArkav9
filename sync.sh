IFS=$'\n'
echo "Syncing ctfd challs"
for name in `find -name *challenge.yml`
do
    dir="$(dirname "${name}")"
    echo "Found $dir"
    python3 -m ctfcli challenge sync $dir
done
echo "Syncing done"