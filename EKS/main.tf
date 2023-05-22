module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-cluster"
  cluster_version = "1.24"
  subnet_ids      = module.vpc.private_subnets
   cluster_endpoint_public_access = true

  vpc_id = module.vpc.vpc_id
  eks_managed_node_groups = {
  one = {
    name = "server-1"

    instance_types = ["t3.small"]

    min_size     = 1
    max_size     = 3
    desired_size = 1
    }
  }
}


module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.103.0/24", "10.0.203.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true
  
  public_subnet_tags = {
    "kubernetes.io/cluster/my-cluster" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/my-cluster" = "shared"
    "kubernetes.io/role/internal-elb"             = 1
  }
}






