#!/bin/bash
# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
feedback() {
    local output_lines=("${!1}")
    local result="$2"
    local mode="$3"

    for line in "${output_lines[@]}"; do
        echo "$line"
        clean_line=$(echo "$line" | sed 's/\x1B\[[0-9;]*[JKmsu]//g')

        if [[ "$mode" == "web" ]]; then
            echo "$clean_line" >> xcore_output_web.log
        elif [[ "$mode" == "gui" ]]; then
            echo "$clean_line" >> xcore_output_gui.log
        fi
    done

    if [[ "$mode" == "web" && -n "$result" ]]; then
        echo "$result" >> xcore_result_web.json
    fi
}
