import time
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console
from art import *
import json
import keyword

data = {}
console = Console()

def checkInputErrors(input):
    keywords = keyword.kwlist
    input = str(input).strip()
    return True if (keywords.__contains__(input)) else False

def getAppName():
    while True:
        try:
            app_name = prompt("[green]Name your app [/green]", validator =lambda name: len(name) > 0)
            if checkInputErrors(app_name):
                console.print("[red]> Input cannot be pre-defined keywords!")
                continue
            else:
                console.print("[green]> Initializing [bold]"+app_name+".json[/bold] file...[/green]")
                console.print("")
                return app_name
                break
        except:
            console.print("[red]> Input cannot be empty!")

def getAppSecret():
    try:
        secret = prompt("Enter the secret key for hashing passwords", validator= lambda pr: len(pr) > 0)
    except: 
        console.print("[red]> Input cannot be empty!")
    return secret

def getApiPrefix():
    prefix = None
    if(confirm("[green]Any prefix for api-endpoints ?[/green]")):
        while True:
            try:
                prefix = prompt("[green]Enter prefix for api-endpoints ?[/green]", validator = lambda pr: len(pr) > 0)
                if(checkInputErrors(prefix)):
                    console.print("[red]> Input cannot be pre-defined keywords!")
                    continue
                else:
                    console.print("[green]> Adding prefix [bold] /"+prefix+" [/bold] to api-endpoints...[/green]")
                    console.print("")
                    break
            except:
                console.print("[red]> Error while adding prefix !!!")
                continue
    return prefix

def setupAppAuthentication():
    if(confirm("[green]Want to add authentication functionality to the api ?[/green]")):
        data['auth_config'] = {}
        data["auth_config"]["auth"] = True
        console.print("Adding auth functionality ...")
        tables = list(data['schema'].keys())
        console.print("[green]Select table of which variables will be used to verify credentials")
        auth_table = select(options=tables, cursor="👉")
        data["auth_config"]["table"] = auth_table
        console.print(auth_table+" table selected...")
        table_vars = list(data['schema'][auth_table].keys())
        console.print("[green]Select variable to be used for verifying email/username")
        auth_email = select(options=table_vars, cursor="👉")
        data['auth_config']["email_field"] = auth_email
        console.print(auth_email+" selected...")
        console.print("[green]Select variable to be used for verifying password")
        auth_pass = select(options=table_vars, cursor="👉")
        data["auth_config"]['pass_field'] = auth_pass
        console.print(auth_pass+" selected...")
        all_routes = ["GET", "POST", "PUT", "DELETE"]
        data["auth_config"]['auth_routes'] = {}
        for i in tables:
            data["auth_config"]['auth_routes'][i] = None
            console.print("[green]Select all ROUTES to secure for "+i+" table[/green]")
            selected_routes = select_multiple(options=all_routes, tick_character="✅")
            str_selected_routes = ""
            for val in selected_routes: str_selected_routes += val+", "
            str_selected_routes = str_selected_routes[: len(str_selected_routes)-2]
            data["auth_config"]['auth_routes'][i] = str_selected_routes
            console.print(str(selected_routes)+" selected...")
        data['secret'] = getAppSecret()

def setupAppSchema():
    console.print("> [green]Let's add [bold]Schema[/bold] info ...[/green]")
    console.print("")
    data['schema'] = {}
    add_more_table = False
    while(True):
        try:
            s_name = prompt("> [green]Enter table name ?[/green]", validator = lambda pr: len(pr) > 0)
            if (checkInputErrors(s_name)):
                console.print("[red]> Input cannot be pre-defined keywords!")
                continue
            data['schema'][s_name] = {}
            console.print("Added table "+s_name)
            add_more_var = False
            while(True):
                s_var = prompt("Add variable name (Enter) and select datatype")
                data['schema'][s_name][s_var] = "NULL"
                # console.print("Select datatype for variable")
                dataTypes = ["INT", "TEXT", "BOOLEAN", "BLOB"]
                s_var_type = select(options=dataTypes, cursor="👉")
                data['schema'][s_name][s_var] = s_var_type
                console.print(s_var+": "+s_var_type)
                add_more_var = confirm("Add another variable to schema "+s_name+" ?")
                if add_more_var:
                    continue
                else:
                    console.print("Adding variables to schema "+s_name+" ...")
                    break
            add_more_table = confirm("Want to add more tables to project ?")
            if add_more_table:
                continue
            else:
                break
        except:
            console.print("[red]> Input cannot be empty!")

def askQuestion():

    tprint("BadB", font="swampland")
    console.print("")
    console.print("[bold blue]Welcome to the BADB[/bold blue]")
    console.print("[bold blue]Create your Backend/API seamlessly[/bold blue]")
    console.print("")
    data['name'] = getAppName()
    data['secret'] = "my_secret"
    data['prefix'] = getApiPrefix()
    setupAppSchema()
    setupAppAuthentication()

    with open(data['name']+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    console.print("[green bold]Run following command to create api-endpoints :[/green bold] badb-create-app [cyan bold]"+data['name']+".json[/cyan bold]")


