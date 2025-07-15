// ════════════════════════════════════════════════════════════════════ XCORE ══
// Copyright (C) 2025, Xeniorn | x404bjrn
// Lizenziert - siehe LICENSE Datei für Details
// ─────────────────────────────────────────────────────────────────────────────
import java.io.FileWriter;
import java.io.IOException;

public class JavaFeedbackSystem {
    public static void feedback(String[] outputLines, String resultJson, String mode) {
        for (String line : outputLines) {
            System.out.println(line);
            String cleanLine = line.replaceAll("\u001B\\[[;\\d]*m", "");

            if (mode.equals("web")) {
                appendToFile("xcore_output_web.log", cleanLine);
            } else if (mode.equals("gui")) {
                appendToFile("xcore_output_gui.log", cleanLine);
            }
        }

        if (mode.equals("web") && resultJson != null && !resultJson.isEmpty()) {
            appendToFile("xcore_result_web.json", resultJson);
        }
    }

    private static void appendToFile(String path, String content) {
        try (FileWriter fw = new FileWriter(path, true)) {
            fw.write(content + "\n");
        } catch (IOException e) {
            System.err.println("Fehler beim Schreiben in " + path + ": " + e.getMessage());
        }
    }
}
