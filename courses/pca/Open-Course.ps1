param(
    [ValidateRange(1, 65535)][int]$EditorPort = 2728,
    [ValidateRange(1, 65535)][int]$PresentationPort = 2729,
    [switch]$NoBrowser,
    [string]$StopRun
)

$ErrorActionPreference = 'Stop'
$runtimeRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '.runtime'))

# Explicit stop mode only touches processes recorded by this launcher and
# verifies their creation times so a recycled PID cannot target another app.
if ($StopRun) {
    $recordPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot $StopRun))
    if (-not $recordPath.StartsWith($runtimeRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'The run record must be inside this course .runtime directory.'
    }
    $record = Get-Content -LiteralPath $recordPath -Raw | ConvertFrom-Json
    foreach ($owned in @($record.processes)) {
        $process = Get-Process -Id $owned.pid -ErrorAction SilentlyContinue
        if (-not $process) { continue }
        if ($process.StartTime.ToUniversalTime().ToString('o') -ne $owned.startedUtc -or $process.ProcessName -ne 'uv') {
            throw "Process $($owned.pid) no longer matches this run. It was not stopped."
        }
        & taskkill.exe /PID $owned.pid /T /F | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "Could not stop recorded process tree $($owned.pid)." }
    }
    Write-Host 'Stopped the matching course process trees. Local logs remain in .runtime.'
    return
}

if ($EditorPort -eq $PresentationPort) { throw 'Editor and presentation need different ports.' }
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCommand) { throw 'Install uv and open a new terminal before launching the course.' }

function Assert-FreePort([int]$Number) {
    $probe = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $Number)
    try { $probe.Start() }
    catch { throw "Port $Number is occupied. Existing services were not changed. Choose different ports or explicitly stop your own prior course run." }
    finally { $probe.Stop() }
}

Assert-FreePort $EditorPort
Assert-FreePort $PresentationPort
Push-Location $PSScriptRoot
try {
    Write-Host 'Building the native Studio presentation before starting either server...'
    & $uvCommand.Source tool run --python 3.12 --from 'marimo-studio[deno]==0.2.3' marimo-studio view build lesson --target pca_lesson.py --profile production
    if ($LASTEXITCODE -ne 0) { throw 'Studio build failed. No server was started.' }
    Assert-FreePort $EditorPort
    Assert-FreePort $PresentationPort

    $runName = 'run-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)
    $runDir = Join-Path $runtimeRoot $runName
    New-Item -ItemType Directory -Path $runDir -Force | Out-Null
    $relativeRecord = ".runtime/$runName/processes.json"
    $relativeLink = ".runtime/$runName/editor-link.txt"
    $recordFile = Join-Path $PSScriptRoot $relativeRecord
    $editorOut = Join-Path $runDir 'editor.out.log'
    $editorErr = Join-Path $runDir 'editor.err.log'
    $ownedProcesses = @()

    function Save-RunRecord {
        @{ schema = 1; editorPort = $EditorPort; presentationPort = $PresentationPort; processes = @($ownedProcesses) } |
            ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $recordFile -Encoding utf8
    }

    # All native argument values here are fixed tokens, numbers, or generated
    # relative paths without spaces. WorkingDirectory handles course paths with spaces.
    $editorArgs = @('tool', 'run', '--python', '3.12', '--with', 'marimo-studio[deno]==0.2.3', '--with', 'numpy==2.5.3', 'marimo', 'edit', 'pca_lesson.py', '--no-sandbox', '--watch', '--headless', '--token', '--host', '127.0.0.1', '--port', "$EditorPort")
    $editor = Start-Process -FilePath $uvCommand.Source -ArgumentList $editorArgs -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $editorOut -RedirectStandardError $editorErr -PassThru
    $ownedProcesses += @{ role = 'editor'; pid = $editor.Id; startedUtc = $editor.StartTime.ToUniversalTime().ToString('o') }
    Save-RunRecord
    Write-Host "Editor started. Run record: $relativeRecord"

    $generatedUrl = $null
    $deadline = [DateTime]::UtcNow.AddSeconds(120)
    $urlPattern = 'http://localhost:' + $EditorPort + '(?:/[^\s\x1b<>"'']*)?\?[^\s\x1b<>"'']*access_token=[^\s\x1b<>"'']+'
    while ([DateTime]::UtcNow -lt $deadline) {
        $editor.Refresh()
        if ($editor.HasExited) { throw "The editor exited. Inspect its ignored logs in $runDir locally; do not publish authentication URLs." }
        foreach ($logFile in @($editorOut, $editorErr)) {
            if (Test-Path -LiteralPath $logFile) {
                $logText = Get-Content -LiteralPath $logFile -Raw
                if ($logText) {
                    $match = [regex]::Match($logText, $urlPattern)
                    if ($match.Success) { $generatedUrl = $match.Value; break }
                }
            }
        }
        if ($generatedUrl) { break }
        Start-Sleep -Milliseconds 300
    }
    if (-not $generatedUrl) { throw "The editor did not emit its generated login URL in time. Use ./Open-Course.ps1 -StopRun $relativeRecord to stop this run." }
    # Never echo this value, put it in command-line arguments, or commit it.
    Set-Content -LiteralPath (Join-Path $PSScriptRoot $relativeLink) -Value $generatedUrl -Encoding utf8
    $generatedUrl = $null

    Assert-FreePort $PresentationPort
    $presentationArgs = @('run', '--python', '3.12', '--no-project', '--with', 'marimo-studio[deno]==0.2.3', '--with', 'numpy==2.5.3', 'python', 'serve_lesson.py', '--port', "$PresentationPort", '--editor-url', "http://localhost:$EditorPort/studio/lesson/", '--editor-url-file', $relativeLink)
    $presentation = Start-Process -FilePath $uvCommand.Source -ArgumentList $presentationArgs -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runDir 'presentation.out.log') -RedirectStandardError (Join-Path $runDir 'presentation.err.log') -PassThru
    $ownedProcesses += @{ role = 'presentation'; pid = $presentation.Id; startedUtc = $presentation.StartTime.ToUniversalTime().ToString('o') }
    Save-RunRecord

    $presentationUrl = "http://localhost:$PresentationPort/lesson/"
    $ready = $false
    $deadline = [DateTime]::UtcNow.AddSeconds(120)
    while ([DateTime]::UtcNow -lt $deadline) {
        $presentation.Refresh()
        if ($presentation.HasExited) { throw "The presentation exited. Inspect its ignored local logs in $runDir." }
        try {
            $response = Invoke-WebRequest -Uri $presentationUrl -TimeoutSec 3 -MaximumRedirection 3
            if ($response.StatusCode -eq 200 -and $response.Content.Contains('marimo-studio-presentation')) { $ready = $true; break }
        } catch { }
        Start-Sleep -Milliseconds 300
    }
    if (-not $ready) { throw "The presentation did not become ready. Use ./Open-Course.ps1 -StopRun $relativeRecord to stop this run." }
    Write-Host "Course: $presentationUrl"
    Write-Host 'Back to editable notebook keeps the generated editor authentication.'
    Write-Host "To stop only this run: ./Open-Course.ps1 -StopRun $relativeRecord"
    Write-Host 'Logs and the authenticated editor URL stay in ignored .runtime files. Do not publish them.'
    if (-not $NoBrowser) { Start-Process $presentationUrl }
} finally {
    Pop-Location
}
