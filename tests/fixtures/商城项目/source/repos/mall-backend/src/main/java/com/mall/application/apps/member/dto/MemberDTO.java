package com.mall.application.apps.member.dto;

import com.mall.application.apps.member.entity.MemberEntity;

/**
 * 会员数据传输对象
 */
public class MemberDTO {

    private String memberId;
    private String name;
    private String phone;
    private String email;
    private String level;
    private int points;

    public MemberDTO() {}

    public MemberDTO(MemberEntity entity) {
        this.memberId = entity.getMemberId();
        this.name = entity.getName();
        this.phone = entity.getPhone();
        this.email = entity.getEmail();
        this.level = entity.getLevel();
        this.points = entity.getPoints();
    }

    public String getMemberId() { return memberId; }
    public void setMemberId(String memberId) { this.memberId = memberId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getLevel() { return level; }
    public void setLevel(String level) { this.level = level; }
    public int getPoints() { return points; }
    public void setPoints(int points) { this.points = points; }
}