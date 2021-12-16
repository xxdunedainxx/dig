#! /bin/bash

APPLICATION_DEPLOYMENT_PATH=/home/ec2-user/dig
HOME=$(pwd)

if [[ ! -f "./deployment/INSTANCE.txt" || ! -f "./deployment/SSH_KEY_PATH.txt" || ! -f "./deployment/USERNAME.txt" ]] ;then
  read -p "Please provide your AWS EC2 instance:" AWS_EC2_INSTANCE
  read -p "Please specify the path of your SSH Key" SSH_KEY_PATH
  read -p "Please specify your username" USERNAME

  echo "${AWS_EC2_INSTANCE}" > "./deployment/INSTANCE.txt"
  echo "${SSH_KEY_PATH}"     > "./deployment/SSH_KEY_PATH.txt"
  echo "${USERNAME}"         > "./deployment/USERNAME.txt"
else
  AWS_EC2_INSTANCE=$(cat "./deployment/INSTANCE.txt")
  SSH_KEY_PATH=$(cat "./deployment/SSH_KEY_PATH.txt")
  USERNAME=$(cat "./deployment/USERNAME.txt")
fi

./build.sh

mkdir deployment/images

echo "Bundling latest docker images in deployment/images"

docker save dig_server:latest | gzip > deployment/images/dig_server.tar.gz
docker save dig_mysql_server:latest | gzip > deployment/images/dig_mysql_server.tar.gz

# Upload steps

ssh "${USERNAME}@${AWS_EC2_INSTANCE}" -i "${SSH_KEY_PATH}" -- """\
mkdir -p ${APPLICATION_DEPLOYMENT_PATH}
"""

echo "Uploading docker files..."
scp -v -i "${SSH_KEY_PATH}" "deployment/images/dig_mysql_server.tar.gz" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"
scp -v -i "${SSH_KEY_PATH}" "deployment/images/dig_server.tar.gz" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"

echo "Publishing docker compose"
scp -v -i "${SSH_KEY_PATH}" "docker-compose.yml" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"

echo "Publishing util scripts"
scp -v -i "${SSH_KEY_PATH}" "deployment/setup/install_new_images.sh" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"
scp -v -i "${SSH_KEY_PATH}" "deployment/setup/docker_setup.sh" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"
scp -v -i "${SSH_KEY_PATH}" "run.sh" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"
scp -v -i "${SSH_KEY_PATH}" "prod.conf.json" "${USERNAME}@${AWS_EC2_INSTANCE}":"${APPLICATION_DEPLOYMENT_PATH}"