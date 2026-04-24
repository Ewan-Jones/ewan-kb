package com.mall.application.apps.member.mapper;

import com.mall.application.apps.member.entity.MemberEntity;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

/**
 * 会员数据映射接口
 */
@Mapper
public interface MemberMapper {

    MemberEntity selectById(@Param("memberId") String memberId);

    int insertMember(MemberEntity memberEntity);

    int updatePoints(@Param("memberId") String memberId, @Param("points") int points);

    int updateLevel(@Param("memberId") String memberId, @Param("level") String level);

    int deleteById(@Param("memberId") String memberId);
}