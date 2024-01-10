sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir /mnt/cd
sudo mount /dev/nvme1n1 /mnt/cd
sudo chown -R $USER:$USER /mnt/cd
sudo bash -c "echo \"/dev/nvme1n1 /mnt/cd ext4 defaults 0 0\" >> /etc/fstab"

sudo mkfs.ext4 /dev/nvme2n1
sudo mkdir /mnt/sd
sudo mount /dev/nvme2n1 /mnt/sd
sudo chown -R $USER:$USER /mnt/sd
mkdir -p /mnt/sd/{db,sd,viscnts}     
sudo bash -c "echo \"/dev/nvme2n1 /mnt/sd ext4 defaults 0 0\" >> /etc/fstab"

cd ~
mkdir testdb
cd testdb
ln -s /mnt/sd/{db,sd,viscnts} .
ln -s /mnt/cd .
cd ..

echo "export sd_dev=nvme2n1" >> ~/.profile
echo 'export cd_dev=nvme1n1' >> ~/.profile
