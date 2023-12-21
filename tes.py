
def restart():
    import sys
    import subprocess
    # Run the git pull command
    result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE)
    # Check the exit code of the command
    if result.returncode != 0:
        print("Error: Git pull failed with exit code {}".format(result.returncode))
    else:
        print("Success: Git pull was executed successfully.")
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")

    import os
    os.execv(sys.executable, ['python'] + sys.argv)
while True:
    print('estou execultando')
    parar = input('parar?')
    if parar == 'sim':
        restart()