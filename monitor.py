import subprocess

#Memory usage
cmd1 = ["cat", "/proc/meminfo"]
bout1 = subprocess.check_output(cmd1)
sout1 = bout1.decode("utf-8").splitlines()
memtotal = int(sout1[0].split()[1])
memfree = int(sout1[1].split()[1])
memused = memtotal - memfree
permemused = (memused/memtotal)*100
print(permemused)

#Cpu usage
cmd2 = ["sar","-u", "2", "1"]
bout2 = subprocess.check_output(cmd2)
sout2 = bout2.decode("utf-8").splitlines()
sout2 = sout2[len(sout2)-1].split()
cpufree = float(sout2[len(sout2)-1])
percpuused = 100 - cpufree
print(percpuused)