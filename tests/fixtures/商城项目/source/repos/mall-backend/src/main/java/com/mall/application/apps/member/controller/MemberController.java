package com.mall.application.apps.member.controller;

import com.mall.application.apps.member.service.MemberService;
import com.mall.application.apps.member.dto.MemberDTO;
import com.mall.application.apps.member.entity.MemberEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 会员管理控制器
 * 提供会员信息查询、注册、积分更新等接口
 */
@RestController
@RequestMapping("/api/members")
public class MemberController {

    @Autowired
    private MemberService memberService;

    /**
     * 获取会员信息
     */
    @GetMapping("/{memberId}")
    public MemberDTO getMemberInfo(@PathVariable String memberId) {
        return memberService.getMemberInfo(memberId);
    }

    /**
     * 注册会员
     */
    @PostMapping("/register")
    public MemberDTO registerMember(@RequestBody MemberEntity memberEntity) {
        return memberService.registerMember(memberEntity);
    }

    /**
     * 更新会员积分
     */
    @PostMapping("/{memberId}/points")
    public MemberDTO updatePoints(@PathVariable String memberId,
                                  @RequestParam int points) {
        return memberService.updateMemberPoints(memberId, points);
    }
}