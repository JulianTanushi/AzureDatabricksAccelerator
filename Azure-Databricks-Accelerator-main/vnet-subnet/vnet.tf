
resource "azurerm_virtual_network" "this" {
  name                = var.vnetname
  location            = azurerm_resource_group.this.location
  resource_group_name = var.resource_group_name
  address_space       = ["10.0.0.0/16"]
  tags                = local.tags
}




resource "azurerm_subnet" "host" {
  name                 = var.hostsubnet
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = ["10.0.1.64/26"]

}


resource "azurerm_subnet" "container" {
  name                 = var.containersubnet
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = ["10.0.1.128/26"]

  private_link_service_network_policies_enabled = true
}


resource "azurerm_subnet" "pesubnet" {
  name                                           = var.pesubnet
  resource_group_name                            = var.resource_group_name
  virtual_network_name                           = azurerm_virtual_network.this.name
  private_link_service_network_policies_enabled  = true
  address_prefixes =  ["10.0.1.192/27"]
}


