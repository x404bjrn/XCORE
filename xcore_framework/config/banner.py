# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from .formatting import formatter
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

setpoint_cli_banner = r"""
╔════════════════════════════════════════╗
║  {LGN}XCORE{X} {LBE}SETPOINT{X} - {BE}CLI{X} ({LYW}Konfiguration{X})  ║
╚════════════════════════════════════════╝"""

cli_modullist_header_banner = r"""
╔═══════════════════════════════════════════════════════════
║ {LGN}X C O R E{X}   M O D U L E S   L I S T
╠═══════════════════════════════════════════════════════════"""

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

cli_module_info_banner = r"""
╔═══════════════════════════════════════════════════════════
║ {header}
╠═══════════════════════════════════════════════════════════
║ {LYW}{mod_name}{X}
║ {mod_desc}
║ {mod_author}
║ {mod_version}
║ {mod_created}
╚═══════════════════════════════════════════════════════════
"""

cli_module_options_banner = r"""╔═══════════════════════════════════════════════════════════
║🧾 Option: {option_label}
╚┳──────────────────────────────────────────────────────────
 ├─ {option_required}
 ├─ {option_default}
 ├─ {option_current}
 └─ {option_desc}
"""


def show_banner(banner="xcore_banner", **kwargs):
    """
    Zeigt ein Banner basierend auf dem gegebenen Parameter an.
    """
    # Formatieren der Versionsanzeige
    version = ((9 - (len(__version__) + 1)) * ' ') + 'v' + __version__

    if banner == "cli_banner":
        # Banner des CLI-/ Konsolen-Modus
        print(cli_banner.format(version=version, **formatter))

    elif banner == "cli_modullist_header_banner":
        # Modullisten Header des CLI-Modus
        print(cli_modullist_header_banner.format(**formatter))

    elif banner == "cli_module_info_banner":
        # Modulinformationen Banner des CLI-Modus
        print(cli_module_info_banner.format(
            header=i18n.t("header.module_info"),
            mod_name=i18n.t("info.name", name=kwargs.get("name", "")),
            mod_desc=i18n.t("info.description", desc=kwargs.get("desc", "")),
            mod_author=i18n.t("info.author", author=kwargs.get("author", "")),
            mod_version=i18n.t("info.version", version=kwargs.get("version", "")),
            mod_created=i18n.t("info.created", created=kwargs.get("created", "")),
            **formatter)
        )

    elif banner == "cli_module_options_banner":
        # Moduloptionen Banner des CLI-Modus
        print(cli_module_options_banner.format(
            option_label=i18n.t("options.label", name=kwargs.get("label", "")),
            option_required=i18n.t("options.required", required=kwargs.get("required", "")),
            option_default=i18n.t("options.default", default=kwargs.get("default", "")),
            option_current=i18n.t("options.current", current=kwargs.get("current", ""),
                                  space=kwargs.get("space", "")),
            option_desc=i18n.t("options.description", desc=kwargs.get("desc", "")),
            **formatter)
        )

    elif banner == "setpoint_cli_banner":
        # Banner des Setpoint-Modus mit CLI Interface
        print(setpoint_cli_banner.format(**formatter))

    elif banner == "xcore_banner":
        # Default XCORE Banner
        print(xcore_banner.format(dialog=i18n.t("main.banner_dialog"),
                                  version=version,
                                  **formatter))
