wget -O - 192.168.0.162:8000/rootfs.ext4 | dd of=/dev/mmcblk0p2 bs=4096 
mkdir /tmp/d
mount /dev/mmcblk0p1 /tmp/d
cd /tmp/d/utility
rm ./Image
rm ./bcmcostam
wget 192.168.0.162:8000/Image 
wget 192.168.0.162:8000/bcmcostam