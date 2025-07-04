package com.example.service;
import java.time.LocalDateTime;
import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.ObjectUtil;
import com.example.common.enums.ResultCodeEnum;
import com.example.common.enums.RoleEnum;
import com.example.common.enums.SexEnum;
import com.example.context.BaseContext;
import com.example.entity.Account;
import com.example.entity.User;
import com.example.DAO.UserDAO;
import com.example.entity.UserBasicInfo;
import com.example.entity.UserCheckInfo;
import com.example.exception.CustomException;
import com.example.mapper.UserMapper;
import com.example.mapper.UserBasicInfoMapper;
import com.example.utils.TokenUtils;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.List;
import java.util.Objects;

/**
 * 用户表业务处理
 **/
@Service
public class UserService {

    @Value("${server.port:9090}")
    private String port;

    @Value("${ip:localhost}")
    private String ip;

    @Resource
    private UserMapper userMapper;

    @Resource
    private UserBasicInfoMapper userBasicInfoMapper;

    /**
     * 新增
     */
    @Transactional
    public void add(User user) {
        // 1. 检查用户名和手机号唯一性
        if (ObjectUtil.isNotNull(userMapper.selectByUsername(user.getUsername()))) {
            throw new CustomException(ResultCodeEnum.USER_EXIST_ERROR);
        }
        if (ObjectUtil.isNotNull(userMapper.selectByPhone(user.getPhone()))) {
            throw new CustomException(ResultCodeEnum.PHONE_EXIST_ERROR);
        }

        // 2. 设置默认值
        String avatarUrl = "http://" + ip + ":" + port + "/files/default-avatar.png"; // 建议抽为常量
        user.setAvatar(avatarUrl);
        user.setRegister_time(LocalDateTime.now());
        user.setRole(RoleEnum.USER.name());

        // 3. 插入用户表（自动生成主键）
        userMapper.insert(user);
        Long userId = Long.valueOf(user.getId()); // 自动回填的ID

        // 4. 插入 user_basic_info
        UserBasicInfo ubi = new UserBasicInfo();
        ubi.setUserId(userId);
        ubi.setGender(SexEnum.保密.name());
        userBasicInfoMapper.insert(ubi);

        // 5. 插入 user_check_info
        UserCheckInfo uci = new UserCheckInfo(userId, 0, 0, 0, 0, 0.0, 0.0);
        userBasicInfoMapper.insertCheckInfo(uci);
    }


    /**
     * 删除
     */
    public void deleteById(Integer id) {
        userMapper.deleteById(id);
    }

    public Integer selectMaxId() {
        return userMapper.selectMaxId();
    }

    /**
     * 批量删除
     */
    public void deleteBatch(List<Integer> ids) {
        for (Integer id : ids) {
            userMapper.deleteById(id);
        }
    }

    /**
     * 修改
     */
    public void updateById(User user) {
        User dbUser2 = userMapper.selectByUsername(user.getUsername());
        //  根据当前更新的用户的账号查询数据库  如果数据库存在跟当前更新用户一样账号的数据  那么当前的更新是不合法的  数据重复了
        if (ObjectUtil.isNotEmpty(dbUser2) && !Objects.equals(dbUser2.getId(), user.getId())) {
            throw new CustomException(ResultCodeEnum.USER_EXIST_ERROR);
        }
        userMapper.updateById(user);
    }

    /**
     * 修改if_new
     */
    public void updateIfNewById() {
        User user = new User();
        long userId = BaseContext.getCurrentId();
        int userid1 = (int) userId;
        user.setId(userid1);
        user.setIf_new(false);
        userMapper.updateById(user);
    }

    /**
     * 根据ID查询
     */
    public User selectById(Integer id) {
        return userMapper.selectById(id);
    }

    /**
     * 查询所有
     */
    public List<User> selectAll(User user) {
        return userMapper.selectAll(user);
    }

    /**
     * 分页查询
     */
    public PageInfo<User> selectPage(User user, Integer pageNum, Integer pageSize) {
        PageHelper.startPage(pageNum, pageSize);
        List<User> list = userMapper.selectAll(user);
        return PageInfo.of(list);
    }

    /**
     * 用户登录
     */
    public Account login(Account account) {
        String name;
        Account dbUser;
        User user;
        LocalDateTime currentTime = LocalDateTime.now(); // 默认系统时区
        if(account.getPhone() != null){
            user = userMapper.selectByPhone(account.getPhone());
            System.out.println(user.isIf_new());
            user.setLast_time(currentTime);
            System.out.println(user.isIf_new());
            dbUser = this.selectByUsername(user.getUsername());
        }else{
            user = userMapper.selectByUsername(account.getUsername());
            System.out.println(user.isIf_new());
            user.setLast_time(currentTime);
            System.out.println(user.isIf_new());
            dbUser = this.selectByUsername(account.getUsername());
        }
        System.out.println(user.isIf_new());
        userMapper.updateById(user);
        if (ObjectUtil.isNull(dbUser)) {
            throw new CustomException(ResultCodeEnum.USER_NOT_EXIST_ERROR);
        }
        if (!account.getPassword().equals(dbUser.getPassword())) {   // 比较用户输入密码和数据库密码是否一致
            throw new CustomException(ResultCodeEnum.USER_ACCOUNT_ERROR);
        }
        // 生成token
        String tokenData = dbUser.getId() + "-" + RoleEnum.USER.name();
        String token = TokenUtils.createToken(tokenData, dbUser.getPassword());
        dbUser.setToken(token);
        return dbUser;
    }

    private User selectByUsername(String username) {
        //User user = new User();
        //user.setUsername(username);
        List<User> userList = userMapper.selectByUsername1(username);
        return CollUtil.isEmpty(userList) ? null : userList.get(0);
    }

    /**
     * 用户注册
     */
   public void register(Account account) {
        User user = new User();
        account.setIf_new(true);
        BeanUtils.copyProperties(account, user);  // 拷贝 账号和密码2个属性
        this.add(user);  // 添加用户信息
    }

}
