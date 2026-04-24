package com.mall.application.apps.member.entity;

import java.time.LocalDateTime;

/**
 * 会员实体类
 * 等级枚举: NORMAL, VIP, SVIP
 */
public class MemberEntity {

    private String memberId;
    private String name;
    private String phone;
    private String email;
    private String level; // NORMAL / VIP / SVIP
    private int points;
    private LocalDateTime registerTime;

    public MemberEntity() {
        this.level = "NORMAL";
        this.points = 0;
        this.registerTime = LocalDateTime.now();
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
    public LocalDateTime getRegisterTime() { return registerTime; }
    public void setRegisterTime(LocalDateTime registerTime) { this.registerTime = registerTime; }
}