import subprocess
import os
import sys


class CrontabRegister:
    def __init__(self,
                 channel_id,
                 time_limit_for_checking_in_minutes=None,  # Default time interval is 10 minutes
                 time_limit_for_checking_in_hours=None,  # Default time interval is 10 minutes
                 python_executable=sys.executable,  # Default python executable is the current python executable
                 cron_expression="*/10 * * * *",  # Default cron expression is every 10 minutes
                 absolute_path_of_python_script=os.getcwd() + "/youtube_community_alarm.py",
                 absolute_path_of_log_file=os.getcwd() + "/log.log",
                 **kwargs):
        self.channel_id = channel_id
        self.python_executable = python_executable
        self.cron_expression = cron_expression
        self.absolute_path_of_python_script = absolute_path_of_python_script
        self.absolute_path_of_log_file = absolute_path_of_log_file
        self.time_limit_for_checking_in_minutes = time_limit_for_checking_in_minutes if time_limit_for_checking_in_minutes else kwargs.get("time_limit_for_checking_in_minutes")
        self.time_limit_for_checking_in_hours = time_limit_for_checking_in_hours if time_limit_for_checking_in_hours else kwargs.get("time_limit_for_checking_in_hours")

        time_limit_arguments = " --time_limit_for_checking_in_minutes " + str(self.time_limit_for_checking_in_minutes) if self.time_limit_for_checking_in_minutes else "--time_limit_for_checking_in_hours " + str(self.time_limit_for_checking_in_hours)
        self.arguments = f"--channel_id {self.channel_id} " + time_limit_arguments

    def register_crontab(self):
        cron_command = f"{self.python_executable} {self.absolute_path_of_python_script} {self.arguments} >> {self.absolute_path_of_log_file} 2>&1"
        cron_job = f'(crontab -l; echo "{self.cron_expression} {cron_command}") | crontab -'

        try:
            subprocess.run(cron_job, shell=True, check=True)
            print("Cron job registered successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error registering cron job: {e}")





