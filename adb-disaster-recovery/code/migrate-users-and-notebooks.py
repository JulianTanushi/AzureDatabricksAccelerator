import sys
import os
import subprocess
from subprocess import call, check_output

EXPORT_PROFILE = "primary"
IMPORT_PROFILE = "secondary"

# Get a list of all users
user_list_out = check_output(["databricks", "workspace", "list", "/Users", "--profile", EXPORT_PROFILE])
user_list = (user_list_out.decode(encoding="utf-8")).splitlines()

print (user_list)

# Export sandboxed environment(folders, notebooks) for each user and import into new workspace.
#Libraries are not included with these APIs / commands.

for user in user_list:
  #print("Trying to migrate workspace for user ".decode() + user)
  print (("Trying to migrate workspace for user ") + user)

  subprocess.call(str("mkdir -p ") + str(user), shell = True)
  export_exit_status = call("databricks workspace export_dir /Users/" + str(user) + " ./" + str(user) + " --profile " + EXPORT_PROFILE, shell = True)

  if export_exit_status==0:
    print ("Export Success")
    import_exit_status = call("databricks workspace import_dir ./" + str(user) + " /Users/" + str(user) + " --profile " + IMPORT_PROFILE, shell=True)
    if import_exit_status==0:
      print ("Import Success")
    else:
      print ("Import Failure")
  else:
    print ("Export Failure")
print ("All done")