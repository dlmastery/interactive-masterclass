param(
    [switch]$Edit,
    [ValidateRange(0, 65535)][int]$Port = 0,
    [ValidateRange(1, 65535)][int]$EditorPort = 2728
)

$ErrorActionPreference = 'Stop'
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCommand) {
    throw 'The uv command is required. Install uv, open a new terminal, and rerun this script.'
}

if ($Port -eq 0) {
    $Port = if ($Edit) { $EditorPort } else { 2729 }
}
if (-not $Edit -and $Port -eq $EditorPort) {
    throw 'Slides and the editable notebook require different ports.'
}

# Diagnose conflicts without terminating or reusing an unrelated server.
$probe = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
try {
    $probe.Start()
} catch {
    throw "Port $Port is occupied. Choose -Port with an unused port; existing services were not changed."
} finally {
    $probe.Stop()
}

$notebookFile = Join-Path $PSScriptRoot 'pca_lesson.py'
Push-Location $PSScriptRoot
try {
    if ($Edit) {
        Write-Host "Opening the native Studio editor on http://localhost:$Port/studio/lesson/"
        & $uvCommand.Source tool run --python 3.12 --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' marimo edit $notebookFile --no-sandbox --watch --host 127.0.0.1 --port $Port
        if ($LASTEXITCODE -ne 0) { throw "The notebook editor exited with code $LASTEXITCODE." }
    } else {
        Write-Host 'Building the native Studio lesson with its frozen frontend lockfile...'
        & $uvCommand.Source tool run --python 3.12 --from 'marimo-studio[deno]==0.2.3' marimo-studio view build lesson --target $notebookFile --profile production
        if ($LASTEXITCODE -ne 0) { throw "Studio build failed with code $LASTEXITCODE; presentation was not started." }
        $editorUrl = "http://localhost:$EditorPort/studio/lesson/"
        Write-Host "Keep a second terminal running: ./Start-Lesson.ps1 -Edit -EditorPort $EditorPort"
        & $uvCommand.Source run --python 3.12 --no-project --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' python (Join-Path $PSScriptRoot 'serve_lesson.py') --port $Port --editor-url $editorUrl
        if ($LASTEXITCODE -ne 0) { throw "The presentation server exited with code $LASTEXITCODE." }
    }
} finally {
    Pop-Location
}
