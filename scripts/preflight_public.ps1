param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
python "$PSScriptRoot/preflight_public.py" $Root
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
