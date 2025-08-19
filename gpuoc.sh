#!/bin/bash
# nvidia-smi output:
#
# ...
# +-----------------------------------------------------------------------------------------+
#| Processes:                                                                              |
#|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
#|        ID   ID                                                               Usage      |
#|=========================================================================================|
#|    0   N/A  N/A           24237      G   /usr/libexec/Xorg                         9MiB |
#|    0   N/A  N/A           24406      G   /usr/bin/gnome-shell                      4MiB |
#|    0   N/A  N/A          385108      C   python                                 5206MiB |
#|    1   N/A  N/A           24237      G   /usr/libexec/Xorg                         8MiB |
# ...
#
# Read into these variables:
#x    i     g    c               p      x
# We only care about i (index) and p (PID).
# The same user may have multiple processes on the same index, so run uniq first.
# The first awk command combines lines with the same index.
# The second awk command prints devices that have processes by multiple users.

nvidia-smi | sed '1,/Processes:/d' | while read -r line; do
    read -r x i g c p x < <(echo $line)
    if [[ $i =~ [0-9] ]]; then
        u=$(ps -p $p -o user=)
        if [ ! "$u" = "gdm" ]; then
            echo "$i: $u"
        fi
    fi
done | uniq |\
awk -F: -v ORS="" 'a!=$1""{a=$1""; $0=RS $0} a==$1""{ sub($1":"," ") } 1' |\
awk 'NF>2{print}'
