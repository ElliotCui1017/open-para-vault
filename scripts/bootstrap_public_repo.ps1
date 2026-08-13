param(
    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [string]$SourceRoot = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

$source = [System.IO.Path]::GetFullPath($SourceRoot)
$destinationPath = [System.IO.Path]::GetFullPath($Destination)

if ($destinationPath.StartsWith($source + [System.IO.Path]::DirectorySeparatorChar)) {
    throw "Destination must be outside the source repository: $destinationPath"
}

if (Test-Path -LiteralPath $destinationPath) {
    $existing = @(Get-ChildItem -LiteralPath $destinationPath -Force)
    if ($existing.Count -gt 0) {
        throw "Destination is not empty: $destinationPath"
    }
} else {
    New-Item -ItemType Directory -Path $destinationPath | Out-Null
}

$allowlist = @(
    ".gitattributes",
    ".github",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "MIGRATION_AUDIT.md",
    "README.md",
    "RELEASE_NOTES_v0.1.0.md",
    "ROADMAP.md",
    "SECURITY.md",
    "codex",
    "config",
    "docs",
    "examples",
    "scripts",
    "tests",
    "templates"
)

$excludedDirectoryNames = @(
    ".git",
    ".ipynb_checkpoints",
    ".trash",
    ".venv",
    "__pycache__",
    "build",
    "cache",
    "coverage",
    "dist",
    "node_modules",
    "venv"
)

$excludedFileExtensions = @(
    ".bak",
    ".log",
    ".pyc",
    ".pyo",
    ".temp",
    ".tmp"
)

function Copy-PublicDirectory {
    param(
        [string]$SourceDirectory,
        [string]$TargetDirectory
    )

    New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null
    foreach ($child in @(Get-ChildItem -LiteralPath $SourceDirectory -Force)) {
        if ($child.PSIsContainer) {
            if ($excludedDirectoryNames -contains $child.Name) {
                continue
            }
            Copy-PublicDirectory $child.FullName (Join-Path $TargetDirectory $child.Name)
            continue
        }

        if ($excludedFileExtensions -contains $child.Extension.ToLowerInvariant()) {
            continue
        }
        Copy-Item -LiteralPath $child.FullName -Destination $TargetDirectory -Force
    }
}

foreach ($relativePath in $allowlist) {
    $item = Join-Path $source $relativePath
    if (Test-Path -LiteralPath $item) {
        $target = Join-Path $destinationPath $relativePath
        $sourceItem = Get-Item -LiteralPath $item -Force
        if ($sourceItem.PSIsContainer) {
            Copy-PublicDirectory $item $target
        } else {
            Copy-Item -LiteralPath $item -Destination $target -Force
        }
    }
}

Push-Location $destinationPath
try {
    git init -b main

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($null -eq $python) {
        throw "Python 3 is required. Install it, then run: python scripts/preflight_public.py ."
    }

    & $python.Source "scripts/preflight_public.py" "."
    if ($LASTEXITCODE -ne 0) {
        throw "Public preflight failed. Review the findings before committing."
    }

    Write-Host "Public scaffold created at: $destinationPath"
    Write-Host "Review the files, run the validators, and add a remote only after choosing the intended repository."
} finally {
    Pop-Location
}
