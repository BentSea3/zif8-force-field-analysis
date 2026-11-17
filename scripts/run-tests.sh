
#!/usr/bin/env bash

# Run all repository tests from any working directory.

set -u

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root" || exit 1

test_dirs=(tests)

for dir in studies/01-zif8-force-field-evaluation/figures/reconstructed/*/tests; do
    if [[ -d "$dir" ]]; then
        test_dirs+=("$dir")
    fi
done

failed=0

for dir in "${test_dirs[@]}"; do
    echo
    echo "===== Testing: $dir ====="

    if ! python -m unittest discover -s "$dir" -v; then
        failed=1
    fi
done

echo

if [[ "$failed" -eq 0 ]]; then
    echo "ALL TEST GROUPS PASSED"
else
    echo "ONE OR MORE TEST GROUPS FAILED"
fi

exit "$failed"
