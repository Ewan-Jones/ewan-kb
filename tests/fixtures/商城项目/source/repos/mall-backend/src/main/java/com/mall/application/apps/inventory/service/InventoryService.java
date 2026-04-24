package com.mall.application.apps.inventory.service;

import com.mall.application.apps.inventory.entity.InventoryEntity;
import com.mall.application.apps.inventory.mapper.InventoryMapper;
import com.mall.application.apps.product.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 库存服务 - 库存查询、扣减、调整
 */
@Service
public class InventoryService {

    @Autowired
    private InventoryMapper inventoryMapper;
    @Autowired
    private ProductService productService;

    public int getStock(String productId) {
        InventoryEntity inventory = inventoryMapper.selectByProductId(productId);
        return inventory != null ? inventory.getAvailableQuantity() : 0;
    }

    public void decreaseStock(String productId, int quantity) {
        productService.getProductDetail(productId);
        InventoryEntity inventory = inventoryMapper.selectByProductId(productId);
        if (inventory.getAvailableQuantity() < quantity) {
            throw new RuntimeException("库存不足");
        }
        inventoryMapper.updateQuantity(productId, inventory.getQuantity() - quantity);
    }

    public void adjustStock(String productId, int delta) {
        productService.getProductDetail(productId);
        InventoryEntity inventory = inventoryMapper.selectByProductId(productId);
        inventoryMapper.updateQuantity(productId, inventory.getQuantity() + delta);
    }

    public boolean lockStock(String productId, int quantity) {
        return inventoryMapper.lockStock(productId, quantity) > 0;
    }
}