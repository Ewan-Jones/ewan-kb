package com.mall.application.apps.member.service;

import com.mall.application.apps.member.entity.MemberEntity;
import com.mall.application.apps.member.dto.MemberDTO;
import com.mall.application.apps.member.mapper.MemberMapper;
import com.mall.application.apps.order.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 会员服务 - 会员信息、注册、积分管理
 */
@Service
public class MemberService {

    @Autowired
    private MemberMapper memberMapper;
    @Autowired
    private OrderService orderService;

    public MemberDTO getMemberInfo(String memberId) {
        MemberEntity member = memberMapper.selectById(memberId);
        return new MemberDTO(member);
    }

    public MemberDTO registerMember(MemberEntity memberEntity) {
        memberEntity.setLevel("NORMAL");
        memberEntity.setPoints(0);
        memberMapper.insertMember(memberEntity);
        return new MemberDTO(memberEntity);
    }

    public MemberDTO updateMemberPoints(String memberId, int points) {
        MemberEntity member = memberMapper.selectById(memberId);
        member.setPoints(member.getPoints() + points);
        checkLevelUpgrade(member);
        memberMapper.updatePoints(memberId, member.getPoints());
        return new MemberDTO(member);
    }

    public MemberDTO updateMemberPoints(String orderId, int points) {
        return updateMemberPoints(orderId, points);
    }

    private void checkLevelUpgrade(MemberEntity member) {
        int orderCount = orderService.getOrderCount(member.getMemberId());
        if (orderCount >= 50) {
            member.setLevel("SVIP");
        } else if (orderCount >= 10) {
            member.setLevel("VIP");
        }
    }
}