# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from .formatting import formatter, strip_ansi
from .i18n import i18n

from xcore_framework import __version__


cli_banner = r"""


{LGN}        ███████         ███████               {X}
{LGN}      ███████████    ████████████             {X}
{LGN}    ████      ████  ████       ███            {X}
{LGN}   ███          ██████          ███           {X}
{LGN}  ███            ████    {LMA}  █     {LGN}███          {X}
{LGN}  ███             ██     {LMA} █{MA}█{LMA}█    {LGN} ███         {X}
{LGN}  ███                    {LMA}█{MA}███{LMA}█   {LGN} ███         {X}
{LGN}  ███       {LMA}      █     ██{MA}█ █{LMA}██  {LGN} ███         {X}
{LGN}  ███       {LMA}     ███   ██{MA}█   █{LMA}██              {X}
{LGN}  ████      {LMA}    █████ █{MA}██     ██{LMA}██████████████████{X}
{LGN}   ████     {LMA}██████ ███{MA}██       ███████████████████████{X}
{LGN}    ████            ███ {X}╔═════════════════════════════════════════════╗
{LGN}     █████              {X}║  {LGN}██╗  ██╗{GN} ██████╗ ██████╗ ██████╗ ███████╗{X}  ║
{LGN}       ████             {X}║  {LGN}╚██╗██╔╝{GN}██╔════╝██╔═══██╗██╔══██╗██╔════╝{X}  ║
{LGN}         ████           {X}║  {LGN} ╚███╔╝ {GN}██║     ██║   ██║██████╔╝█████╗  {X}  ║
{LGN}           ████         {X}║  {LGN} ██╔██╗ {GN}██║     ██║   ██║██╔══██╗██╔══╝  {X}  ║
{LGN}             ████      █{X}║  {LGN}██╔╝ ██╗{GN}╚██████╗╚██████╔╝██║  ██║███████╗{X}  ║
{LGN}               ████  ███{X}║  {LGN}╚═╝  ╚═╝{GN} ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝{X}  ║
{LGN}                 ██████ {X}║               powered by {LMA}Xeniorn{X} | {MA}x404bjrn{X} ║
{LGN}                   ██   {X}║                                   {LYW}{version}{X} ║
                        ╚═════════════════════════════════════════════╝
"""

xcore_banner = r"""
╔═════════════════════════════════════════════╗
║  {LGN}██╗  ██╗{GN} ██████╗ ██████╗ ██████╗ ███████╗{X}  ║
║  {LGN}╚██╗██╔╝{GN}██╔════╝██╔═══██╗██╔══██╗██╔════╝{X}  ║
║  {LGN} ╚███╔╝ {GN}██║     ██║   ██║██████╔╝█████╗  {X}  ║
║  {LGN} ██╔██╗ {GN}██║     ██║   ██║██╔══██╗██╔══╝  {X}  ║
║  {LGN}██╔╝ ██╗{GN}╚██████╗╚██████╔╝██║  ██║███████╗{X}  ║
║  {LGN}╚═╝  ╚═╝{GN} ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝{X}  ║
║               powered by {LMA}Xeniorn{X} | {MA}x404bjrn{X} ║
║                                   {LYW}{version}{X} ║
╚═════════════════════════════════════════════╝

{dialog}
"""

default_banner = r"""
╔══════════════════════════════════════════════════════════╗
║ {color}{header}{X} ║
╚══════════════════════════════════════════════════════════╝"""

cli_module_info_banner = r"""
╔══════════════════════════════════════════════════════════╗
║ {LBE}{header}{X} ║
╠══════════════════════════════════════════════════════════╣
║ {mod_name} ║
║ {mod_desc} ║
║ {mod_author} ║
║ {mod_version} ║
║ {mod_created} ║
╚══════════════════════════════════════════════════════════╝
"""

cli_module_options_banner = r"""╔══════════════════════════════════════════════════════════╗
║ {option_label} ║
╚┳─────────────────────────────────────────────────────────┘
 ├─ {option_required}
 ├─ {option_default}
 ├─ {option_current}
 └─ {option_desc}
"""


def fit_text_to_frame(text, frame_chars=56):
    """
    Passt den gegebenen Text an den Rahmen an, indem Leerzeichen hinzugefügt werden,
    um sicherzustellen, dass die resultierende Breite des Textes dem gewünschten Rahmen
    entspricht. Falls ANSI-Farbcodes im Text enthalten sind, werden sie berücksichtigt
    und bei der Längenberechnung ignoriert.

    Args:
        text (str): Der Text, der an den Rahmen angepasst werden soll. Kann ANSI-Farbcodes
                    enthalten, welche nicht bei der Längenzählung berücksichtigt werden.
        frame_chars (int, optional): Die gewünschte Breite des Rahmens. Standard ist 56.

    Returns:
        str: Der angepasste Text, dessen Länge der gewünschten Breite entspricht.
    """
    new_text = text + (frame_chars - len(strip_ansi(text))) * " "
    return str(new_text)


def show_basic_banner(text, chars=56, color=formatter["BE"]):
    """
    Zeigt ein Basis-Banner im Terminal an.

    Die Funktion erstellt ein Banner mit einem Titeltext, der an eine bestimmte
    Zeichenbreite angepasst wird, und wendet eine definierte Farbformatierung
    an.

    Args:
        text (str): Der Text, der im Banner angezeigt wird.
        chars (int, optional): Die maximale Zeichenbreite für das Banner.
                               Standardmäßig auf 56 gesetzt.
        color (str, optional): Die Farbformatierung für den Bannertext.
                               Standardmäßig wird der Wert aus formatter["BE"]
                               verwendet.
    """
    print(
        default_banner.format(
            header=fit_text_to_frame(text, chars), color=color, **formatter
        )
    )


def show_banner(banner="xcore_banner", **kwargs):
    """
    Zeigt ein Banner basierend auf dem gegebenen Parameter an.
    """
    # Formatieren der Versionsanzeige
    version = ((9 - (len(__version__) + 1)) * " ") + "v" + __version__

    if banner == "cli_banner":
        # Banner des CLI-/ Konsolen-Modus
        print(cli_banner.format(version=version, **formatter))

    elif banner == "cli_module_info_banner":
        # Modulinformationen Banner des CLI-Modus
        print(
            cli_module_info_banner.format(
                header=fit_text_to_frame(i18n.t("header.module_info")),
                mod_name=fit_text_to_frame(
                    i18n.t("info.name", name=kwargs.get("name", ""))
                ),
                mod_desc=(
                    fit_text_to_frame(
                        i18n.t("info.description", desc=kwargs.get("desc", ""))[:52]
                        + "..."
                    )
                ),
                mod_author=fit_text_to_frame(
                    i18n.t("info.author", author=kwargs.get("author", ""))
                ),
                mod_version=fit_text_to_frame(
                    i18n.t("info.version", version=kwargs.get("version", ""))
                ),
                mod_created=fit_text_to_frame(
                    i18n.t("info.created", created=kwargs.get("created", ""))
                ),
                **formatter,
            )
        )

    elif banner == "cli_module_options_banner":
        # Moduloptionen Banner des CLI-Modus
        print(
            cli_module_options_banner.format(
                option_label=fit_text_to_frame(
                    i18n.t("options.label", name=kwargs.get("label", ""))
                ),
                option_required=i18n.t(
                    "options.required", required=kwargs.get("required", "")
                ),
                option_default=i18n.t(
                    "options.default", default=kwargs.get("default", "")
                ),
                option_current=i18n.t(
                    "options.current",
                    current=kwargs.get("current", ""),
                    space=kwargs.get("space", ""),
                ),
                option_desc=i18n.t("options.desc", desc=kwargs.get("desc", "")),
                **formatter,
            )
        )

    elif banner == "xcore_banner":
        # XCORE Banner
        print(
            xcore_banner.format(
                dialog=i18n.t("main.banner_dialog"), version=version, **formatter
            )
        )
