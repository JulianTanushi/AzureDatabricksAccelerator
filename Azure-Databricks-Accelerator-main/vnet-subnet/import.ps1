# Define variables
$subscriptionId = "7c77785e-55b1-434e-914a-f520f3234923"
$resourceGroupName = "dbx-rg"


# Import resource group
Write-Host "Importing Resource Group..."
terraform import azurerm_resource_group.this "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName"

