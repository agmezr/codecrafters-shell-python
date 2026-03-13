import subprocess

def get_commands(cmd):
    cmd = cmd.split("|")
    return cmd

def run_pipe_command(cmd):
    commands = get_commands(cmd)
    _input = None

    for command in commands:
        r = subprocess.run(
            ["./your_program.sh", "-c", f"{command}"],
            stdout=subprocess.PIPE,
            text=True,
            input=_input
        )
        _input = r.stdout
    
    return r