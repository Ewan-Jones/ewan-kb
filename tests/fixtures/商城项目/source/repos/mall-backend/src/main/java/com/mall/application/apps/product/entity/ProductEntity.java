package com.mall.application.apps.product.entity;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 商品实体类
 * 状态枚举: ON_SALE, OFF_SALE
 */
public class ProductEntity {

    private String productId;
    private String productName;
    private String category;
    private BigDecimal price;
    private String description;
    private String status; // ON_SALE / OFF_SALE
    private LocalDateTime createTime;

    public ProductEntity() {
        this.status = "ON_SALE";
        this.createTime = LocalDateTime.now();
    }

    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public BigDecimal getPrice() { return price; }
    public void setPrice(BigDecimal price) { this.price = price; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime createTime) { this.createTime = createTime; }
}