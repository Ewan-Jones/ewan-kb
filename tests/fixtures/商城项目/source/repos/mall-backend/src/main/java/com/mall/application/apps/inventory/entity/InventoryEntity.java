package com.mall.application.apps.inventory.entity;

import java.time.LocalDateTime;

/**
 * 库存实体类
 */
public class InventoryEntity {

    private String inventoryId;
    private String productId;
    private int quantity;
    private String warehouseCode;
    private int lockedQuantity;
    private int availableQuantity;
    private LocalDateTime updateTime;

    public InventoryEntity() {
        this.lockedQuantity = 0;
        this.updateTime = LocalDateTime.now();
    }

    public String getInventoryId() { return inventoryId; }
    public void setInventoryId(String inventoryId) { this.inventoryId = inventoryId; }
    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; this.availableQuantity = quantity - this.lockedQuantity; }
    public String getWarehouseCode() { return warehouseCode; }
    public void setWarehouseCode(String warehouseCode) { this.warehouseCode = warehouseCode; }
    public int getLockedQuantity() { return lockedQuantity; }
    public void setLockedQuantity(int lockedQuantity) { this.lockedQuantity = lockedQuantity; this.availableQuantity = this.quantity - lockedQuantity; }
    public int getAvailableQuantity() { return availableQuantity; }
    public void setAvailableQuantity(int availableQuantity) { this.availableQuantity = availableQuantity; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime updateTime) { this.updateTime = updateTime; }
}