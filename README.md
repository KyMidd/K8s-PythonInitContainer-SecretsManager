# K8s-CSI-SecretsManager

Deployable docker, k8s, and terraform to deploy a pod to fetch secrets dynamically from AWS Secrets Manager on pod launch using custom python script. The Init container is called with arguments to tell it which secret string ARNs to search against with fuzzy matching to identify multiple secrets. It stages those secret values in a shared dir for the app container to ingest as arguments, with K8s over-riding the entrypoint and args. 

This avoid K8s "Secrets" (which K8s doesn't protect well), and instead calls the secrets on demand each time, with secret values never leaving the "pod" construct. 

The weakness of this of course is: 
1. Secrets live on disk and not just in memory.
2. Secrets are called live on each pod restart/redeploy. If the AWS Secret Manager API is down (or rate-limited due to large applications), the pod will delay or fail to launch. 

Secrets are refreshed each time pod is launched, either via manual action or deployment replace. Secrets are not automatically refreshed on a live pod unless configured to do so. 

Docker config builds: 
- An image which does nothing, and stays online for interactive terminal for testing

Terraform config builds: 
- Eks k8s cluster
- EKS node group
- IAM Role + Policy with assume role policy
- OID Provider
- Secret in Secrets Manager and populate it with json payload

K8s config builds: 
- Our Service Account
- Our SecretProviderClass
- Our App1 host
- Our Init host with embedded python to call secrets
