package com.mall.application.apps.order.dto;

import java.math.BigDecimal;

/**
 * 订单数据传输对象
 */
public class OrderDTO {

    private String orderId;
    private String productName;
    private int quantity;
    private BigDecimal totalAmount;
    private String statusName;

    public OrderDTO() {}

    public OrderDTO(com.mall.application.apps.order.entity.OrderEntity entity) {
        this.orderId = entity.getOrderId();
        this.quantity = entity.getQuantity();
        this.totalAmount = entity.getTotalAmount();
        this.statusName = mapStatusName(entity.getStatus());
    }

    private String mapStatusName(String status) {
        switch (status) {
            case "PENDING": return "待支付";
            case "PAID": return "已支付";
            case "SHIPPED": return "已发货";
            case "CANCELLED": return "已取消";
            default: return status;
        }
    }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
    public BigDecimal getTotalAmount() { return totalAmount; }
    public void setTotalAmount(BigDecimal totalAmount) { this.totalAmount = totalAmount; }
    public String getStatusName() { return statusName; }
    public void setStatusName(String statusName) { this.statusName = statusName; }
}