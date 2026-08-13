param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if ($null -ne $python) {
    & $python.Source "$PSScriptRoot/preflight_public.py" $Root
    exit $LASTEXITCODE
}

$launcher = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $launcher) {
    & $launcher.Source -3 "$PSScriptRoot/preflight_public.py" $Root
    exit $LASTEXITCODE
}

throw "Python 3 is required to run the public preflight."
