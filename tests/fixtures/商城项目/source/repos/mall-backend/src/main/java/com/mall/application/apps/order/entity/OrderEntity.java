package com.mall.application.apps.order.entity;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 订单实体类
 * 状态枚举: PENDING, PAID, SHIPPED, CANCELLED
 */
public class OrderEntity {

    private String orderId;
    private String memberId;
    private String productId;
    private int quantity;
    private BigDecimal totalAmount;
    private String status; // PENDING / PAID / SHIPPED / CANCELLED
    private LocalDateTime createTime;
    private LocalDateTime updateTime;

    public OrderEntity() {
        this.status = "PENDING";
        this.createTime = LocalDateTime.now();
        this.updateTime = LocalDateTime.now();
    }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public String getMemberId() { return memberId; }
    public void setMemberId(String memberId) { this.memberId = memberId; }
    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public BigDecimal getTotalAmount() { return totalAmount; }
    public void setTotalAmount(BigDecimal totalAmount) { this.totalAmount = totalAmount; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; this.updateTime = LocalDateTime.now(); }
    public LocalDateTime getCreateTime() { return createTime; }
    public LocalDateTime getUpdateTime() { return updateTime; }
}