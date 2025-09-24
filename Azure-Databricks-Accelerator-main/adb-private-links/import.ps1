# Define variables
$subscriptionId = "7c77785e-55b1-434e-914a-f520f3234923"
$resourceGroupName = "dbx-rg"
$vnetName = "dbx-vnet"
$hostsubnetName = "host"
$containersubnetName = "container"
$pesubnetName = "pe-subnet"

# Import resource group
Write-Host "Importing Resource Group..."
terraform import azurerm_resource_group.this "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName"

# Import virtual network
Write-Host "Importing Virtual Network..."
terraform import azurerm_virtual_network.this "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Network/virtualNetworks/$vnetName"

# Import subnet
Write-Host "Importing Host Subnet..."
terraform import azurerm_subnet.host "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Network/virtualNetworks/$vnetName/subnets/$hostsubnetName"

# Import subnet
Write-Host "Importing Container Subnet..."
terraform import azurerm_subnet.container "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Network/virtualNetworks/$vnetName/subnets/$containersubnetName"

# Import subnet
Write-Host "Importing PE Subnet..."
terraform import azurerm_subnet.pesubnet "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Network/virtualNetworks/$vnetName/subnets/$pesubnetName"
