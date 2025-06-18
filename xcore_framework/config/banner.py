# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from .formatting import formatter
from .i18n import i18n

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
{LGN}                 ██████ {X}║              powered by {LMA}Xeniorn{X} | {MA}x404bjrn{X}  ║
{LGN}                   ██   {X}╚═════════════════════════════════════════════╝
"""

setpoint_cli_banner = r"""
╔════════════════════════════════════════╗
║  {LGN}XCORE{X} {LBE}SETPOINT{X} - {BE}CLI{X} ({LYW}Konfiguration{X})  ║
╚════════════════════════════════════════╝"""

xcore_banner = r"""
╔═════════════════════════════════════════════╗
║  {LGN}██╗  ██╗{GN} ██████╗ ██████╗ ██████╗ ███████╗{X}  ║
║  {LGN}╚██╗██╔╝{GN}██╔════╝██╔═══██╗██╔══██╗██╔════╝{X}  ║
║  {LGN} ╚███╔╝ {GN}██║     ██║   ██║██████╔╝█████╗  {X}  ║
║  {LGN} ██╔██╗ {GN}██║     ██║   ██║██╔══██╗██╔══╝  {X}  ║
║  {LGN}██╔╝ ██╗{GN}╚██████╗╚██████╔╝██║  ██║███████╗{X}  ║
║  {LGN}╚═╝  ╚═╝{GN} ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝{X}  ║
║              powered by {LMA}Xeniorn{X} | {MA}x404bjrn{X}  ║
╚═════════════════════════════════════════════╝

{dialog}
"""


def show_banner(banner="cli_banner"):
    if banner == "cli_banner":
        print(cli_banner.format(**formatter))
    elif banner == "setpoint_cli_banner":
        print(setpoint_cli_banner.format(**formatter))
    elif banner == "xcore_banner":
        print(xcore_banner.format(dialog=i18n.t("main.banner_dialog"), **formatter))
