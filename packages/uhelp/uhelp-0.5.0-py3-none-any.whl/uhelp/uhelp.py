#!/usr/bin/env python
# -*- coding:utf-8 -*-
from datetime import datetime
# import configparser
from configupdater import ConfigUpdater
import argparse
import pathlib
from pathlib import Path
from tinydb import TinyDB, Query
import json
import pprint
from rich.console import Console
from rich.style import Style
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from rich.markdown import Markdown
# from rich.theme import Theme
from rich_theme_manager import Theme, ThemeManager
import tempfile, os
from subprocess import run
import re


# from rich import print_json
import logging


def main():
    """
    main function
    setup.cfg pyproject.toml pip want this. case in console software
    """
    # testing path inner pip package and open pettern
    """
    here = Path(__file__).parent
    fname = here / "uhelp.json"
    print(f"{here=}  {fname=}")
    with fname.open() as f:
        print(f"{f=}")
        print("success open uhelp.json!")
    """


    # Choosing a path when building a .deb or pip package
    # python(one directory) or deb(deb package style) or pip(module dir)
    pathtype = "pip"

    # for adjust pip or binary compile path
    if pathtype == "python":

        tldr_path = pathlib.Path("./pages/")
        dictionary_path = pathlib.Path("./uhelp.json")
        theme_path = pathlib.Path("./rich_theme_manager/themes")

        init_path = pathlib.Path("./uhelp.ini")
        sleep_path = pathlib.Path("./smemo.txt")
        currentdir_chk = pathlib.Path("./uhelp.py")

    elif pathtype == "deb":

        tldr_path = pathlib.Path("/opt/uhelp/pages/")
        dictionary_path = pathlib.Path("/opt/uhelp/uhelp.json")
        theme_path = pathlib.Path("/opt/uhelp/rich_theme_manager/themes")
        init_path = pathlib.Path("/opt/uhelp/uhelp.ini")
        sleep_path = pathlib.Path("/opt/uhelp/smemo.txt")

    elif pathtype == "pip":

        # testing path inner pip package 
        here = Path(__file__).parent
        tldr_path = here / "pages/"
        dictionary_path = here / "uhelp.json"
        theme_path = here / "rich_theme_manager/themes"
        init_path = here / "uhelp.ini"
        sleep_path = here / "smemo.txt"

    # Reject execution from outside the program directory
    # (because it creates uhelp.ini etc. in the current directory that is unrelated to the program, But I wonder why, it seems strange)
    if pathtype == "python" and currentdir_chk.exists() == False:
        print(f"{pathtype=} {currentdir_chk.exists()=}")
        print("Can only run from the program directory with uhelp.py")
        return  # how to finish main



    # rich console instance with theme
    #console = Console(theme=custom_theme)
    #console = Console()

    # logging setting
    logging.basicConfig(level=logging.DEBUG)

    logger_blocklist = [
        "markdown_it",
    ]

    for module in logger_blocklist:
        logging.getLogger(module).setLevel(logging.WARNING)

    #logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    logging.disable(logging.CRITICAL)



    resdict = ""


    # TODO:let themes one by one commonise

    # basic theme on built-in for test. planning is load thi  s from setuped theme directory
    THEMES = [
        Theme(
            name="terminal",
            description="my terminal mode theme",
            tags=["terminal"],
            styles={
                "title": "bold cyan on blue",
                "oldusage": "green",
                "usage": "#000000 on #FFFEF6",
                "strong": "bold red",
                "info": "dim cyan",
                "warning": "bold magenta",
                "danger": "bold red",
                "info2": Style(color="#22863a", bold=True),
                "foot": "#DDDCD3",
                "codez": "#000000 on #BFC5CA",
                "markdown.paragraph": Style(),
                "markdown.text": Style(),
                "markdown.em": Style(italic=True),
                "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
                "markdown.strong": Style(bold=True),
                "markdown.code": "#000000 on #BFC5CA",
                "markdown.code_block": Style(color="cyan", bgcolor="black"),
                "markdown.block_quote": Style(color="blue"),
                "markdown.list": Style(color="#395A5B"),
                "markdown.item": Style(),
                "markdown.item.bullet": Style(color="#23274F", bold=True),
                "markdown.item.number": Style(color="green", bold=True),
                "markdown.hr": Style(color="black"),
                "markdown.h1.border": Style(),
                "markdown.h1": Style(bold=True),
                "markdown.h2": Style(bold=True, underline=True),
                "markdown.h3": Style(bold=True),
                "markdown.h4": Style(bold=True, dim=True),
                "markdown.h5": Style(underline=True),
                "markdown.h6": Style(italic=True),
                "markdown.h7": Style(italic=True, dim=True),
                "markdown.link": Style(color="bright_blue"),
                "markdown.link_url": Style(color="blue", underline=True),
            },
        ),
        Theme(
            name="retroterminal",
            description="retro terminal mode theme",
            tags=["retroterminal"],
            styles={
                "title": "green",
                "usage": "green",
                "strong": "bold red",
                "info": "dim cyan",
                "warning": "bold magenta",
                "danger": "bold red",
                "info2": Style(color="#22863a", bold=True),
                "foot": "#DDDCD3",
                "codez": "#000000 on green",
                "markdown.paragraph": Style(),
                "markdown.text": Style(),
                "markdown.em": Style(italic=True),
                "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
                "markdown.strong": Style(bold=True),
                "markdown.code": "#000000 on green",
                "markdown.code_block": "#000000 on green",
                "markdown.block_quote": Style(color="green"),
                "markdown.list": Style(color="green"),
                "markdown.item": Style(),
                "markdown.item.bullet": Style(color="#A0FA20", bold=True),
                "markdown.item.number": Style(color="#A0FA20", bold=True),
                "markdown.hr": Style(color="green"),
                "markdown.h1.border": Style(),
                "markdown.h1": Style(bold=True),
                "markdown.h2": Style(bold=True, underline=True),
                "markdown.h3": Style(bold=True),
                "markdown.h4": Style(bold=True, dim=True),
                "markdown.h5": Style(underline=True),
                "markdown.h6": Style(italic=True),
                "markdown.h7": Style(italic=True, dim=True),
                "markdown.link": Style(color="bright_green"),
                "markdown.link_url": Style(color="green", underline=True),

            },
        ),
        Theme(
            name="retroterminal2",
            description="retro orange terminal",
            tags=["retroorangeterm"],
            styles={
                "title": "#FFD400",
                "usage": "#FFD400",
                "codez": "#000000 on #FFD400",
                "info": "#FFD400",
                "warning": "bold magenta",
                "danger": "bold red",
                "markdown.paragraph": Style(),
                "markdown.text": Style(),
                "markdown.em": Style(italic=True),
                "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
                "markdown.strong": Style(bold=True),
                "markdown.code": "#000000 on #FFD400",
                "markdown.code_block": Style(color="cyan", bgcolor="black"),
                "markdown.block_quote": Style(color="#FFD400"),
                "markdown.list": Style(color="cyan"),
                "markdown.item": Style(),
                "markdown.item.bullet": Style(color="#FFD400", bold=True),
                "markdown.item.number": Style(color="#FFD400", bold=True),
                "markdown.hr": Style(color="#FFD400"),
                "markdown.h1.border": Style(),
                "markdown.h1": Style(bold=True),
                "markdown.h2": Style(bold=True, underline=True),
                "markdown.h3": Style(bold=True),
                "markdown.h4": Style(bold=True, dim=True),
                "markdown.h5": Style(underline=True),
                "markdown.h6": Style(italic=True),
                "markdown.h7": Style(italic=True, dim=True),
                "markdown.link": Style(color="#FFD400"),
                "markdown.link_url": Style(color="#FFD400", underline=True),

            },
        ),
        Theme(
            name="fruits",
            description="fruits theme",
            tags=["fruits"],
            styles={
                "title": "bold #E25666",
                "oldusage": "blue",
                "usage": "bold #590B1A on #E95B6B",
                "strong": "bold blue",
                "info": "dim cyan",
                "warning": "bold magenta",
                "danger": "bold red",
                "info2": Style(color="#22863a", bold=True),
                "foot": "#DDDCD3",
                "codez": "#EEEEEE on #8C5FBC",
                "markdown.paragraph": Style(),
                "markdown.text": Style(),
                "markdown.em": Style(italic=True),
                "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
                "markdown.strong": Style(bold=True),
                "markdown.code": "#EEEEEE on #8C5FBC",
                "markdown.code_block": Style(color="cyan", bgcolor="black"),
                "markdown.block_quote": Style(color="blue"),
                "markdown.list": Style(color="#395A5B"),
                "markdown.item": Style(),
                "markdown.item.bullet": Style(color="#23274F", bold=True),
                "markdown.item.number": Style(color="green", bold=True),
                "markdown.hr": Style(color="black"),
                "markdown.h1.border": Style(),
                "markdown.h1": Style(bold=True),
                "markdown.h2": Style(bold=True, underline=True),
                "markdown.h3": Style(bold=True),
                "markdown.h4": Style(bold=True, dim=True),
                "markdown.h5": Style(underline=True),
                "markdown.h6": Style(italic=True),
                "markdown.h7": Style(italic=True, dim=True),
                "markdown.link": Style(color="bright_blue"),
                "markdown.link_url": Style(color="blue", underline=True),
            },
        ),
        Theme(
                name="simple",

            description="simple terminal",
            tags=["simpleterm"],
            styles={
                "title": "#F6DFFF",
                "usage": "#FFF4F4",
                "codez": "bold #F7DFEF underline",
                "info": "#FFD400",
                "warning": "bold magenta",
                "danger": "bold red",
                "markdown.paragraph": Style(color="#FFF6DC"),
                "markdown.text": Style(color="#659AD2"),
                "markdown.em": Style(italic=True),
                "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
                "markdown.strong": Style(bold=True, color="#AFB4DB"),
                "markdown.code": "#F7DFEF on #001F43",
                "markdown.code_block": Style(color="cyan", bgcolor="black"),
                "markdown.block_quote": Style(color="#8689C3"),
                "markdown.list": Style(color="cyan"),
                "markdown.item": Style(),
                "markdown.item.bullet": Style(color="#F0566E", bold=True),
                "markdown.item.number": Style(color="#F0566E", bold=True),
                "markdown.hr": Style(color="yellow"),
                "markdown.h1.border": Style(color="bright_blue"),
                "markdown.h1": Style(bold=True, color="cyan"),
                "markdown.h2": Style(bold=True, underline=True),
                "markdown.h3": Style(bold=True),
                "markdown.h4": Style(bold=True, dim=True),
                "markdown.h5": Style(underline=True),
                "markdown.h6": Style(italic=True),
                "markdown.h7": Style(italic=True, dim=True),
                "markdown.link": Style(color="bright_blue"),
                "markdown.link_url": Style(color="blue", underline=True),
            },
        ),
        Theme(
            name="mono",
            description="Monochromatic theme",
            tags=["mono", "colorblind"],
            styles={
                "info": "italic",
                "warning": "bold",
                "danger": "reverse bold",
                "markdown.paragraph": Style(),
                "markdown.text": Style(),
                "markdown.em": Style(italic=True),
                "markdown.emph": Style(italic=True),  # For commonmark backwards compatibility
                "markdown.strong": Style(bold=True),
                "markdown.code": "#000000 on #BFC5CA",
                "markdown.code_block": Style(color="cyan", bgcolor="black"),
                "markdown.block_quote": Style(color="magenta"),
                "markdown.list": Style(color="cyan"),
                "markdown.item": Style(),
                "markdown.item.bullet": Style(color="yellow", bold=True),
                "markdown.item.number": Style(color="yellow", bold=True),
                "markdown.hr": Style(color="yellow"),
                "markdown.h1.border": Style(),
                "markdown.h1": Style(bold=True),
                "markdown.h2": Style(bold=True, underline=True),
                "markdown.h3": Style(bold=True),
                "markdown.h4": Style(bold=True, dim=True),
                "markdown.h5": Style(underline=True),
                "markdown.h6": Style(italic=True),
                "markdown.h7": Style(italic=True, dim=True),
                "markdown.link": Style(color="bright_blue"),
                "markdown.link_url": Style(color="blue", underline=True),

            },
        ),
    ]

                #"title": "bold #FAE9E8 on #9F66EA",Referenced pypi software glosslip


    def get_args():
        psr = argparse.ArgumentParser(
            prog='uhelp',
            description='usage memo your own',
            epilog='more simple info you want? run `uhelp uhelp` :)')

        group = psr.add_mutually_exclusive_group()
        group.add_argument('-s', '--sleep', dest='smode', action='store_const', const='smemo', default='uhelp', help='sleep memo mode')
        # dest wrong below
        group.add_argument('-e', '--edit', dest='smode', action='store_const', const='edit', default='uhelp', help='edit user dictionary')
        group.add_argument('-r', '--remove', dest='smode', action='store_const', const='remove', default='uhelp', help='remove entry user dictionary')

        group.add_argument('-v', '--vstyle', dest='smode', action='store_const', const='vstyle', default='uhelp', help='this option change visual style')
        group.add_argument('-b', '--backupmenu', dest='smode', action='store_const', const='bkrs', default='uhelp', help='backup or restore or import your database table')
        group.add_argument('-t', '--tldr', dest='smode', action='store_const', const='tldr', default='uhelp', help='tldr cliant mode')


        psr.add_argument('targetstrings', metavar='CommandName_or_Strings', type=str, nargs='+',
                        help='required. normaly command name your serching. (and strings for sleep memo mode)')
    #    psr.add_argument('commandname', help='find this command info')
        group.add_argument('--version', action='version', version='%(prog)s 1.0')
        return psr.parse_args()


    def initfiles():
        """
        if not exist required init files then create
        """
        # uhelp.json load bas and usr template from init.py
        # uhelp.ini

        # uhelp.ini file exists

        #myi = pathlib.Path("./uhelp.ini")
        myi = init_path
        chkuini = myi.exists()
        logging.debug(f"{chkuini=}")
        
        # check exists section&value in uhelp.ini
        D_INI = ";this is init file\n;<--semicoron column is commentout\n\n;available default/retro/retro2/simple/fruits\n\n[outputform]\nmode = default\n\n;setting example uhelp or tldr,uhelp or tldr or uhelp,tldr\n\n[multioutput]\nprintitem = uhelp"

        if chkuini == False:
            logging.debug("uhelp.ini is no exists. writing default ini file")

            print("\nuhelp.ini no exists. making file from default template")
            # create from default template
            with open(init_path, "w+", encoding="utf-8") as f:
                f.write(D_INI)

        else:
            logging.debug("uhelp.ini is exists")

        return 0

    initfiles()



    # create database and tables
    db = TinyDB(dictionary_path)

    bas = db.table('basictable')
    usr = db.table('usertable')
    ext = db.table('extratable')

    # set to "usr" for default table then db.* access is meaning usertable
    db.default_table_name = "usertable"


    # For Program Authors. bas/usr/ext selecter
    # If you change this to bas, the edit function will work for the bas table
    target_table = usr
    logging.debug(f"{target_table=}")


    def switch_test():
        """
        switch target table test
        """
        qu = Query()
        print(f"table check 'uhelp' = {target_table.contains(qu.command == 'uhelp')}")
        return 0

    # switch_test()


    def readdefdb():
        """
        open json and read it to python dictionary
        dictionary to tinyDB table
        """

        with open('defdb.json') as f:
            df = json.load(f)

        pprint.pprint(df, width=40)
        return 0


    def dbzeroinit():
        """
        everytime reset database for test
        """
        global db
        global bas
        # database clear all
        db.truncate()  # cant truncate table?
        bas.truncate()  # clear database is need this
        # set default data
        # readdefdb() no available now
        return 0

    # db reset
    #dbzeroinit()


    def jload(repath):  # what is this function? may be not need
        with open(repath, 'r') as file:
            dict_data = json.load(file)
        # print(f"{dict_data[-1]=}")
        return dict_data

    def backupmenu(cmenu):

        def ubackup():  # TODO:beaupy can path complecation https://petereon.github.io/beaupy/examples/
            """
            backup user table to listfile json
            """

            # add date filename
            dt_now = datetime.now()
            dtname = dt_now.strftime('%y%m%d_%H%M%S')

            console.rule(f'[bold #A6BFC8]Backup Your Dictionay[/]', style='#A6BFC8')
            console.print("[yellow]Create backupfile in your home directory[/]")

            backupfilestr= ('~/'+'uhelpusr_'+dtname+'.json')
            backupfilepath = Path(backupfilestr).expanduser()
            cfmbk = Prompt.ask(f"backup to {backupfilepath}?", choices=["y", "n"])

            if cfmbk == "y":  # No matter how many hours later you press "y" The filename timestamp is as of the displayed above
                with open(backupfilepath, 'w') as f:

                    json.dump(usr.all(), f)

                console.print("[blue]user table backuped.[/blue]")

            else:
                pass

            return

        # ubackup()

        def urestore():  # I will try Back up just in case, and then try to truncate usr from uhelp.json and write it back. success
            """
            restore from backuped usertable or other users table file
            You can choose between two methods, Update and Upsert, as an update method.
            """
            console = Console()
            # TODO:need Check if the terminal can display 16-bit or more color
            # explain update(delete) , upsert
            console.rule(f'[bold #A6BFC8]Restore Your Dictionay[/]', style='#A6BFC8')

            console.print("There are roughly two ways to restore files\n\
            \n ways 1 simply restore backup_________________\
            \n uhelp.json[red]\[]\[][green]\[][/green]\[][green]\[]\[][/green]\[][/red] *usr table\
            \n yourbackup[blue]\[]\[]\[]\[]\[]\[]\[][/blue]\
            \n                 ↓ ↓ ↓\
            \n uhelp.json[blue]\[]\[]\[]\[]\[]\[]\[][/blue]\
            \n \
            \n  [dim][italic]The normal restore method.  user's dictionary part is the will be the same as the backup[/][/]\
            \n \
            \n ways 2 Partial update________________________\
            \n uhelp.json[red]\[]\[][green]\[][/green]\[][green]\[]\[][/green]\[][/red] *usr table\
            \n yourbackup[blue]\[]\[]\[]\[]\[]\[]\[][/blue]\
            \n                 ↓ ↓ ↓\
            \n uhelp.json[blue]\[]\[][green]\[][/green]\[][green]\[]\[][/green]\[][/blue]\
            \n \
            \n  [dim][italic]case If use other people's table data additional to own data[/][/]\
            \n              ")

            ynways = Prompt.ask("which restore ways choose? 1 = restore / 2 = partial", choices=["1", "2"])

            def askrestorepath():
                # pathlib expanduser() understund home ~/
                lbexists = False
                while not lbexists:
                    lbpath = Prompt.ask("Please specify the path of the file to be restored")
                    LBP = Path(lbpath).expanduser()
                    print(LBP)
                    logging.debug(f"{LBP.exists()=}, {LBP.is_file()=}, {LBP.suffix=}")
                    if LBP.exists() and LBP.is_file() and LBP.suffix=='.json':
                        lbexists = True
                        console.print(f"[blue]path is[/] [green]True[/]")
                    else:
                        pag = Prompt.ask(f"file not exists : {lbpath} \n enter again?", choices=["y", "n"])
                        if pag == "y":
                            pass
                        elif pag == "n":
                            lbexists = False
                            break
                return LBP, lbexists

            if ynways == "1":  # simple overwrite usr table

                # restore function
                logging.debug("restore function 1")

                CLBP = askrestorepath()

                if CLBP[1]:

                    # restore function
                    usr.truncate()
                    console.print(f"user table [yellow]truncated.[/] Number of registered items: {len(usr)}")

                    # belows I want to use update instead of upsert,
                    # but the difference is whether I truncate or not, so I'll go with this for now
                    rt = jload(CLBP[0])
                    for i in range(len(rt)):
                        cnm = rt[i]['command']
                        usr.insert(rt[i])
                        console.print(f"[green]{cnm}[/] is not exist. [blue]insert[/] ")

                    console.print(f"[blue]success restore usr table[/] {len(usr)=}")

                    console.print(f"[blue]restored usertable from {CLBP[0]} Number of registered items[/]: {len(usr)}")
                else:
                    console.print(f"[red]abort[/] restore function wrong path {len(usr)=}")

            elif ynways == "2":  # upsert usr table
                logging.debug("restore function 2")
                CLBP = askrestorepath()

                User = Query()
                rt = jload(CLBP[0])

                for i in range(len(rt)):
                    cnm = rt[i]['command']
                    if usr.contains(Query()['command']==rt[i]['command']):  # bool
                        console.print(f"[yellow]{cnm}[/] is exists. [red]skip[/]")
                    else:  # If the command name does not exist
                        # insert item
                        usr.insert(rt[i])
                        console.print(f"[green]{cnm}[/] is not exist. [blue]insert[/] ")

                console.print(f"\n[blue]success restore usr table ([red]upsert method[/])[/] {len(usr)=}")
                #print(usr.all())

            else:
                print(f"error Prompt.ask")

            return

        # backup or restore
        if cmenu == "backup":
            ubackup()
        elif cmenu == "restore":
            urestore()
        else:
            console.print(f"There is no option {cmenu}")

        return

    #jload()
    #urestore()  # upsert success


    def vstyle_change(chv):
        """
        change init file style value
        configparser is remove comment so here using configupdater 
        """

        console.rule(f'[bold #A6BFC8]Change Output Style[/] [#C7A252]<[/][#123456 on #C7A252]{chv}[/]', style='#A6BFC8')

        if chv == 'default' or chv == 'retro' or chv == 'retro2' or chv == 'simple' or chv == 'fruits':
                
            updater = ConfigUpdater()
            updater.read(init_path)

            logging.debug(f"{updater.has_section('outputform')}")
            if updater.has_section('outputform') == True:
                console.print("[dim]uhelp.ini has outputform section...[/dim]")

                with open(init_path, 'w') as f:
                    prechange = updater["outputform"]["mode"].value
                    updater["outputform"]["mode"].value = chv
                    updater.write(f)
                    if updater["outputform"]["mode"].value == chv:
                        console.print(f"[dim]changed init value {prechange} -> {chv}[/dim]")
                console.print(f"\n[blue]Successfully changed outputform value to [bold]{chv}[/bold][/blue]\n")

            else:
                print("ugelp.ini outputform section not exist")

        else:
            console.print(f"\n[warning]There is no style of [/warning][blue]`{chv}`[/]\n")


        return 0


    def editdata(edcmnd, edsrc=b"it is new blank data"):
        EDITOR = os.environ.get('EDITOR','vim')  # that easy!


        initial_message = b"# infomation how edit.  this comments are no need delete\n# you can decolate text like this. with used available them  e tag[info]hello[/info] world [warning]good morning  [/warning]\n# basicaly this app theme has [info][codez][warning][heavy][point]\n# [/]or[/info]  to close tag. when no c  lose tag then apply 1 line. if want bracket normally use [ ] please escape \\[something] like this\n# if already command registed. texts show below\n"  # if you want to set up the file somehow

        # comnentout when testing nano
        #EDITOR = 'nano'

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            tf.write(initial_message)
            tf.write(edsrc)
            tf.flush()

            def editopr():

                cmdvim = f"{EDITOR} +6 {tf.name}"  # "+n" cursor position for vi/vim. "+" = last
                cmdnano = f"{EDITOR} {tf.name}"  # nogood here if add --saveonexit ?

                if EDITOR == "vim" or "vi":

                    run(cmdvim, shell=True)  # cursol set last
                elif EDITOR == "nano":

                    run(cmdnano, tf.name)

                else:

                    run(EDITOR, tf.name)

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                edited_message = tf.read()
                prepost = edited_message.decode("utf-8")
                para = prepost.splitlines()  # split to list
                # I've decided on a comment part, and I've decided if it's actually 5 lines,
                # but I haven't used this at the moment.
                chk = 5  # example comment lines
                for i in range(chk):
                    logging.debug(re.match(r'^#', para[i].lstrip()))
                spara = "\n".join(para[5:])  # slice to remove example info
                try:
                    # print("example comment lines(5) deleted")
                    formsout(edcmnd, spara, 0)
                except:
                    console.rule(f'[bold #A6BFC8]Edit Dictionaly[/] [red]error[/]', style='#A6BFC8')

                    redit = Prompt.ask(f"\nsome error include your text. please fix. \nmaybe tag close miss and them matching/tag wrong name\nyes to back to edit no to abort editting", choices=["y", "n"])
                    if redit == "y":
                        logging.debug("---error redit---")
                        editopr()
                    else:
                        print("edit aborted")
                else:   


                    fedit = Prompt.ask(f"register it ?", choices=["y", "n"])
                    if fedit == "y":
                        logging.debug("---write function---")

                        target_table.upsert({'command':edcmnd, 'usage':spara}, Query().command==edcmnd)

                    else:
                        aged = Prompt.ask(f"BACK TO EDIT ? if abort(choose n) then edited data is lost", choices=["y", "n"])
                        if aged == 'y':
                            #print(tf.name)
                            editopr()
                        else:
                            pass
                return

            editopr()

        return

    def dupchk(skey):
        """
        already registerd or not register
        """
        qu = Query()

        return target_table.contains(qu.command == skey)


    def adduserdb(edcom):
        """
        usr table edit by text editor
        1 ask command name
        2 dupplicate check & if already aveilable load it
        3 edit
        4 show result and user accept 
        """
        console.rule(f'[bold #A6BFC8]Edit Dictionaly[/] [#C7A252]<[/][#123456 on #C7A252]{edcom}[/]', style='#A6BFC8')

        # print(f"editting {edcom}")

        if dupchk(edcom) == 0:
            ente = "this is no exists entry newdata."
            anou = "exists checked. its new dictionary"

        else:
            # read value from database using key 
            resdoc = target_table.get(Query()['command'] == edcom)
            ente = resdoc.get('usage')
            anou = f"already exists ` {edcom} `."

        whatcom = Prompt.ask(f"{anou} are you edit {edcom} ?", choices=["y", "n"])

        if whatcom == "y":
            entb = ente.encode('utf-8')
            # Error that nonetype cannot be encoded when Usage is empty or not exists
            # It was displayed when the command-only data was created by mistake.
            editdata(edcom, entb)

        else:
            print("okay.")

        return 0


    # TODO:Problems that appear to say `success deleted` even if you delete an item that doesn't exist
    def removeuserdb(rterg):

        rask = Prompt.ask(f"are you realy [red]`remove`[/red] registered {rterg} in user db?", choices=["y", "n"])

        if rask == "y":
            target_table.remove(Query().command == rterg)

            if dupchk(rterg) == False:
                print(f"succesfully {rterg} is removed your database")

        else:
            print(f"abort remove `{rterg}` function")

        return


    def formsout(arg1, arg2, arg3):
        """style output format and printout
        this function output load simple/box/table/color/theme etc  form styling
        if multiple list then them strip to oneline string here
        :param str arg1: command name or date time
        :param str arg2: usage or memo
        :param str arg3: 0 = usr hit / 1 = bas hit / 2 = non / 3= tldr
        """

        adoc = arg1
        bdoc = arg2
        whit = arg3

        def getforminit(argtt):

            updater = ConfigUpdater()
            updater.read(init_path)
            if updater.has_section('outputform') == True:
                logging.debug('section outputform found')
            else:
                logging.debug('section outputform is not found')

            formmode = updater['outputform'][argtt].value
            logging.debug(f'setting value is {formmode}')

            return formmode


        forms = getforminit('mode')  # read setting from ini file


        match forms:

            case 'retro':  # format using retro
                logging.debug("output format is retro")
                # want change theme
                retroterm = theme_manager.get("retroterminal")
                console = Console(theme=retroterm)


                # usr hit or bas hit?
                if whit == 0:

                    console.print(Panel.fit(bdoc, style='usage', title=adoc, title_align='left'))

                    console.print(f"\n your database - total:{len(usr)}", ".", justify="right", style='usage', highlight=False)
                elif whit == 1:

                    console.print(Panel.fit(bdoc, style='usage', title=adoc, title_align='left'))


                    console.print(f"\n \[basic dictionary] - total:{len(bas)}", ".", justify="right", style='usage', highlight=False)
                elif whit == 3:  # tldr mode
                    console.print(Panel.fit(bdoc, style='usage',   title=adoc, title_align='left'))
                    console.print(f"\n \[from tldr {resdict}]", ".", justify="right", style='usage', highlight=False)

                else:  # whit2 for sleepmemo
                    console.print(Panel.fit(bdoc, style='usage', title=adoc, title_align='left'))


            case 'retro2':  # format using retro style
                logging.debug("output format is retro2")
                # want theme change
                retroterm2 = theme_manager.get("retroterminal2")
                console = Console(theme=retroterm2)


                # usr hit or bas hit?
                if whit == 0:
                    console.print(Panel.fit(bdoc,  style='usage', title=adoc, title_align='left'))

                    console.print(f"\n your database - total:{len(usr)}", ".", justify="right", style='usage', highlight=False)
                elif whit == 1:
                    console.print(Panel.fit(bdoc, style='usage', title=adoc, title_align='left'))

                    console.print(f"\n \[basic dictionary] - total:{len(bas)}", ".", justify="right", style='usage', highlight=False)
                elif whit == 3:  # tldr mode
                    console.print(Panel.fit(bdoc, style='usage', title=adoc, title_align='left'))

                    console.print(f"\n \[from tldr {resdict}]", ".", justify="right", style='usage', highlight=False)

                else:  # whit2 for sleepmemo
                    console.print(Panel.fit(bdoc, style='usage', title=adoc, title_align='left'))



            case 'simple':
                logging.debug("output format is simple")

                dtheme = theme_manager.get("simple")
                console = Console(theme=dtheme)

                if whit == 0:  # this is wrong usage it print action here
                    #ddoc = console.print(f"your database - total:{len(usr)}", ".", justify="right", style='title', highlight=False)
                    ddoc = f"your database - total:{len(usr)}"


                elif whit == 1:
                    #ddoc = console.print(f"\n \[basic dictionary] - total:{len(bas)}", ".", justify="right", style='title', highlight=False)
                    ddoc = f"\[basic dictionary] - total:{len(bas)}"

                elif whit == 3:  # tldr mode
                    #ddoc = console.print(f"\n \[from tldr {resdict}]", ".", justify="right", style='title', highlight=False)
                    ddoc = f"\n \[from tldr {resdict}]"


                else:  # whit2 for sleepmemo
                    ddoc = ""  # It's not necessary, but if there is none, an error will occur

                table = Table(box=box.SIMPLE, expand=True, show_header=False)
                # Fake headers for colspan realization
                table.add_column(adoc, ':pen:', width=None, justify="left")

                table.add_column(ddoc, width=None, justify="rite")

                table.add_row(
                        adoc,
                        ddoc,
                        )


                table2 = Table(show_header=False)
                table2.add_column()

                table2.add_row(
                    bdoc,
                    )
                console.print(table)
                console.print(table2)

            case 'fruits':  # here not hardcort bas/usr this is good. because not confliction when irregular usage too
                logging.debug("output format is fruits")

                dtheme = theme_manager.get("fruits")
                console = Console(theme=dtheme)

                atext = Text(" "+adoc+" ")
                atext.stylize("title")

                table = Table(box=box.SIMPLE_HEAVY, style="#78C808")
                table.add_column(atext, ":pen:", style="usage", width=None)  # trouble this style Not decorating the expected place?. but good
                table.add_row(
                    bdoc,
                            )
                console.print(table)

                if whit == 0:
                    console.print(f"your database - total:{len(usr)}", ".", justify="right", style='foot', highlight=False)
                elif whit == 1:
                    console.print(f"\n \[basic dictionary] - total:{len(bas)}", ".", justify="right", style='foot', highlight=False)
                elif whit == 3:  # tldr mode
                    console.print(f"\n \[from tldr {resdict}]", ".", justify="right", style='foot', highlight=False)

                else:  # whit2 for sleepmemo
                    # no need footer
                    pass


            case 'default':  # here not hardcort bas/usr this is good and not confliction when irregular usage
                logging.debug("output format is default")

                dtheme = theme_manager.get("terminal")
                console = Console(theme=dtheme)


                table = Table(box=box.SIMPLE_HEAVY)
                table.add_column(adoc, ":pen:", style="usage", width=None)  # trouble
                table.add_row(
                    bdoc,
                            )
                console.print(table)

                if whit == 0:
                    console.print(f"your database - total:{len(usr)}", ".", justify="right", style='foot', highlight=False)
                elif whit == 1:
                    console.print(f"\n \[basic dictionary] - total:{len(bas)}", ".", justify="right", style='foot', highlight=False)
                elif whit == 3:  # tldr mode
                    console.print(f"\n \[from tldr {resdict}]", ".", justify="right", style='foot', highlight=False)

                else:  # whit2 for sleepmemo
                    #console.print(Panel(bdoc, style='usage',   title=adoc, title_align='left'))
                    pass

            case _:
                print("error! not match format style name in theme ini file")

        return 0


    # if __name__ == '__main__':

    args = get_args()

    # theme call
    #theme_dir = pathlib.Path("./rich_theme_manager/themes").expanduser()
    theme_dir = theme_path
    theme_dir.expanduser().mkdir(parents=True, exist_ok=True)

    theme_manager = ThemeManager(theme_dir=theme_dir, themes=THEMES)
    terminal = theme_manager.get("terminal")
    console = Console(theme=terminal)

    # main area theme test
    # console.print(f"[strong]strong style[/] [dim]in called[/] \'terminal theme\'section main")

    # application mode
    if args.smode == 'uhelp':


        logging.debug(f"{args.smode=}")
        logging.debug(f"{args.targetstrings=}")

        # Make Query object
        que = Query()


        if args.targetstrings[0] != 'showtheme':  # uhelp mode

            # TODO: want footerstyle [basic:nohit/15 user:hit/5 tldr:hit/5000 ]
            # and {} show selected item

            # create list from uhelp.ini
            updater = ConfigUpdater()
            updater.read(init_path)
            logging.debug(updater.has_section('multioutput'))
            if updater.has_section('multioutput') == True:
                logging.debug("uhelp.ini has multioutput section...")
                mpri = updater['multioutput']['printitem'].value
                mls = [x.strip() for x in mpri.split(',')]
                logging.debug(f"{mpri=} print item list {mls=}")


            #print(console.size)
            #console.print(console.width)

            # exist check db
            logging.debug(f"exist check '{args.targetstrings[0]}' in bas table: {bas.contains(que.command == args.targetstrings[0])}")
            logging.debug(f"exist check '{args.targetstrings[0]}' in usr table: {usr.contains(que.command == args.targetstrings[0])}")
           
            # all database exist check
            def dataexist():
                """ uhelpbasic,uhelpuser,tldr exist check"""

                def tldrexist():

                    tgname = args.targetstrings[0]+".md"
                    TGC = str(tldr_path)+"/common/"+tgname
                    TGL = str(tldr_path)+"/linux/"+tgname
                    TGA = str(tldr_path)+"/android/"+tgname
                    TG_CPATH = Path(TGC)
                    TG_LPATH = Path(TGL)
                    TG_APATH = Path(TGA)
                    rflag = False

                    if TG_CPATH.exists():
                        rflag = True
                    elif TG_LPATH.exists():
                        rflag = True
                    elif TG_APATH.exists():
                        rflag = True
                    else:
                        rflag = False

                    logging.debug(f"tldr exist : {rflag=}")

                    return rflag

                hitflag=[False, False, False]
                if usr.contains(que.command == args.targetstrings[0]) == True:
                    logging.debug("search hit in uhelp user dictionary. hitflag on")
                    hitflag[0]=True

                if bas.contains(que.command == args.targetstrings[0]) == True:
                    logging.debug("search hit in uhelp user dictionary. hitflag on")
                    hitflag[1]=True

                if tldrexist():
                    logging.debug("search hit in uhelp user dictionary. tldr dictionary. hitflag on")
                    hitflag[2]=tldrexist()  # True?bool?

                return hitflag

            dhitlist = dataexist()

            # read list and formout
            for item in mls:

                if item == 'uhelp' and dhitlist[0]==True:
                    resdoc = usr.get(Query()['command'] == args.targetstrings[0])
                    formsout(args.targetstrings[0], resdoc.get('usage'), 0)

                elif item == 'uhelp' and dhitlist[1]==True:
                    resdoc = bas.get(Query()['command'] == args.targetstrings[0])
                    formsout(args.targetstrings[0], resdoc.get('usage'), 1)

                if dhitlist[0]==False and dhitlist[1]==False and item=='uhelp':
                    console.print("- [#C22047]not found in uhelp's dictionary[/] -\n")

                if item == 'tldr' and dhitlist[2]==True:

                    tgname = args.targetstrings[0]+".md"
                    TGC = str(tldr_path)+"/common/"+tgname
                    TGL = str(tldr_path)+"/linux/"+tgname
                    TGO = str(tldr_path)+"/android/"+tgname
                    TG_CPATH = Path(TGC)
                    TG_LPATH = Path(TGL)
                    TG_APATH = Path(TGO)
                    rflag = False

                    if TG_CPATH.exists():
                        resdict = 'common'
                        # helpdocument from filename
                        with open(TG_CPATH, 'r') as f:
                            rmd = f.read()
                            md = Markdown(rmd)
                        #console.print(md)
                        formsout(args.targetstrings[0],md,3)

                    elif TG_LPATH.exists():
                        resdict = 'linux'
                        # helpdocument from filename
                        with open(TG_LPATH, 'r') as f:
                            rmd = f.read()
                            md = Markdown(rmd)
                        #console.print(md)
                        formsout(args.targetstrings[0],md,3)

                    elif TG_APATH.exists():
                        resdict = 'android'
                        # helpdocument from filename
                        with open(TG_APATH, 'r') as f:
                            rmd = f.read()
                            md = Markdown(rmd)
                        #console.print(md)
                        formsout(args.targetstrings[0],md,3)


                    else:
                        print("error in section tldr pathout")


        else:
            # showtheme. not dictionary (i want change to   subparser)

            try:  # try-except is not silent try! bad choice?
                themename = args.targetstrings[1]

                print('theme_manager.list_themes()')
                theme_manager.list_themes()
                print("\n")

                mytheme = theme_manager.get(themename)
                print('theme_manager.preview_theme(terminal)')
                theme_manager.preview_theme(mytheme)
                console = Console(theme=mytheme)
                print("\n")

                console.print("This is information", style="info")
                console.print("[warning]The pod bay doors are locked[/warning]")
                console.print("Something terrible happened!", style="danger")

            except IndexError:
                console.print("\n[warning]themename argument need![/]usage  [codez]uhelp showtheme themename[/]\n")
                theme_manager.list_themes(show_path=False)  # why not work?

            except ValueError:
                console.print("\n[warning]correct themename need![/]usage [codez]uhelp showtheme themename[/]\n")
                #ThemeManager().themes  # work here
                theme_manager.list_themes(show_path=False) 

    elif args.smode == 'edit':
        logging.debug("entering edit mode")
        adduserdb(args.targetstrings[0])

    elif args.smode == 'remove':
        logging.debug("entering remove mode")
        removeuserdb(args.targetstrings[0])

    elif args.smode == 'vstyle':
        logging.debug("entering vstyle mode")
        vstyle_change(args.targetstrings[0])
    elif args.smode == 'bkrs':
        logging.debug(f"entering menu odered is {args.targetstrings[0]}")
        backupmenu(args.targetstrings[0])

        """
    elif args.smode == 'init':
        logging.debug("entering application setting  interactive ini edit mode")
        ini_change(args.targetstrings[0])
        # Use the FormsOut function to display each setting example and then prompt.Ask
        """

    elif args.smode == 'tldr':
        # only seen the tldr-common directory here now, needs to be fixed(fixed?!)
        logging.debug("entering tldr mode")

        term = theme_manager.get("terminal")
        console = Console(theme=term)

        tgname = args.targetstrings[0]+".md"
        TGC = str(tldr_path)+"/common/"+tgname
        TGL = str(tldr_path)+"/linux/"+tgname
        TGA = str(tldr_path)+"/android/"+tgname
        TG_CPATH = Path(TGC)
        TG_LPATH = Path(TGL)
        TG_APATH = Path(TGA)
        rflag = False


        if TG_CPATH.exists():
            resdict = 'common'
            # helpdocument from filename
            with open(TG_CPATH, 'r') as f:
                rmd = f.read()
                md = Markdown(rmd)
            #console.print(md)
            formsout(args.targetstrings[0],md,3)

        elif TG_LPATH.exists():
            resdict = 'linux'
            # helpdocument from filename
            with open(TG_LPATH, 'r') as f:
                rmd = f.read()
                md = Markdown(rmd)
            #console.print(md)
            formsout(args.targetstrings[0],md,3)

        elif TG_APATH.exists():
            resdict = 'android'
            # helpdocument from filename
            with open(TG_APATH, 'r') as f:
                rmd = f.read()
                md = Markdown(rmd)
            #console.print(md)
            formsout(args.targetstrings[0],md,3)

        else:
            print(f"not exist {tgname} in target tldr directry")

    else:  # start sleep memo mode
        if args.smode == 'smemo':

            logging.debug(f"{args.smode=}")
            logging.debug(f"{args.targetstrings=}")

            console.rule(f'[bold #A6BFC8]Sleep🛌 Note[/] [#C7A252]<[/][#123456 on #C7A252]{str(datetime.today())[:-7]+" now"}[/]', style='#A6BFC8')

            predoc = " ".join(args.targetstrings)
            console.print(f"note : {predoc}")

            noterw = Prompt.ask("\nwrite note? (y/n) no to view notes", choices=["y", "n"])

            logging.debug(f"{noterw=}")

            if noterw == "y":
                # datetime is list, list can't render. reason no space output table. so changed
                daytime = str(datetime.today())[:-7]
                memdoc = " ".join(args.targetstrings)
                formsout(daytime, memdoc, 2)

                logging.debug("sleep memo args list combinate for one")

                # sleep note is registory  max10. keep 10 column and delete 1st line

                #mys = pathlib.Path("smemo.txt")
                mys = sleep_path
                mys.touch(exist_ok=True)  # if no file make file

                # num_lines = sum(1 for line in open('smemo.txt'))
                # this oneliner no need file close? idk so i used in below way

                with open(sleep_path) as myfile:
                    num_lines = sum(1 for line in myfile)  # count lines in file

                logging.debug(f"count of Note is now {num_lines}")
                if num_lines > 9:
                    # cut first line(most old note) and save
                    with open(sleep_path, "r", encoding="utf_8") as o:
                        notefit = o.readlines()
                        logging.debug(f"{notefit=}")


                    with open(sleep_path, "w", encoding="utf_8") as o:
                        o.writelines(notefit[1:])

                # list combine and write
                with open(sleep_path, "a", encoding="utf_8") as o:
                    logging.debug(f"{type(memdoc)=}{len(memdoc)=}")
                    # A rare way to use Print
                    # * is a list expansion, file=None to standard output, file=o exported to a file
                    print(daytime, "=", memdoc, sep="", end="\n", file=o)  # ! advanced print function. it output to file


            else:  # show notes

                with open(sleep_path, encoding="utf-8", mode="r") as f:

                    lines = f.readlines()

                logging.debug(f"{lines=}")

                # let formout
                for i in range(len(lines)):
                    if i < len(lines)-1:
                        # print(f"{i=} {len(lines)=}")
                        #print(lines[i][:19], "\n", lines[i][20:])
                        formsout(lines[i][:19], lines[i][20:].rstrip(), 2)
                    else:
                        # print("mark latest function")
                        dt1 = datetime.strptime(lines[i][:19], '%Y-%m-%d %H:%M:%S')
                        dt2 = datetime.now()
                        td = dt2 - dt1
                        # print(td)
                        atime = str(td)[:1]
                        if int(atime) >= 999:
                            atime = "999+"
                        console.rule(f'[bold #A6BFC8]Latest Note[/] [#C7A252]<[/][#123456 on #C7A252] {atime} hours ago[/]', style='#A6BFC8')  # single theme ...
                        formsout(lines[i][:19], lines[i][20:].rstrip(), 2)


if __name__ == '__main__':
    main()
    #logging.debug("__main__ running")


