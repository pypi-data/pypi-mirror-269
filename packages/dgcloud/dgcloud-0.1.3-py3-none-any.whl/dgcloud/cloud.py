import paramiko


class ServerManager:
    def __init__(self, server_ip, ssh_user, ssh_password):
        self.server_ip = server_ip
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.ssh_connect_start()

    def ssh_connect_start(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh.connect(
            self.server_ip,
            port=22,
            username=self.ssh_user,
            password=self.ssh_password,
        )

    def ssh_connect_close(self):
        self.ssh.close()

    def ssh_execute_command(self, command, port=22):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout = stdout.read().decode().strip()
        stderr = stderr.read().decode().strip()
        return stdout, stderr

    def check_git_access(self):
        out, error = self.ssh_execute_command("ssh -T git@github.com")
        if "denied" in error:
            # print(f"Git access denied for user {self.ssh_user}")
            return False
        return True

    def git_pull(self, git_repo_path):
        if self.check_git_access():
            # print(self.git_changes(git_repo_path))
            STATUS, COMMANDS = self.git_changes(git_repo_path)
            command = f"cd {git_repo_path} && git pull"
            # print(command)
            out, error = self.ssh_execute_command(command)
            # print(out,error)
            if STATUS:
                for command in COMMANDS:
                    out, error = self.ssh_execute_command(command)
                    # print("commands executin : ",out,error)
                    if error:
                        # print(f"Error running command: {command}")
                        return None
            return out
        return "Access Denied"

    def git_application_status(self, service):
        service = f"echo '{self.ssh_password}' |  sudo -S systemctl status {service} | grep 'Active' "
        service_status_data, service_stderr = self.ssh_execute_command(service)
        service_status = (
            service_status_data.strip().split("since")[0].split("Active: ")[-1]
        )
        return service_status

    def restart_application(self, socket, service):
        # service = f"echo '{self.ssh_password}' |  sudo -S systemctl status {service} | grep 'Active' "
        # command = f"echo '{self.ssh_password}' | sudo -S sh -c 'systemctl restart ewpreportsdev.socket && systemctl restart ewpreportsdev.service'"
        # command = f"echo '{self.ssh_password}' | sudo -S systemctl restart {socket} && echo '{self.ssh_password}' | sudo -S systemctl restart {service}"
        command = f"sudo systemctl restart {socket} && sudo systemctl restart {service}"
        # print(command)
        out, error = self.ssh_execute_command(command)
        # print(out,error)
        return out,error

    def git_branch_check(self,git_repo_path,git_branch):
        command = f"cd {git_repo_path} && git branch --show-current"
        out,error = self.ssh_execute_command(command)
        # print(out,error)
        if error:
            return None
        if git_branch != out:
            command = f"git checkout {git_branch}"
            out,error = self.ssh_execute_command(command)
            # print(command,out,error)
            if error:
                return None
        

    def git_changes(self, git_repo_path):
        check_files_command = (
            f"cd {git_repo_path} && git diff --name-only HEAD..origin/main"
        )
        out, error = self.ssh_execute_command(check_files_command)
        # print(out,error)
        if error:
            return None

        watched_files = {
            "models.py": "python manage.py makemigrations && python manage.py migrate",
            "requirements.txt": "pip install -r requirements.txt",
        }

        changed_files = out.strip().split("\n")
        commands_to_run = [
            watched_files[file] for file in watched_files if file in changed_files
        ]
        # print(commands_to_run)

        return (True,commands_to_run) if len(commands_to_run) > 0 else (False, commands_to_run)
