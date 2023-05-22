Gitlab CI-CD project 
==========================

General
------------

It implements a pipeline with gitlab CI-CD using a gitlab runner.
In each run it does the following:

1)Runs tests on the container and on success pushes the image to gitlab container registry while using secrets from a vault server

2)Builds the image and deploys the app to an EKS cluster provisioned with terraform

**Note:To make this project work it must be hosted on a gitlab repository**


How to build
------------

First of all make sure you have the folowing:

1)Gitlab runner

Follow this link for more info:
https://docs.gitlab.com/runner/install/linux-manually.html

2)Docker installed on the gitlab runner

You can visit this site on how to install docker: 
https://docs.docker.com/engine/install/ubuntu/


3)Gitlab runner integrated with AWS cli, you can follow the following commands:

 ```
 - curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
 
 - unzip -u awscliv2.zip
 
 - sudo ./aws/install
 
 - aws --version
 ```

4)Fully operational AWS EKS
- You can visit this site on how to install EKS: https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html

- You can use the one I provided using terraform, you can install terraform on your machine using the following commands:

```
- sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
```

```
- wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
```

```
- echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list
```

`- sudo apt update`

`- sudo apt-get install terraform`



6)Vault server

You can use the following command to run it as docker container:

 ```
 - docker run -d --cap-add=IPC_LOCK -e 'VAULT_LOCAL_CONFIG={"storage": {"file": {"path": "/vault/file"}}, "listener": [{"tcp": { "address": "0.0.0.0:8200", "tls_disable": true}}], "default_lease_ttl": "168h", "max_lease_ttl": "720h", "ui": true}' -p 8200:8200 vault server
 ```

 7)MongoDB server, you can use the free one on their website


How to run
------------

1)Set the vault secrets server and add an env in gitlab named $VAULT_TOKEN for vault's token to login & $VAULT_ADDR_LOCAL for the vault server IP address and edit these parts:


```
- docker run --rm --network host -e VAULT_TOKEN=$VAULT_TOKEN -e VAULT_ADDR=$VAULT_ADDR_LOCAL my-image python3 -m unittest test_app.py

- kubectl set env deployment/mongo-app VAULT_TOKEN=$VAULT_TOKEN_AWS VAULT_ADDR=$VAULT_SERVER_AWS

```

2)Add more env in gitlab $GITLAB_MYEMAIL for your rmail and $GITLAB_MYUSER for your username and edit this part:
```
    - git config user.email $GITLAB_MYEMAIL
    - git config user.name $GITLAB_MYUSER

```


3)Edit this line with your cluster info as well

`- aws eks update-kubeconfig --name my-cluster`

4)In the crud-app.yaml edit this line with your image name:

`- image: registry.gitlab.com/danlos44/gitlab-crud/my-image`



How to interact
------------
The service type is a load balancer
You can access it using your AWS load-balancer url
