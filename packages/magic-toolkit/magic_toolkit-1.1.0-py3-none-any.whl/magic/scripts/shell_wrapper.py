import subprocess
import os
from .check_cc_code_style import run_cpplint

scripts_root = os.path.dirname(__file__)

def shell(cmd, capture_output=False):
    ret = subprocess.run(cmd, shell=True, capture_output=capture_output)
    if capture_output:
        return ret.returncode, ret.stdout.decode('utf-8'), ret.stderr.decode('utf-8')
    else:
        return ret.returncode

def entry_force_kill(args):
    script_file = os.path.join(scripts_root, 'force_kill.sh')
    shell('bash {} {}'.format(script_file, args.keyword))

def entry_run_cpplint(args):
    run_cpplint(args.paths, args.linelength)

def config_parser(sub_parsers):
    # force_kill
    force_kill_p = sub_parsers.add_parser("kill", help="force to kill all pids matched by keyword")
    force_kill_p.add_argument("keyword", help='keyword for match program')
    force_kill_p.set_defaults(func=entry_force_kill)
    # cpplint
    cpplint_p = sub_parsers.add_parser('cpplint', help='cpplint for checking code stype')
    cpplint_p.add_argument('paths', nargs='+', help='folders/filenames')
    cpplint_p.add_argument('--linelength', type=int, default=120, help='allowed line length for the project')
    cpplint_p.set_defaults(func=entry_run_cpplint)
