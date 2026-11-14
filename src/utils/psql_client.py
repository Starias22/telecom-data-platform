import subprocess

class PsqlClient:
    def __init__(self, user, host , db=None,env=None,variable_assignment:str=None):
        command = [
                "psql",
                "-U", user,
                "-h", host,
                "-d", db if db is not None else user,
                "-v", "ON_ERROR_STOP=1"
                        ]
        command.extend(
                 [] if variable_assignment is None else ["-v", variable_assignment] 
            )
        
        self.command =command 
        self.env = env

    def execute(self, input, is_sql_file=False):
        try:
            result = subprocess.run(
                 self.command if not is_sql_file else self.command+ ["-f", input],
                        input=input if not is_sql_file else None,
                        env=self.env,
                        capture_output=True,
                        text=True,
                        check=True
                        )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr) from e

        return result.stdout
  
if __name__ == "__main__":
    pass
