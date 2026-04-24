package com.mall.application.apps.payment.dto;

import java.math.BigDecimal;

/**
 * 支付数据传输对象
 */
public class PaymentDTO {

    private String paymentId;
    private String orderId;
    private BigDecimal amount;
    private String paymentMethodName;
    private String status;

    public PaymentDTO() {}

    public PaymentDTO(com.mall.application.apps.payment.entity.PaymentEntity entity) {
        this.paymentId = entity.getPaymentId();
        this.orderId = entity.getOrderId();
        this.amount = entity.getAmount();
        this.paymentMethodName = mapMethodName(entity.getPaymentMethod());
        this.status = entity.getStatus();
    }

    private String mapMethodName(String method) {
        switch (method) {
            case "ALIPAY": return "支付宝";
            case "WECHAT": return "微信支付";
            case "BANK_CARD": return "银行卡";
            default: return method;
        }
    }

    public String getPaymentId() { return paymentId; }
    public void setPaymentId(String paymentId) { this.paymentId = paymentId; }
    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal amount) { this.amount = amount; }
    public String getPaymentMethodName() { return paymentMethodName; }
    public void setPaymentMethodName(String paymentMethodName) { this.paymentMethodName = paymentMethodName; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}