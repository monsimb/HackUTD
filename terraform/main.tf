# Example Terraform Config to create a
# MongoDB Atlas Shared Tier Project, Cluster,
# Database User and Project IP Whitelist Entry
#
# First step is to create a MongoDB Atlas account
# https://docs.atlas.mongodb.com/tutorial/create-atlas-account/
#
# Then create an organization and programmatic API key
# https://docs.atlas.mongodb.com/tutorial/manage-organizations
# https://docs.atlas.mongodb.com/tutorial/manage-programmatic-access
#
# Terraform MongoDB Atlas Provider Documentation
# https://www.terraform.io/docs/providers/mongodbatlas/index.html
# Terraform 0.14+, MongoDB Atlas Provider 0.9.1+


locals {
  cluster_instance_size_name = "M0"
  mongodb_version = "4.4"
}

provider "mongodbatlas" {
  public_key  = var.mongodb_atlas_api_pub_key
  private_key = var.mongodb_atlas_api_pri_key
}

#
# Create a Project
#
resource "mongodbatlas_project" "my_project" {
  name   = var.atlas_project_name
  org_id = var.atlas_org_id
}

#
# Create an Atlas Admin Database User
#
resource "mongodbatlas_database_user" "my_user" {
  username           = var.mongodb_atlas_database_username
  password           = var.mongodb_atlas_database_user_password
  project_id         = mongodbatlas_project.my_project.id
  auth_database_name = "admin"

  roles {
    role_name     = "atlasAdmin"
    database_name = "admin"
  }
}

# Create a Database User
resource "mongodbatlas_database_user" "db-user" {
  username = "db-user"
  password = random_password.db-user-password.result
  project_id = mongodbatlas_project.my_project.id
  auth_database_name = "admin"
  roles {
    role_name     = "readWrite"
    database_name = "${var.atlas_project_name}-db"
  }
}

# Create a Database Password
resource "random_password" "db-user-password" {
  length = 16
  special = true
  override_special = "_%@"
}


#
# Create an IP Accesslist
#
# can also take a CIDR block or AWS Security Group -
# replace ip_address with either cidr_block = "CIDR_NOTATION"
# or aws_security_group = "SECURITY_GROUP_ID"
#
# Create Database IP Access List
resource "mongodbatlas_project_ip_access_list" "ip" {
  project_id = mongodbatlas_project.my_project.id
  ip_address = var.ip_address
}

#
# Create a Shared Tier Cluster
#
resource "mongodbatlas_cluster" "my_cluster" {
  project_id              = mongodbatlas_project.my_project.id
  name = "${var.atlas_project_name}-${var.environment}-cluster"

  # Provider Settings "block"
  provider_name = "TENANT"

  # options: AWS AZURE GCP
  backing_provider_name = var.cloud_provider

  # options: M2/M5 atlas regions per cloud provider
  # GCP - CENTRAL_US SOUTH_AMERICA_EAST_1 WESTERN_EUROPE EASTERN_ASIA_PACIFIC NORTHEASTERN_ASIA_PACIFIC ASIA_SOUTH_1
  # AZURE - US_EAST_2 US_WEST CANADA_CENTRAL EUROPE_NORTH
  # AWS - US_EAST_1 US_WEST_2 EU_WEST_1 EU_CENTRAL_1 AP_SOUTH_1 AP_SOUTHEAST_1 AP_SOUTHEAST_2
  provider_region_name   = var.atlas_region

  # options: M2 M5
  provider_instance_size_name = local.cluster_instance_size_name

  # Will not change till new version of MongoDB but must be included
  mongo_db_major_version = local.mongodb_version
  auto_scaling_disk_gb_enabled = "false"
}

# Use terraform output to display connection strings.
output "connection_strings" {
  value = mongodbatlas_cluster.my_cluster.connection_strings.0.standard_srv
}