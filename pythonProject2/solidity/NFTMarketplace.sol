// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract NFTMarketplace is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    struct NFTItem {
        uint256 tokenId;
        address payable seller;
        address payable owner;
        uint256 price;
        bool listed;
    }

    mapping(uint256 => NFTItem) private _idToNFTItem;
    mapping(uint256 => string) private _tokenURIs;

    event NFTMinted(uint256 indexed tokenId, address owner);
    event NFTListed(uint256 indexed tokenId, uint256 price);
    event NFTBought(uint256 indexed tokenId, address buyer, uint256 price);

    constructor() ERC721("NFT Marketplace", "NFTM") Ownable(msg.sender) {
        _tokenIds.increment();
    }

    function mintNFT(string memory tokenURI) public returns (uint256) {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _mint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);

        _idToNFTItem[newTokenId] = NFTItem(
            newTokenId,
            payable(msg.sender),
            payable(msg.sender),
            0,
            false
        );

        emit NFTMinted(newTokenId, msg.sender);
        return newTokenId;
    }

    function listNFT(uint256 tokenId, uint256 price) public {
        try this.ownerOf(tokenId) returns (address) {
            require(ownerOf(tokenId) == msg.sender, "Not the owner");
            require(price > 0, "Price must be greater than 0");

            _idToNFTItem[tokenId].price = price;
            _idToNFTItem[tokenId].listed = true;
            _idToNFTItem[tokenId].seller = payable(msg.sender);

            emit NFTListed(tokenId, price);
        } catch {
            revert("Token does not exist");
        }
    }

    function buyNFT(uint256 tokenId) public payable {
        NFTItem storage item = _idToNFTItem[tokenId];
        require(item.listed, "NFT is not listed");
        require(msg.value >= item.price, "Insufficient funds");
        require(msg.sender != item.owner, "Cannot buy your own NFT");

        item.seller.transfer(msg.value);
        _transfer(item.owner, msg.sender, tokenId);

        item.owner = payable(msg.sender);
        item.listed = false;
        item.price = 0;

        emit NFTBought(tokenId, msg.sender, msg.value);
    }

    function getNFTItem(uint256 tokenId) public view returns (NFTItem memory) {
        return _idToNFTItem[tokenId];
    }

    function _setTokenURI(uint256 tokenId, string memory tokenURI) private {
        _tokenURIs[tokenId] = tokenURI;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        try this.ownerOf(tokenId) returns (address) {
            return _tokenURIs[tokenId];
        } catch {
            revert("Token does not exist");
        }
    }
} 