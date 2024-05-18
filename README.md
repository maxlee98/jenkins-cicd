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

### Verifying Jenkins

1. Add the security inbound rule to allow All TCP IPV4 and All TCP IPV6
2. Once saved, give it some time to load, go to the Public IPV4 Address of EC2 and check the port 8080 if the Jenkin service is running
   `54.210.195.95:8080`

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
