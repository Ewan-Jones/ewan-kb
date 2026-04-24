package com.mall.application.apps.payment.mapper;

import com.mall.application.apps.payment.entity.PaymentEntity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

/**
 * 支付数据映射接口
 */
@Mapper
public interface PaymentMapper {

    PaymentEntity selectById(@Param("paymentId") String paymentId);

    PaymentEntity selectByOrderId(@Param("orderId") String orderId);

    int insertPayment(PaymentEntity paymentEntity);

    int updateStatus(@Param("paymentId") String paymentId, @Param("status") String status);

    int deleteById(@Param("paymentId") String paymentId);
}