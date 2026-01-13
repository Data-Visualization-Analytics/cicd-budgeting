# cicd-budgeting
create cicd using minio server, jenkins and docker

### step1: setup local jenkins instance or pull jenkins image, also download docker plugins
  documentation: [https://www.jenkins.io/doc/book/installing/]
### step2: setup local minio or docker pull minio image and setup or if you have aws s3 then provide necessary creds
  documentation: [https://docs.min.io/enterprise/aistor-object-store/installation/container/install/]

### step3: clone github repo https://github.com/Data-Visualization-Analytics/cicd-budgeting.git and set up your creds to jenkins
### step4: create jenkins freestyle pipeline and add in execute shell below code:
```
export PATH=/usr/local/bin:$PATH

docker build -t cicd-budgeting .
#!/bin/bash
echo "$AWS_ACCESS_KEY_ID"
docker run \
	-e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
	-e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
    -e AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION" \
    cicd-budgeting
```
### step5: You should be able to see your processed file in MiniO bucket
<img width="1427" height="286" alt="image" src="https://github.com/user-attachments/assets/586e2138-9b64-41b9-b5c6-925889ab9e08" />

### Jenkins Pipeline
<img width="1029" height="115" alt="image" src="https://github.com/user-attachments/assets/d7e57741-d25b-4c67-96cf-4ed61ebc57d1" />

