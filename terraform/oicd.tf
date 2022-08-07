data "tls_certificate" "aws_eks_cluster_cert" {
  url = aws_eks_cluster.aws_eks_cluster.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "oid_provider" {
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.aws_eks_cluster_cert.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.aws_eks_cluster.identity[0].oidc[0].issuer
}