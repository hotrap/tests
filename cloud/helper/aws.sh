sudo mkfs.ext4 /dev/nvme1n1    
sudo mkdir /mnt/sd    
sudo mount /dev/nvme1n1 /mnt/sd
sudo chown $USER:$USER /mnt/sd
mkdir -p /mnt/sd/{db,sd,viscnts}     
sudo bash -c "echo \"/dev/nvme1n1 /mnt/sd ext4 defaults 0 0\" >> /etc/fstab"

mkdir testdb
cd testdb
ln -s /mnt/sd/{db,sd,viscnts} .
mkdir cd
cd ..

echo "export sd_dev=nvme1n1" >> ~/.profile
echo 'export cd_dev=nvme0n1' >> ~/.profile
