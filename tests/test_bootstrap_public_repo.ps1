param(
    [string]$SourceRoot = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($SourceRoot)) {
    $SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

$source = [System.IO.Path]::GetFullPath($SourceRoot)
$bootstrap = Join-Path $source "scripts/bootstrap_public_repo.ps1"
$python = Get-Command python -CommandType Application -ErrorAction Stop
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("open-para-bootstrap-" + [guid]::NewGuid())
$insideSource = Join-Path $source (".bootstrap-test-" + [guid]::NewGuid())

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        throw $Message
    }
}

function Invoke-NativeChecked {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$Description
    )

    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = @(& $FilePath @Arguments 2>&1)
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }
    if ($exitCode -ne 0) {
        throw "$Description failed with exit code ${exitCode}: $($output -join [Environment]::NewLine)"
    }
    return @($output | ForEach-Object { $_.ToString() })
}

function Invoke-BootstrapFailure {
    param(
        [string]$Destination,
        [string]$ExpectedMessage
    )

    $failureMessage = $null
    try {
        & $bootstrap -Destination $Destination -SourceRoot $source
        throw "Bootstrap unexpectedly succeeded for unsafe destination: $Destination"
    } catch {
        $failureMessage = $_.Exception.Message
    }

    Assert-True ($failureMessage.Contains($ExpectedMessage)) `
        "Bootstrap failed for the wrong reason. Expected '$ExpectedMessage', got '$failureMessage'."
}

$sourceStatusBefore = @(Invoke-NativeChecked "git" @("-C", $source, "status", "--porcelain=v1", "--untracked-files=all") "Source status check")

try {
    New-Item -ItemType Directory -Path $tempRoot | Out-Null

    Write-Host "Testing bootstrap into a clean destination..."
    $cleanDestination = Join-Path $tempRoot "clean-destination"
    New-Item -ItemType Directory -Path $cleanDestination | Out-Null
    & $bootstrap -Destination $cleanDestination -SourceRoot $source

    $expectedFiles = @(
        "MIGRATION_AUDIT.md",
        "README.md",
        "scripts/preflight_public.py",
        "scripts/validate_repo.py",
        "scripts/validate_templates.py",
        "tests/test_bootstrap_public_repo.ps1",
        "tests/test_validate_templates.py"
    )
    foreach ($relativePath in $expectedFiles) {
        Assert-True (Test-Path -LiteralPath (Join-Path $cleanDestination $relativePath) -PathType Leaf) `
            "Bootstrap output is missing expected public file: $relativePath"
    }

    Assert-True (Test-Path -LiteralPath (Join-Path $cleanDestination ".git") -PathType Container) `
        "Bootstrap output does not contain a new Git repository."

    $history = @(Invoke-NativeChecked "git" @("-C", $cleanDestination, "rev-list", "--all") "Scaffold history check")
    Assert-True ($history.Count -eq 0) "Bootstrap copied source Git history into the scaffold."

    $remotes = @(Invoke-NativeChecked "git" @("-C", $cleanDestination, "remote") "Scaffold remote check")
    Assert-True ($remotes.Count -eq 0) "Bootstrap configured a remote in the scaffold."

    Push-Location $cleanDestination
    try {
        $null = Invoke-NativeChecked $python.Source @("scripts/preflight_public.py", ".") "Public preflight"
        $null = Invoke-NativeChecked $python.Source @("scripts/validate_repo.py", ".") "Repository validation"
        $null = Invoke-NativeChecked $python.Source @("scripts/validate_templates.py", ".") "Rendered-template validation"
        $null = Invoke-NativeChecked $python.Source @("-m", "unittest", "discover", "-s", "tests", "-v") "Unit tests"
    } finally {
        Pop-Location
    }

    Write-Host "Testing rejection of a non-empty destination..."
    $nonEmptyDestination = Join-Path $tempRoot "non-empty-destination"
    New-Item -ItemType Directory -Path $nonEmptyDestination | Out-Null
    $sentinel = Join-Path $nonEmptyDestination "sentinel.txt"
    Set-Content -LiteralPath $sentinel -Value "fictional sentinel" -NoNewline
    $sentinelHash = (Get-FileHash -LiteralPath $sentinel -Algorithm SHA256).Hash

    Invoke-BootstrapFailure $nonEmptyDestination "Destination is not empty"
    Assert-True ((Get-FileHash -LiteralPath $sentinel -Algorithm SHA256).Hash -eq $sentinelHash) `
        "Bootstrap modified the non-empty destination sentinel."
    $nonEmptyItems = @(Get-ChildItem -LiteralPath $nonEmptyDestination -Force)
    Assert-True ($nonEmptyItems.Count -eq 1 -and $nonEmptyItems[0].Name -eq "sentinel.txt") `
        "Bootstrap partially populated a non-empty destination."

    Write-Host "Testing rejection of a destination inside the source repository..."
    Invoke-BootstrapFailure $insideSource "Destination must be outside the source repository"
    Assert-True (-not (Test-Path -LiteralPath $insideSource)) `
        "Bootstrap created a scaffold inside the source repository."

    $sourceStatusAfter = @(Invoke-NativeChecked "git" @("-C", $source, "status", "--porcelain=v1", "--untracked-files=all") "Source status check")
    Assert-True (($sourceStatusBefore -join "`n") -ceq ($sourceStatusAfter -join "`n")) `
        "Bootstrap tests changed the source repository working tree."

    Write-Host "Bootstrap behavior tests passed."
} finally {
    if (Test-Path -LiteralPath $insideSource) {
        Remove-Item -LiteralPath $insideSource -Recurse -Force
    }
    if (Test-Path -LiteralPath $tempRoot) {
        Remove-Item -LiteralPath $tempRoot -Recurse -Force
    }
}

Assert-True (-not (Test-Path -LiteralPath $tempRoot)) "Bootstrap test temporary directory was not cleaned up."
