package com.mall.application.apps.inventory.mapper;

import com.mall.application.apps.inventory.entity.InventoryEntity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

/**
 * 库存数据映射接口
 */
@Mapper
public interface InventoryMapper {

    InventoryEntity selectByProductId(@Param("productId") String productId);

    int updateQuantity(@Param("productId") String productId, @Param("quantity") int quantity);

    int lockStock(@Param("productId") String productId, @Param("quantity") int quantity);

    int insertInventory(InventoryEntity inventoryEntity);

    int deleteByProductId(@Param("productId") String productId);
}