param([switch]$Edit, [int]$Port = 0)
$ErrorActionPreference = 'Stop'
if ($Port -eq 0) { $Port = if ($Edit) { 2718 } else { 2719 } }
$lessonFile = Join-Path $PSScriptRoot 'pca_lesson.py'
if ($Edit) {
    & uvx --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' marimo edit $lessonFile --no-sandbox --watch --host 127.0.0.1 --port $Port
} else {
    & uvx --from 'marimo-studio[deno]==0.2.3' marimo-studio view build lesson --target $lessonFile --profile production
    if ($LASTEXITCODE -ne 0) { throw 'Studio build failed.' }
    & uv run --with 'marimo-studio[deno]==0.2.3' --with 'numpy==2.5.3' (Join-Path $PSScriptRoot 'serve_lesson.py') --port $Port
}
