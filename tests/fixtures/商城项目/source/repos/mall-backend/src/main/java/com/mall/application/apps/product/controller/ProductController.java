package com.mall.application.apps.product.controller;

import com.mall.application.apps.product.service.ProductService;
import com.mall.application.apps.product.dto.ProductDTO;
import com.mall.application.apps.product.entity.ProductEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

/**
 * 商品管理控制器
 * 提供商品列表、详情查询、新增商品等接口
 */
@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    /**
     * 获取商品列表
     */
    @GetMapping("/list")
    public List<ProductDTO> getProductList(@RequestParam(defaultValue = "1") int page,
                                            @RequestParam(defaultValue = "20") int size) {
        return productService.getProductList(page, size);
    }

    /**
     * 获取商品详情
     */
    @GetMapping("/{productId}")
    public ProductDTO getProductDetail(@PathVariable String productId) {
        return productService.getProductDetail(productId);
    }

    /**
     * 新增商品
     */
    @PostMapping("/add")
    public ProductDTO addProduct(@RequestBody ProductEntity productEntity) {
        return productService.addProduct(productEntity);
    }
}