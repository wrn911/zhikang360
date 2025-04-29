// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract ERC721Impl is ERC721,AccessControl {
    // 角色定义
    bytes32 public constant PLATFORM_ROLE = keccak256("PLATFORM_ROLE");
    bytes32 public constant WHITELIST_ROLE = keccak256("WHITELIST_ROLE");

    // 定义 TokenInfo 结构体
    struct TokenInfo {
        uint32 lastTransferBlock;  // 上次转账区块号
        uint8 transferCount;       // 转账次数
    }

    // 建立从 token 到约束信息的映射
    mapping(uint256 => TokenInfo) private _tokenInfo;

    // 定义非白名单账户转账的约束条件
    uint32 private immutable _minTransferInterval;
    uint8 private immutable _maxTransferCount;
    
    /**
     * @dev 初始化 NFT 合约
     * @param name_ token 名称
     * @param symbol_ token 符号
     * @param minTransferInterval_ 白名单外最小转账间隔
     * @param maxTransferCount_ 白名单外最大转账次数
     */
     constructor(
        string memory name_,
        string memory symbol_,
        uint32 minTransferInterval_,
        uint8 maxTransferCount_
     ) ERC721(name_,symbol_) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _minTransferInterval = minTransferInterval_;
        _maxTransferCount = maxTransferCount_;
     }

     /**
     * @dev 添加平台合约地址
     * @param platformAddress 要添加的平台合约地址
     */
     function addPlatform(address platformAddress) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(platformAddress != address(0),"Invalid platform address");
        _grantRole(PLATFORM_ROLE, platformAddress);
     }

     /**
     * @dev 移除平台合约地址
     * @param platformAddress 要移除的平台合约地址
     */
     function removePlatform(address platformAddress) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(PLATFORM_ROLE,platformAddress);
     }

     /**
     * @dev 检查是否是平台合约
     * @param platformAddress 要检查的地址
     */
     function isPlatform(address platformAddress) public view returns(bool) {
        return hasRole(PLATFORM_ROLE, platformAddress);
     }

     /**
     * @dev 添加地址到白名单
     * @param account 要添加的地址
     */
    function addToWhitelist(address account) public onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(WHITELIST_ROLE, account);
    }

    /**
     * @dev 从白名单移除地址
     * @param account 要移除的地址
     */
    function removeFromWhitelist(address account) public onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(WHITELIST_ROLE, account);
    }

    /**
     * @dev 检查地址是否在白名单中
     * @param account 要检查的地址
     */
    function isWhitelisted(address account) public view returns (bool) {
        return hasRole(WHITELIST_ROLE, account);
    }


    /**
     * @dev 提高安全性，减少 gas 消耗
     */
    function _checkTransferRestrictions(
        address from,
        address to,
        uint256 tokenId
    ) internal view {
        if (!hasRole(WHITELIST_ROLE, from) && !hasRole(WHITELIST_ROLE, to)) {
            TokenInfo storage info = _tokenInfo[tokenId];
            unchecked {
                if (info.transferCount >= _maxTransferCount) {
                    revert("ERC721: Exceed maximum transfer count");
                }
                
                if (info.lastTransferBlock != 0 && uint32(block.number) - info.lastTransferBlock < _minTransferInterval) {
                    revert("ERC721: Transfer too soon");
                }
            }
        }
    }

    /**
     * @dev 重写transferFrom函数，添加白名单、转账时间间隔和次数限制
     */
    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public virtual override {
        // 限制只有指定平台的合约可以触发交易
        if (msg.sender.code.length>0 && !hasRole(PLATFORM_ROLE,msg.sender)) {
            revert("ERC721: Only platform contract allowed");
        }

        // 转账限制校验
        _checkTransferRestrictions(from, to, tokenId);

        super.transferFrom(from,to,tokenId);

        // 更新 TokenInfo
        if (!hasRole(WHITELIST_ROLE, to) && !hasRole(WHITELIST_ROLE, from)) {
            TokenInfo storage info = _tokenInfo[tokenId];
            unchecked {
                info.lastTransferBlock = uint32(block.number);
                info.transferCount++;
            }
        }
    }

    /**
     * @dev 重写safeTransferFrom函数
     */
     function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) public virtual override {
        // 限制只有指定平台的合约可以触发交易
        if (msg.sender.code.length>0 && !hasRole(PLATFORM_ROLE,msg.sender)) {
            revert("ERC721: Only platform contract allowed");
        }

        // 转账限制校验
        _checkTransferRestrictions(from, to, tokenId);

        super.safeTransferFrom(from,to,tokenId,data);

        // 更新 TokenInfo
        if (!hasRole(WHITELIST_ROLE, to) && !hasRole(WHITELIST_ROLE, from)) {
            TokenInfo storage info = _tokenInfo[tokenId];
            unchecked {
                info.lastTransferBlock = uint32(block.number);
                info.transferCount++;
            }
        }
    }


    /**
     * @dev 获取指定token的最短转账间隔
     * @return 返回最短转账间隔（区块数）
     */
     function getMinTransferInterval() public view returns (uint32) {
        return _minTransferInterval;
     }


     /**
     * @dev 获取指定token的最大转账次数
     * @return 返回最大转账次数
     */
     function getMaxTransferCount() public view returns (uint8) {
        return _maxTransferCount;
     }

     /**
     * @dev 获取指定token的上次转账区块号
     * @param tokenId token的ID
     * @return 返回上次转账的区块号
     */
     function getLastTransferBlock(uint256 tokenId) public view returns(uint32) {
        return _tokenInfo[tokenId].lastTransferBlock;
     }

     /**
     * @dev 获取指定token的当前转账次数
     * @param tokenId token的ID
     * @return 返回当前转账次数
     */
     function getTransferCount(uint256 tokenId) public view returns (uint8) {
        return _tokenInfo[tokenId].transferCount;
    }

    /**
     * @dev 获取指定token的转账信息
     * @param tokenId token的ID
     * @return lastBlock 返回上次转账区块号
     * @return count 返回转账次数
     */
    function getTokenInfo(uint256 tokenId) 
        public 
        view
        returns(uint32 lastBlock,uint8 count) 
        {
            TokenInfo storage info = _tokenInfo[tokenId];
            return (info.lastTransferBlock,info.transferCount);
        }


     /**
     * @dev 实现 supportsInterface 以支持新的接口
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721,AccessControl)
        returns(bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
}

