resource_group_name = "dbx-rg"
hubcidr          = "10.1.0.0/16"
spokecidr        = "10.0.0.0/16"
vnetname         = "dbx-vnet"
hostsubnet       = "host"
containersubnet  = "container"
pesubnet         = "pe-subnet"
rglocation       = "eastus"
metastoreip      = "20.62.132.167"
dbfs_prefix      = "dbfs"

workspace_prefix = "adb"
no_public_ip     = true
firewallfqdn = [                                                      // we don't need scc relay and dbfs fqdn since they will go to private endpoint
  "dbartifactsprodeastus.blob.core.windows.net",                        //databricks artifacts
  "dbartifactsprodeap.blob.core.windows.net",                         //databricks artifacts secondary
  "dblogprodeastus.blob.core.windows.net",                            //log blob
  "prod-eastus1-observabilityEventHubs.servicebus.windows.net",
  "prod-eastusc2-observabilityeventhubs.servicebus.windows.net",
  "prod-eastusc3-observabilityeventhubs.servicebus.windows.net",
 //eventhub
  "cdnjs.com",                                                        //ganglia
]
