# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
from xcore_framework.config.formatting import formatter

# Erster Banner Entwurf (Start CLI)
def cli_welcome_banner():
    banner = r"""


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
    print(banner.format(**formatter))
