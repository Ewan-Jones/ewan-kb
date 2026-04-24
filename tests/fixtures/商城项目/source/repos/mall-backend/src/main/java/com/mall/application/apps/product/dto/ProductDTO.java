package com.mall.application.apps.product.dto;

import java.math.BigDecimal;

/**
 * 商品数据传输对象
 */
public class ProductDTO {

    private String productId;
    private String productName;
    private BigDecimal price;
    private int stockQuantity;

    public ProductDTO() {}

    public ProductDTO(com.mall.application.apps.product.entity.ProductEntity entity) {
        this.productId = entity.getProductId();
        this.productName = entity.getProductName();
        this.price = entity.getPrice();
    }

    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    public int getStockQuantity() { return stockQuantity; }
    public void setStockQuantity(int stockQuantity) { this.stockQuantity = stockQuantity; }
}