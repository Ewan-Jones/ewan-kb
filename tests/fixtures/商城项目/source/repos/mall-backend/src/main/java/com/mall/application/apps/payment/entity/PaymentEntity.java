package com.mall.application.apps.payment.entity;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 支付实体类
 * 支付方式枚举: ALIPAY, WECHAT, BANK_CARD
 * 状态枚举: INIT, PROCESSING, SUCCESS, FAILED, REFUNDED
 */
public class PaymentEntity {

    private String paymentId;
    private String orderId;
    private BigDecimal amount;
    private String paymentMethod; // ALIPAY / WECHAT / BANK_CARD
    private String status; // INIT / PROCESSING / SUCCESS / FAILED / REFUNDED
    private LocalDateTime payTime;

    public PaymentEntity() {
        this.status = "INIT";
        this.payTime = LocalDateTime.now();
    }

    public String getPaymentId() { return paymentId; }
    public void setPaymentId(String paymentId) { this.paymentId = paymentId; }
    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getPayTime() { return payTime; }
    public void setPayTime(LocalDateTime payTime) { this.payTime = payTime; }
}