# Creates the EKS main cluster
# Note: No compute is created automatically, so all pods fail to schedule, including core DNS
resource "aws_eks_cluster" "aws_eks_cluster" {
  name     = "aws_eks_cluster"
  role_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/EksClusterRole"
  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  vpc_config {
    subnet_ids = [
      "subnet-111", #Public Subnet 1 ID
      "subnet-222" #Public Subnet 2 ID
    ]
  }
  timeouts {
    delete = "30m"
  }
}
