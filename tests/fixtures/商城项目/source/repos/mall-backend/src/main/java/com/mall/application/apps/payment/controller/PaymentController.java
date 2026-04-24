package com.mall.application.apps.payment.controller;

import com.mall.application.apps.payment.service.PaymentService;
import com.mall.application.apps.payment.dto.PaymentDTO;
import com.mall.application.apps.payment.entity.PaymentEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 支付管理控制器
 * 提供支付创建、支付详情查询、退款等接口
 */
@RestController
@RequestMapping("/api/payments")
public class PaymentController {

    @Autowired
    private PaymentService paymentService;

    /**
     * 创建支付
     */
    @PostMapping("/create")
    public PaymentDTO createPayment(@RequestBody PaymentEntity paymentEntity) {
        return paymentService.initPayment(paymentEntity.getOrderId(), paymentEntity.getAmount());
    }

    /**
     * 获取支付详情
     */
    @GetMapping("/{paymentId}")
    public PaymentDTO getPaymentDetail(@PathVariable String paymentId) {
        return paymentService.getPaymentDetail(paymentId);
    }

    /**
     * 退款
     */
    @PostMapping("/refund")
    public PaymentDTO refundPayment(@RequestParam String paymentId) {
        return paymentService.refundPayment(paymentId);
    }
}