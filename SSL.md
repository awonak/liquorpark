# Lets Encrypt + EB Single Instance + Django

I am currently running a Single Instance elastic beanstalk server that I would
like to add SSL to using Lets Encrypt. Since LE is still in beta, the amazon
flavor of linux used by eb is not yet supported, so we need to do the manual
installation. Furthermore, since I'm using elastic beanstalk, I wanted to make
sure that the cert installation was reproducable when creating new environments.

From a high level we need to do the following steps:

1. Run letsencrypt-auto to being creating the certificate
1. Add a specific url to your domain proving ownership
1. Once certs are generated, move them to the appropriate place
1. Add certs to s3 and grant permission to that bucket for the eb role
1. Install mod_ssl and update apache conf
1. Reprovision / restart server


## Creat Lets Encrypt Cert

First, I needed to clone the letsencrypt repo to my running instance and run a
few commands.

```bash
$ git clone https://github.com/letsencrypt/letsencrypt
$ cd letsencrypt/
$ ./letsencrypt-auto certonly --manual
```

During that step I was asked to have my domain serve a url to prove ownership.
Since my app was already running, I just added a url route which pointed to a
text file containing my challenge response, deployed and was up and serving
the challenge.

```python
# in my root urls.py
url(r'^.well-known/acme-challenge/frz<...>n8o',
    TemplateView.as_view(template_name='letsencrypt.txt',
    content_type='text/plain')),
```

Once this was live I continued with the `letsencrypt-auto` prompts and
successfully generated the certificate files. The certificate files get
installed in `/etc/letsencrypt/live/$domain`.

# Move certificate files

Next, I needed to get my ssl certs on S3 so I can get them when I deploy a new
environment. In order to do this, I needed to grant S3 access to my eb role.

In the AWS console, navigate to `IAM > Roles > aws-elasticbeanstalk-ec2-role`
and add an Inline Policy under the permission tab.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::<mydomain>/*",
                "arn:aws:s3:::<mydomain>"
            ]
        }
    ]
}
```

Now with the read/write access on S3 I was able to put the files on S3 for later
access.

```
$ aws s3 sync /etc/letsencrypt/live/<mydomain>/ s3://<mydomain>/ssl/
```

Finally, I needed to add the certificates to IAM:

```bash
$ aws iam upload-server-certificate \
    --server-certificate-name <mydomain>-ssl \
    --certificate-body /etc/letsencrypt/live/<mydomain>/cert.pem \
    --private-key /etc/letsencrypt/live/<mydomain>/privkey.pem \
    --certificate-chain /etc/letsencrypt/live/<mydomain>/chain.pem
```

## Configure Apache

I needed to add configuration to serve https. I added an apache configuration
file called `ssl.conf` to override `wsgi.conf`.

```
Listen 443
<VirtualHost *:80>
  ServerName www.<mydomain>.com
  Redirect permanent / https://www.<mydomain>.com/
</VirtualHost>

<VirtualHost *:443>
  ServerName www.<mydomain>.com

  SSLEngine on
  SSLCertificateFile "/etc/pki/tls/certs/server.crt"
  SSLCertificateKeyFile "/etc/pki/tls/certs/server.key"
  SSLCertificateChainFile "/etc/pki/tls/certs/chain.pem"

</VirtualHost>
```

To add this configuration change upon provisioning an environment, I added it to
my `.ebextensions`:

```yaml
container_commands:
  01_replace_ssl:
    command: "cp .ebextensions/ssl.conf /etc/httpd/conf.d/"
```


## Configure elastic beanstalk environment

When provisioning a new environment, we need to fetch the certs and open port
443.

Install mod_ssl
```yaml
packages:
  yum:
    mod24_ssl : []
```

Copy our certs from s3 to the new environment

```yaml
files:
  "/etc/pki/tls/certs/server.crt" :
    mode: "000400"
    owner: root
    group: root
    authentication: "S3Auth"
    source: https://liquorpark.s3.amazonaws.com/ssl/server.crt
  "/etc/pki/tls/certs/server.key" :
    mode: "000400"
    owner: root
    group: root
    authentication: "S3Auth"
    source: https://liquorpark.s3.amazonaws.com/ssl/server.key
  "/etc/pki/tls/certs/chain.pem" :
    mode: "000400"
    owner: root
    group: root
    authentication: "S3Auth"
    source: https://liquorpark.s3.amazonaws.com/ssl/chain.pem
```

Finally, configure the Resources (I don't think this worked, I needed to
manually update the incoming ports on the running instance):

```yaml
Resources:
  sslSecurityGroupIngress:
    Type: AWS::EC2::SecurityGroupIngress
    Properties:
      GroupId: {"Fn::GetAtt" : ["AWSEBSecurityGroup", "GroupId"]}
      IpProtocol: tcp
      ToPort: 443
      FromPort: 443
      CidrIp: 0.0.0.0/0
  AWSEBAutoScalingGroup:
    Metadata:
      AWS::CloudFormation::Authentication:
        S3Auth:
          type: "s3"
          buckets: "liquorpark"
          roleName: "aws-elasticbeanstalk-ec2-role"
```


Test everything by creating a new environment using elastic beanstalk:

```bash
$ eb create mydomain-ssl --single
```

Everything should provision correctly, however the cert will still fail because
the cert is for your real domain, not the one provided by elastic beanstalk. If
everything looks good, we can deploy these changes to your main running instance.
