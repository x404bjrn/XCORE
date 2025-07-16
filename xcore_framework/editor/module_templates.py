# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# INFO: Eine Sammlung von Moduleditor Templates der verschiedenen
#  Programmiersprachen. Diese können hier ganz einfach und flexibel erweiter
#  werden.


SECTION_TEMPLATES = {
    "python": """def run(params, state):
    
    # Modul-Arbeitsverzeichnis abrufen
    workdir = params['_working_dir']
    
    output = ["Python section started in " + workdir]

    # Gruß hinzufügen zum State
    state['greeting'] = "Hey!"
    
    # Printausgaben
    print([state['greeting']])
    print(output, state)
    
    # State zurückschreiben
    return state
""",

    "bash": """#!/bin/bash

PARAM_FILE="$1"
STATE_FILE="$2"

WORKDIR=$(jq -r '._working_dir' "$PARAM_FILE")
echo "Bash section started in $WORKDIR"

# Aktuellen State laden
STATE=$(cat "$STATE_FILE")

# Gruß hinzufügen
STATE=$(echo "$STATE" | jq '.greeting = "Hey!"')

# Ausgabe der Begrüßung
echo "[\"$(echo "$STATE" | jq -r '.greeting')\"]"

# Neue Ausgabe + State anzeigen
echo "$STATE"

# State zurückschreiben
echo "$STATE" > "$STATE_FILE"
""",

    "powershell": """param (
    [string]$paramFile,
    [string]$stateFile
)

$params = Get-Content $paramFile | ConvertFrom-Json
$state = Get-Content $stateFile | ConvertFrom-Json

$workdir = $params._working_dir
Write-Host "PowerShell section started in $workdir"

# Gruß setzen
$state.greeting = "Hey!"

# Ausgabe der Begrüßung
Write-Host "[$($state.greeting)]"

# State anzeigen
$state | ConvertTo-Json -Depth 10 | Write-Host

# Zurückschreiben
$state | ConvertTo-Json -Depth 10 | Set-Content $stateFile
""",

    "java": """import java.io.*;
import java.nio.file.*;
import org.json.*;

public class Main {
    public static void main(String[] args) throws Exception {
        JSONObject params = new JSONObject(Files.readString(Path.of(args[0])));
        JSONObject state = new JSONObject(Files.readString(Path.of(args[1])));

        String workdir = params.getString("_working_dir");
        System.out.println("Java section started in " + workdir);

        state.put("greeting", "Hey!");

        System.out.println("[\"" + state.getString("greeting") + "\"]");

        System.out.println(state.toString(2));

        Files.writeString(Path.of(args[1]), state.toString(2));
    }
}
""",

    "node": """const fs = require("fs");

// Argumente: [0]=node, [1]=scriptname, [2]=params, [3]=state
const [,, paramPath, statePath] = process.argv;

const params = JSON.parse(fs.readFileSync(paramPath, "utf8"));
const state = JSON.parse(fs.readFileSync(statePath, "utf8"));

const workdir = params._working_dir;
console.log("Node.js section started in " + workdir);

state.greeting = "Hey!";

console.log([state.greeting]);
console.log(JSON.stringify(state, null, 2));

fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
"""
}
