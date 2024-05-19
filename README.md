# Setup virtual environment using anaconda

```python
conda create -n jenkins-env python=3.10 -y
conda activate jenkins-env
pip install -r requirements.txt
pip insttall .
```

# Test the FastAPI

```json
{
  "Gender": "Male",
  "Married": "No",
  "Dependents": "2",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 5849,
  "CoapplicantIncome": 0,
  "LoanAmount": 1000,
  "Loan_Amount_Term": 1,
  "Credit_History": "1.0",
  "Property_Area": "Rural"
}
```

# Docker Comamnds

```
docker build -t loan_pred:v1 .
docker build -t maxlee1998/cicd:v1 .
docker push maxlee1998/cicd:v1

docker run -d -it --name modelv1 -p 8005:8005 maxlee1998/cicd:v1 bash

docker exec modelv1 python prediction_model/training_pipeline.py

docker exec modelv1 pytest -v --junitxml TestResults.xml --cache-clear

docker cp modelv1:/code/src/TestResults.xml .

 // Running the Fast API server
docker exec -d -w /code modelv1 python main.py

// if you want to specify the port
docker exec -d -w /code modelv1 uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8005
```

# Setting up AWS EC2 Server

1. Create a key pair
2. Launce the instance
3. Wait for the instance to be running, then click onto "connect"
4. Open up git bash to run the chmod command `chmod 400 "aws-mlops.pem"`
5. Connect to EC2 instance via the AWS Command example `ssh -i "aws-mlops.pem" ubuntu@ec2-54-210-195-95.compute-1.amazonaws.com`

## Installing Jenkins

```bash
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins

sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version

sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins


```

### Get Jenkins default password

`sudo cat /var/lib/jenkins/secrets/initialAdminPassword`

### Verifying Jenkins

1. Add the security inbound rule to allow All TCP IPV4 and All TCP IPV6
2. Once saved, give it some time to load, go to the Public IPV4 Address of EC2 and check the port 8080 if the Jenkin service is running
   `54.210.195.95:8080`

3. Login to Jenkins:
   user = `admin`
   pass = `f46a7d85b02f465e9ed6a769e664f4b0`

### Plugins for Jenkins

1. Get the password from bash when you attempt to access the Public IPV4 address
2. Setup the plugins, enable the JUnit, Github and Email Templates
3. Skip and use admin

### Linking to Github

1. Manage Jenkins > Credentials > System > Global Credentials (Unrestricted)
2. Kind = Secret Text, Secret = `[Github Generated Key]`
3. Once confirmed / created profile > go back to Github Repository and click onto Repository Settings > Go to Webhooks, Add Webhook
4. Payload URL = `http://54.210.195.95:8080/github-webhook/`, Content Type = `application/json`
5. Go back to Jenkins Page > Manage Jenkins > System > Scroll down to `Github` > Add Server > Name = `jenkins` , credentials = `jenkins` (newly created) > Test Connection

6. If you have created a jenkins project, need to configure the settings to use `Git` for source code management. Add the repository URL : `https://github.com/maxlee98/jenkins-cicd`
7. Edit which branch to use, by default = `master` but some use `main` change to whichever you are using

## Installing Docker

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -a -G docker jenkins
sudo usermod -a -G docker $USER
```

Restart the EC2 instance if `docker ps` still shows permission denied

### Using Docker with Jenkins

1. Go to Jenkins dashboard > Manage Jenkins > Plugins > Docker (with the cloud) > Install
2. Once installed go to > Manage Jenkins > Cloud > Create New docker (check the docker box) > copy and paste the uri suggested and test the connection.
3. Create a new credential. Login to Dockerhub on another webpage.
4. Dockerhub > Account Settings > Securities > Generate New Access Token
5. Copy the Password and paste into Jenkins webpage in the `Password` field
6. Click onto save and check if you can select the new created credentials (even if cannot just click on save first)
7. Go to your Jenkins Project and

## Linking Gmail with Jenkins for Notification

1. Go to gmail and enable the 2fa
2. Create a new App Password (call it however you like)
3. Open up the Jenkins Page (Dashboard > Manage Jenkins > System)
4. You may edit the system admin e-mail address (Example = `jenkin-admin<admin@cicdteam.com>`)
5. Scroll down to Extended Gmail Notification, add SMTP server = `smtp.gmail.com`, SMTP Port = 465
6. Click on advanced and add your new credentials for your email account.
7. Username = email (Example `abendigo100@gmail.com`), Password = `[generated password from Google App password]` (!! WITHOUT THE BLANK SPACES !!), id = `[any id]` then click `Add`
8. Select the newly created credentials, Check the use SSL and use TLS box
9. You may choose to add the Default Receipient and Reply to List
10. You may edit the Default Content of the email
11. Under Default Triggers > Check `Always` option to always send the email
12. Once done and checked, click on `Apply` then `Save`
13. Now go to your project that you would want to send the email everytime a build is completed. Click on `Configure`
14. Add the Post Build Step `Editable Email Notification` then `Attach Build Log`

# CICD Process

## Github to Jenkins to Docker

1. Ensure that within a build step, after you have built the image, you would have to include in a `Build/Publish Docker Image`
2. Directory for Dockerfile (varies from Project to Project) `$WORKSPACE`
3. Select the Registry credentials as the docker credentials
4. Advanced options: Select the created Cloud within Jenkins for building the image (previously created `Cloud`)
5. Image : `maxlee1998/cicd:latest`

## Training with the Build Docker Image

1. Create a new Freestyle project, go to Build Triggers, Projects to watch would depend on the name of the project meant to build the image
2. Trigger only if build is stable.
3. Add the Docker code to run after the image is built and the execution code
   `docker run -d -it --name modelv1 -p 8005:8005 maxlee1998/cicd:latest bash` > `docker exec modelv1 python prediction_model/training_pipeline.py`
4. Save the configuration and test the build by running the first project `1-Github-Docker` and see if it links to `2-Training-Project`
5. If there is the error that the container is already in use, you need to use `docker stop [container name]` and `docker rm [container name]` to reuse the command
6.

### Automate the deletion of Docker Container

Hi, you can also use this to automate the deletion of container if exists already, add this before

```bash
#!/bin/bash

CONTAINER_NAME="modelv1"

# Check if the container exists

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then

    # If it exists, stop and remove it

    echo "Stopping and removing existing container: $CONTAINER_NAME"

    docker stop $CONTAINER_NAME

    docker rm $CONTAINER_NAME

else

    echo "Container $CONTAINER_NAME does not exist."

fi
```

## Testing with Docker Built Image

1. Add the build steps needed to execute the test and also to copy the test results from docker to the host system
2. !! Post build actions: Publish JUnit Test Result Report

## Deploy to Server

1. Create a new freestyle project and
