import os
from rich.console import Console
import tomli

console = Console()

cli_root_path = os.path.dirname(__file__)

def print_logo()-> None:
    ascii_art = """
    =====================================================================================
      :::    ::: ::::::::: ::::::::::: :::                         :::     ::::::::::: 
     :+:    :+: :+:    :+:    :+:     :+:                       :+: :+:       :+:      
    +:+    +:+ +:+    +:+    +:+     +:+                      +:+   +:+      +:+       
   +#++:++#++ +#++:++#+     +#+     +#+       /#++:++#++:+/ +#++:++#++:     +#+        
  +#+    +#+ +#+    +#+    +#+     +#+                     +#+     +#+     +#+         
 #+#    #+# #+#    #+#    #+#     #+#                     #+#     #+#     #+#          
###    ### #########     ###     ##########              ###     ### ###########   
=====================================================================================         
"""
    # Display ASCII art
    console.print(ascii_art.strip())

def get_integration_version() -> str:
    try:
        with open("./pyproject.toml", "rb") as toml_file:
            pyproject_data = tomli.load(toml_file)
            return pyproject_data["tool"]["poetry"]["version"]
    except (FileNotFoundError, KeyError):
        return ""