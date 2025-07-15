# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# INFO: Eine Sammlung von Modul (Code) Templates der verschiedenen
#  Programmiersprachen. Diese können hier ganz einfach und flexibel erweiter
#  werden.


SECTION_TEMPLATES = {
    "python": """from xcore_framework.runtime.feedback.python_feedback import XmodResultFeedbackSystem

def run(params, state):
    fb = XmodResultFeedbackSystem()
    fb.mode = params.get("_mode", "cli")

    workdir = params['_working_dir']
    output = ["Python section started in " + workdir]

    state['greeting'] = "Hey!"

    fb.feedback(output, state)
    return state""",

    "bash": """#!/bin/bash
source ./xcore_framework/runtime/feedback/bash_feedback.sh

params_file=\"$1\"
state_file=\"$2\"

params=$(<\"$params_file\")
state=$(<\"$state_file\")

workdir=$(echo \"$params\" | jq -r '._working_dir')
output=(\"Bash section started in $workdir\")

state_json='{"greeting":"Hey!"}'

feedback output[@] \"$state_json\" \"cli\"""",

    "powershell": """. .\\xcore_framework\\runtime\\feedback\\ps_feedback.ps1

$params = Get-Content $args[0] | ConvertFrom-Json
$state = Get-Content $args[1] | ConvertFrom-Json

$workdir = $params._working_dir
$output = @("PowerShell section started in $workdir")

$state.greeting = "Hey!"

$fb = New-Object XmodResultFeedbackSystem
$fb.mode = $params._mode
$fb.feedback($output, $state)""",

    "java": """import java.io.*;
import java.nio.file.*;
import org.json.*;
import xcore_framework.runtime.feedback.JavaFeedback;

public class Main {
    public static void main(String[] args) throws Exception {
        JSONObject params = new JSONObject(Files.readString(Path.of(args[0])));
        JSONObject state  = new JSONObject(Files.readString(Path.of(args[1])));

        String workdir = params.getString("_working_dir");
        String[] output = {"Java section started in " + workdir};

        JavaFeedback fb = new JavaFeedback();
        fb.mode = "cli";
        fb.feedback(output, "{\'greeting\': \'Hey!\'}");
    }
}""",

    "node": """import { XmodResultFeedbackSystem } from \"./xcore_framework/runtime/feedback/node_feedback.js\";

const fb = new XmodResultFeedbackSystem();
fb.mode = process.env._MODE || \"cli\";

const fs = require("fs");
const [,, paramPath, statePath] = process.argv;

const params = JSON.parse(fs.readFileSync(paramPath, "utf8"));
const state = JSON.parse(fs.readFileSync(statePath, "utf8"));

const output = ["Node section started in " + params._working_dir];
state.greeting = "Hey!";

fb.feedback(output, state);"""
}
