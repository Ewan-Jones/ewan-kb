package com.mall.application.apps.order.service;

import com.mall.application.apps.order.entity.OrderEntity;
import com.mall.application.apps.order.dto.OrderDTO;
import com.mall.application.apps.order.mapper.OrderMapper;
import com.mall.application.apps.product.service.ProductService;
import com.mall.application.apps.payment.service.PaymentService;
import com.mall.application.apps.member.service.MemberService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 订单服务 - 处理订单生命周期管理，创建时校验库存、初始化支付、获取会员信息
 */
@Service
public class OrderService {

    @Autowired
    private OrderMapper orderMapper;
    @Autowired
    private ProductService productService;
    @Autowired
    private PaymentService paymentService;
    @Autowired
    private MemberService memberService;

    public OrderDTO createOrder(OrderEntity orderEntity) {
        productService.checkStock(orderEntity.getProductId(), orderEntity.getQuantity());
        memberService.getMemberInfo(orderEntity.getMemberId());
        orderMapper.insertOrder(orderEntity);
        paymentService.initPayment(orderEntity.getOrderId(), orderEntity.getTotalAmount());
        return new OrderDTO(orderEntity);
    }

    public OrderDTO cancelOrder(String orderId) {
        OrderEntity order = orderMapper.selectById(orderId);
        order.setStatus("CANCELLED");
        orderMapper.updateStatus(orderId, "CANCELLED");
        return new OrderDTO(order);
    }

    public OrderDTO getOrderDetail(String orderId) {
        OrderEntity order = orderMapper.selectById(orderId);
        return new OrderDTO(order);
    }

    public int getOrderCount(String memberId) {
        return orderMapper.selectByMemberId(memberId).size();
    }
}