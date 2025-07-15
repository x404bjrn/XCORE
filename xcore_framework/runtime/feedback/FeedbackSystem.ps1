# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
function Strip-Ansi {
    param([string]$line)
    return $line -replace "`e\[[\d;]*[A-Za-z]", ""
}

function Feedback {
    param(
        [string[]]$OutputLines,
        [string]$Result,
        [string]$Mode = "cli"
    )

    foreach ($line in $OutputLines) {
        Write-Host $line
        $cleanLine = Strip-Ansi $line

        if ($Mode -eq "web") {
            Add-Content -Path "xcore_output_web.log" -Value $cleanLine
        } elseif ($Mode -eq "gui") {
            Add-Content -Path "xcore_output_gui.log" -Value $cleanLine
        }
    }

    if ($Mode -eq "web" -and $Result) {
        Add-Content -Path "xcore_result_web.json" -Value $Result
    }
}
