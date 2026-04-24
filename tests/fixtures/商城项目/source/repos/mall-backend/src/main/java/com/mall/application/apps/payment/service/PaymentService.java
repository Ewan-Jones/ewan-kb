package com.mall.application.apps.payment.service;

import com.mall.application.apps.payment.entity.PaymentEntity;
import com.mall.application.apps.payment.dto.PaymentDTO;
import com.mall.application.apps.payment.mapper.PaymentMapper;
import com.mall.application.apps.order.service.OrderService;
import com.mall.application.apps.member.service.MemberService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;

/**
 * 支付服务 - 处理支付创建、支付处理、退款流程
 */
@Service
public class PaymentService {

    @Autowired
    private PaymentMapper paymentMapper;
    @Autowired
    private OrderService orderService;
    @Autowired
    private MemberService memberService;

    public PaymentDTO initPayment(String orderId, BigDecimal amount) {
        PaymentEntity payment = new PaymentEntity();
        payment.setOrderId(orderId);
        payment.setAmount(amount);
        payment.setStatus("INIT");
        paymentMapper.insertPayment(payment);
        return new PaymentDTO(payment);
    }

    public PaymentDTO processPayment(String paymentId) {
        PaymentEntity payment = paymentMapper.selectById(paymentId);
        payment.setStatus("PROCESSING");
        paymentMapper.updateStatus(paymentId, "PROCESSING");
        payment.setStatus("SUCCESS");
        paymentMapper.updateStatus(paymentId, "SUCCESS");
        orderService.getOrderDetail(payment.getOrderId());
        memberService.updateMemberPoints(payment.getOrderId(), 10);
        return new PaymentDTO(payment);
    }

    public PaymentDTO refundPayment(String paymentId) {
        PaymentEntity payment = paymentMapper.selectById(paymentId);
        paymentMapper.updateStatus(paymentId, "REFUNDED");
        return new PaymentDTO(payment);
    }

    public PaymentDTO getPaymentDetail(String paymentId) {
        PaymentEntity payment = paymentMapper.selectById(paymentId);
        return new PaymentDTO(payment);
    }
}