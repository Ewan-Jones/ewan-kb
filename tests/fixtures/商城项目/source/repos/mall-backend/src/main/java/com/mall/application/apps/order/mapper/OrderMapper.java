package com.mall.application.apps.order.mapper;

import com.mall.application.apps.order.entity.OrderEntity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

/**
 * 订单数据映射接口
 */
@Mapper
public interface OrderMapper {

    OrderEntity selectById(@Param("orderId") String orderId);

    List<OrderEntity> selectByMemberId(@Param("memberId") String memberId);

    int insertOrder(OrderEntity orderEntity);

    int updateStatus(@Param("orderId") String orderId, @Param("status") String status);

    int deleteById(@Param("orderId") String orderId);
}