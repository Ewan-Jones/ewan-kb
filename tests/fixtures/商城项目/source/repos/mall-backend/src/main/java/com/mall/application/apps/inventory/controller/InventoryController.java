package com.mall.application.apps.inventory.controller;

import com.mall.application.apps.inventory.service.InventoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 库存管理控制器
 * 提供库存查询、调整、扣减等接口
 */
@RestController
@RequestMapping("/api/inventory")
public class InventoryController {

    @Autowired
    private InventoryService inventoryService;

    /**
     * 获取商品库存
     */
    @GetMapping("/{productId}")
    public int getStock(@PathVariable String productId) {
        return inventoryService.getStock(productId);
    }

    /**
     * 调整库存
     */
    @PostMapping("/adjust")
    public String adjustStock(@RequestParam String productId,
                              @RequestParam int delta) {
        inventoryService.adjustStock(productId, delta);
        return "SUCCESS";
    }

    /**
     * 扣减库存
     */
    @PostMapping("/decrease")
    public String decreaseStock(@RequestParam String productId,
                                @RequestParam int quantity) {
        inventoryService.decreaseStock(productId, quantity);
        return "SUCCESS";
    }
}