package com.mall.application.apps.product.mapper;

import com.mall.application.apps.product.entity.ProductEntity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

/**
 * 商品数据映射接口
 */
@Mapper
public interface ProductMapper {

    ProductEntity selectById(@Param("productId") String productId);

    List<ProductEntity> selectPage(@Param("page") int page, @Param("size") int size);

    int insertProduct(ProductEntity productEntity);

    int updateStatus(@Param("productId") String productId, @Param("status") String status);

    int deleteById(@Param("productId") String productId);
}