package com.mall.application.apps.product.service;

import com.mall.application.apps.product.entity.ProductEntity;
import com.mall.application.apps.product.dto.ProductDTO;
import com.mall.application.apps.product.mapper.ProductMapper;
import com.mall.application.apps.inventory.service.InventoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 商品服务 - 商品列表、详情查询、库存校验
 */
@Service
public class ProductService {

    @Autowired
    private ProductMapper productMapper;
    @Autowired
    private InventoryService inventoryService;

    public List<ProductDTO> getProductList(int page, int size) {
        List<ProductEntity> products = productMapper.selectPage(page, size);
        return products.stream().map(ProductDTO::new).collect(Collectors.toList());
    }

    public ProductDTO getProductDetail(String productId) {
        ProductEntity product = productMapper.selectById(productId);
        int stock = inventoryService.getStock(productId);
        ProductDTO dto = new ProductDTO(product);
        dto.setStockQuantity(stock);
        return dto;
    }

    public boolean checkStock(String productId, int requiredQuantity) {
        int available = inventoryService.getStock(productId);
        return available >= requiredQuantity;
    }

    public ProductDTO addProduct(ProductEntity productEntity) {
        productMapper.insertProduct(productEntity);
        return new ProductDTO(productEntity);
    }
}