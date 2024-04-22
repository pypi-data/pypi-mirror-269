SPACESINADDRESSINFO = """query SpacesInAddressInfo($address: String!, $listSpaceInput: ListSpaceInput!) {
  addressInfo(address: $address) {
    id
    spaces(input: $listSpaceInput) {
      list {
        ...SpaceBasicFrag
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment SpaceBasicFrag on Space {
  id
  name
  info
  thumbnail
  alias
  links
  isVerified
  status
  followersCount
  activeCampaignCount
  __typename
}
"""
CHECK_TWITTER_AC = """mutation checkTwitterAccount($input: VerifyTwitterAccountInput!) {
  checkTwitterAccount(input: $input) {
    address
    twitterUserID
    twitterUserName
    __typename
  }
}
"""
VERIFY_TWITTER_AC = """mutation VerifyTwitterAccount($input: VerifyTwitterAccountInput!) {
  verifyTwitterAccount(input: $input) {
    address
    twitterUserID
    twitterUserName
    __typename
  }
}
"""
PASSPORTINFO = """query PassportInfo($address: String!) {
  addressInfo(address: $address) {
    id
    passport {
      status
      pendingRedactAt
      id
      __typename
    }
    __typename
  }
}
"""
GET_CAMP_INFO = """query CampaignInfo($id: ID!, $address: String!) {
  campaign(id: $id) {
    ...CampaignDetailFrag
    ...CampaignForCampaignDetail
    space {
      ...SpaceDetail
      isAdmin(address: $address)
      __typename
    }
    isBookmarked(address: $address)
    inWatchList
    claimedLoyaltyPoints(address: $address)
    parentCampaign {
      id
      isSequencial
      __typename
    }
    isSequencial
    childrenCampaigns {
      ...CampaignDetailFrag
      parentCampaign {
        id
        isSequencial
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment CampaignDetailFrag on Campaign {
  id
  ...CampaignMedia
  ...CampaignForgePage
  ...CampaignForCampaignParticipantsBox
  name
  numberID
  type
  inWatchList
  cap
  info
  useCred
  smartbalancePreCheck(mintCount: 1)
  smartbalanceDeposited
  formula
  status
  seoImage
  creator
  tags
  thumbnail
  gasType
  isPrivate
  createdAt
  requirementInfo
  description
  enableWhitelist
  chain
  startTime
  endTime
  requireEmail
  requireUsername
  blacklistCountryCodes
  whitelistRegions
  rewardType
  distributionType
  rewardName
  claimEndTime
  loyaltyPoints
  tokenRewardContract {
    id
    address
    chain
    __typename
  }
  tokenReward {
    userTokenAmount
    tokenAddress
    depositedTokenAmount
    tokenRewardId
    tokenDecimal
    tokenLogo
    tokenSymbol
    __typename
  }
  nftHolderSnapshot {
    holderSnapshotBlock
    __typename
  }
  spaceStation {
    id
    address
    chain
    __typename
  }
  ...WhitelistInfoFrag
  ...WhitelistSubgraphFrag
  gamification {
    ...GamificationDetailFrag
    __typename
  }
  creds {
    id
    name
    type
    credType
    credSource
    referenceLink
    description
    lastUpdate
    lastSync
    syncStatus
    credContractNFTHolder {
      timestamp
      __typename
    }
    chain
    eligible(address: $address, campaignId: $id)
    subgraph {
      endpoint
      query
      expression
      __typename
    }
    dimensionConfig
    value {
      gitcoinPassport {
        score
        lastScoreTimestamp
        __typename
      }
      __typename
    }
    commonInfo {
      participateEndTime
      modificationInfo
      __typename
    }
    __typename
  }
  credentialGroups(address: $address) {
    ...CredentialGroupForAddress
    __typename
  }
  rewardInfo {
    discordRole {
      guildId
      guildName
      roleId
      roleName
      inviteLink
      __typename
    }
    premint {
      startTime
      endTime
      chain
      price
      totalSupply
      contractAddress
      banner
      __typename
    }
    loyaltyPoints {
      points
      __typename
    }
    loyaltyPointsMysteryBox {
      points
      weight
      __typename
    }
    __typename
  }
  participants {
    participantsCount
    bountyWinnersCount
    __typename
  }
  taskConfig(address: $address) {
    participateCondition {
      conditions {
        ...ExpressionEntity
        __typename
      }
      conditionalFormula
      eligible
      __typename
    }
    rewardConfigs {
      id
      conditions {
        ...ExpressionEntity
        __typename
      }
      conditionalFormula
      description
      rewards {
        ...ExpressionReward
        __typename
      }
      eligible
      rewardAttrVals {
        attrName
        attrTitle
        attrVal
        __typename
      }
      __typename
    }
    referralConfig {
      id
      conditions {
        ...ExpressionEntity
        __typename
      }
      conditionalFormula
      description
      rewards {
        ...ExpressionReward
        __typename
      }
      eligible
      rewardAttrVals {
        attrName
        attrTitle
        attrVal
        __typename
      }
      __typename
    }
    __typename
  }
  referralCode(address: $address)
  recurringType
  latestRecurringTime
  nftTemplates {
    id
    image
    treasureBack
    __typename
  }
  __typename
}

fragment CampaignMedia on Campaign {
  thumbnail
  rewardName
  type
  gamification {
    id
    type
    __typename
  }
  __typename
}

fragment CredentialGroupForAddress on CredentialGroup {
  id
  description
  credentials {
    ...CredForAddressWithoutMetadata
    __typename
  }
  conditionRelation
  conditions {
    expression
    eligible
    ...CredentialGroupConditionForVerifyButton
    __typename
  }
  rewards {
    expression
    eligible
    rewardCount
    rewardType
    __typename
  }
  rewardAttrVals {
    attrName
    attrTitle
    attrVal
    __typename
  }
  claimedLoyaltyPoints
  __typename
}

fragment CredForAddressWithoutMetadata on Cred {
  id
  name
  type
  credType
  credSource
  referenceLink
  description
  lastUpdate
  lastSync
  syncStatus
  credContractNFTHolder {
    timestamp
    __typename
  }
  chain
  eligible(address: $address)
  subgraph {
    endpoint
    query
    expression
    __typename
  }
  dimensionConfig
  value {
    gitcoinPassport {
      score
      lastScoreTimestamp
      __typename
    }
    __typename
  }
  __typename
}

fragment CredentialGroupConditionForVerifyButton on CredentialGroupCondition {
  expression
  eligibleAddress
  __typename
}

fragment WhitelistInfoFrag on Campaign {
  id
  whitelistInfo(address: $address) {
    address
    maxCount
    usedCount
    claimedLoyaltyPoints
    currentPeriodClaimedLoyaltyPoints
    currentPeriodMaxLoyaltyPoints
    __typename
  }
  __typename
}

fragment WhitelistSubgraphFrag on Campaign {
  id
  whitelistSubgraph {
    query
    endpoint
    expression
    variable
    __typename
  }
  __typename
}

fragment GamificationDetailFrag on Gamification {
  id
  type
  nfts {
    nft {
      id
      animationURL
      category
      powah
      image
      name
      treasureBack
      nftCore {
        ...NftCoreInfoFrag
        __typename
      }
      traits {
        name
        value
        __typename
      }
      __typename
    }
    __typename
  }
  airdrop {
    name
    contractAddress
    token {
      address
      icon
      symbol
      __typename
    }
    merkleTreeUrl
    addressInfo(address: $address) {
      index
      amount {
        amount
        ether
        __typename
      }
      proofs
      __typename
    }
    __typename
  }
  forgeConfig {
    minNFTCount
    maxNFTCount
    requiredNFTs {
      nft {
        category
        powah
        image
        name
        nftCore {
          capable
          contractAddress
          __typename
        }
        __typename
      }
      count
      __typename
    }
    __typename
  }
  __typename
}

fragment NftCoreInfoFrag on NFTCore {
  id
  capable
  chain
  contractAddress
  name
  symbol
  dao {
    id
    name
    logo
    alias
    __typename
  }
  __typename
}

fragment ExpressionEntity on ExprEntity {
  cred {
    id
    name
    type
    credType
    credSource
    dimensionConfig
    referenceLink
    description
    lastUpdate
    lastSync
    chain
    eligible(address: $address)
    metadata {
      visitLink {
        link
        __typename
      }
      twitter {
        isAuthentic
        __typename
      }
      worldcoin {
        dimensions {
          values {
            value
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    commonInfo {
      participateEndTime
      modificationInfo
      __typename
    }
    __typename
  }
  attrs {
    attrName
    operatorSymbol
    targetValue
    __typename
  }
  attrFormula
  eligible
  eligibleAddress
  __typename
}

fragment ExpressionReward on ExprReward {
  arithmetics {
    ...ExpressionEntity
    __typename
  }
  arithmeticFormula
  rewardType
  rewardCount
  rewardVal
  __typename
}

fragment CampaignForgePage on Campaign {
  id
  numberID
  chain
  spaceStation {
    address
    __typename
  }
  gamification {
    forgeConfig {
      maxNFTCount
      minNFTCount
      requiredNFTs {
        nft {
          category
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForCampaignParticipantsBox on Campaign {
  ...CampaignForParticipantsDialog
  id
  chain
  space {
    id
    isAdmin(address: $address)
    __typename
  }
  participants {
    participants(first: 10, after: "-1", download: false) {
      list {
        address {
          id
          avatar
          __typename
        }
        __typename
      }
      __typename
    }
    participantsCount
    bountyWinners(first: 10, after: "-1", download: false) {
      list {
        createdTime
        address {
          id
          avatar
          __typename
        }
        __typename
      }
      __typename
    }
    bountyWinnersCount
    __typename
  }
  __typename
}

fragment CampaignForParticipantsDialog on Campaign {
  id
  name
  type
  rewardType
  chain
  nftHolderSnapshot {
    holderSnapshotBlock
    __typename
  }
  space {
    isAdmin(address: $address)
    __typename
  }
  rewardInfo {
    discordRole {
      guildName
      roleName
      __typename
    }
    __typename
  }
  __typename
}

fragment SpaceDetail on Space {
  id
  name
  info
  thumbnail
  alias
  status
  links
  isVerified
  discordGuildID
  followersCount
  nftCores(input: {first: 1}) {
    list {
      id
      marketLink
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForCampaignDetail on Campaign {
  ...CampaignForGetImage
  ...CampaignForGetMarketLink
  ...CampaignForSiblingSlide
  ...CampaignForCampaignTools
  ...CampaignForCampaignParticipantsBox
  ...CampaignForCampaignTime
  ...CampaignForClaimInfo
  id
  numberID
  isBookmarked(address: $address)
  inWatchList
  name
  description
  space {
    ...SpaceForCampaignInfoSpace
    status
    __typename
  }
  nftTemplates {
    id
    treasureBack
    __typename
  }
  spaceStation {
    address
    __typename
  }
  __typename
}

fragment CampaignForGetImage on Campaign {
  ...GetImageCommon
  nftTemplates {
    image
    __typename
  }
  __typename
}

fragment GetImageCommon on Campaign {
  ...CampaignForTokenObject
  id
  type
  thumbnail
  __typename
}

fragment CampaignForTokenObject on Campaign {
  tokenReward {
    tokenAddress
    tokenSymbol
    tokenDecimal
    tokenLogo
    __typename
  }
  tokenRewardContract {
    id
    chain
    __typename
  }
  __typename
}

fragment CampaignForGetMarketLink on Campaign {
  space {
    nftCores(input: {first: 1}) {
      list {
        id
        marketLink
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForSiblingSlide on Campaign {
  id
  space {
    id
    alias
    __typename
  }
  parentCampaign {
    id
    thumbnail
    isSequencial
    childrenCampaigns {
      id
      ...CampaignForGetImage
      ...CampaignForCheckFinish
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForCheckFinish on Campaign {
  claimedLoyaltyPoints(address: $address)
  whitelistInfo(address: $address) {
    usedCount
    __typename
  }
  __typename
}

fragment SpaceForCampaignInfoSpace on Space {
  ...SpaceForCampaignSpaceFollow
  thumbnail
  name
  isVerified
  categories
  alias
  __typename
}

fragment SpaceForCampaignSpaceFollow on Space {
  id
  isFollowing
  followersCount
  __typename
}

fragment CampaignForCampaignTools on Campaign {
  id
  numberID
  type
  status
  recurringType
  space {
    isAdmin(address: $address)
    alias
    __typename
  }
  childrenCampaigns {
    id
    __typename
  }
  __typename
}

fragment CampaignForCampaignTime on Campaign {
  startTime
  endTime
  __typename
}

fragment CampaignForCalcCampaigClaimNFT on Campaign {
  ...CampaignForCalcCampaignCanClaim
  type
  whitelistInfo(address: $address) {
    usedCount
    __typename
  }
  credentialGroups(address: $address) {
    rewards {
      rewardType
      rewardCount
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForCalcCampaignCanClaim on Campaign {
  distributionType
  cap
  type
  __typename
}

fragment CampaignForCalcCampaigClaimCommon on Campaign {
  type
  whitelistInfo(address: $address) {
    usedCount
    maxCount
    __typename
  }
  credentialGroups(address: $address) {
    rewards {
      rewardType
      rewardCount
      __typename
    }
    __typename
  }
  ...CampaignForCalcCampaignCanClaim
  ...CampaignForIsRaffleParticipateEnded
  __typename
}

fragment CampaignForCalcCampaigClaimToken on Campaign {
  ...CampaignForCalcCampaigClaimCommon
  __typename
}

fragment CampaignForCalcCampaigClaimPoints on Campaign {
  type
  loyaltyPoints
  recurringType
  credentialGroups(address: $address) {
    rewards {
      rewardType
      rewardCount
      __typename
    }
    __typename
  }
  whitelistInfo(address: $address) {
    claimedLoyaltyPoints
    currentPeriodClaimedLoyaltyPoints
    __typename
  }
  __typename
}

fragment CampaignForIsRaffleParticipateEnded on Campaign {
  endTime
  __typename
}

fragment CampaignForClaimInfo on Campaign {
  ...CampaignForCalcCampaigClaimNFT
  ...CampaignForCalcCampaigClaimCommon
  ...CampaignForCalcCampaigClaimToken
  ...CampaignForCalcCampaigClaimPoints
  ...CampaignAsCampaignParticipants
  gasType
  __typename
}

fragment CampaignAsCampaignParticipants on Campaign {
  numNFTMinted
  participants {
    participantsCount
    bountyWinnersCount
    __typename
  }
  __typename
}
"""
CREATE_PERSONA_ID = """mutation GetOrCreateInquiryByAddress($input: GetOrCreateInquiryByAddressInput!) {
  getOrCreateInquiryByAddress(input: $input) {
    status
    vendor
    personaInquiry {
      inquiryID
      sessionToken
      declinedReason
      __typename
    }
    __typename
  }
}
"""

PREPAREPARTICIPATE = """mutation PrepareParticipate($input: PrepareParticipateInput!) {
  prepareParticipate(input: $input) {
    allow
    disallowReason
    signature
    nonce
    mintFuncInfo {
      funcName
      nftCoreAddress
      verifyIDs
      powahs
      cap
      __typename
    }
    extLinkResp {
      success
      data
      error
      __typename
    }
    metaTxResp {
      metaSig2
      autoTaskUrl
      metaSpaceAddr
      forwarderAddr
      metaTxHash
      reqQueueing
      __typename
    }
    solanaTxResp {
      mint
      updateAuthority
      explorerUrl
      signedTx
      verifyID
      __typename
    }
    aptosTxResp {
      signatureExpiredAt
      tokenName
      __typename
    }
    tokenRewardCampaignTxResp {
      signatureExpiredAt
      verifyID
      __typename
    }
    loyaltyPointsTxResp {
      TotalClaimedPoints
      __typename
    }
    flowTxResp {
      Name
      Description
      Thumbnail
      __typename
    }
    __typename
  }
}
"""
SYNCCREDVAL = """mutation SyncCredentialValue($input: SyncCredentialValueInput!) {
  syncCredentialValue(input: $input) {
    value {
      address
      spaceUsers {
        follow
        points
        participations
        __typename
      }
      campaignReferral {
        count
        __typename
      }
      gitcoinPassport {
        score
        lastScoreTimestamp
        __typename
      }
      walletBalance {
        balance
        __typename
      }
      multiDimension {
        value
        __typename
      }
      allow
      survey {
        answers
        __typename
      }
      quiz {
        allow
        correct
        __typename
      }
      __typename
    }
    message
    __typename
  }
}
"""
SIGNIN = """mutation SignIn($input: Auth) {
  signin(input: $input)
}
"""
CHECKUSERNAME = """query IsUsernameExisting($username: String!) {
  usernameExist(username: $username)
}
"""
CREATENEWACCOUT = """mutation CreateNewAccount($input: CreateNewAccount!) {
  createNewAccount(input: $input)
}
"""
CHECK_JWT_QL = """mutation CheckJWT($captchaInput: CaptchaInput!) {
  checkJwt(captchaInput: $captchaInput)
}
"""
PROFILEQ = """query BasicUserInfo($address: String!) {
  addressInfo(address: $address) {
    id
    username
    avatar
    address
    evmAddressSecondary {
      address
      __typename
    }
    hasEmail
    solanaAddress
    aptosAddress
    seiAddress
    injectiveAddress
    flowAddress
    starknetAddress
    bitcoinAddress
    suiAddress
    stacksAddress
    hasEvmAddress
    hasSolanaAddress
    hasAptosAddress
    hasInjectiveAddress
    hasFlowAddress
    hasStarknetAddress
    hasBitcoinAddress
    hasSuiAddress
    hasStacksAddress
    hasTwitter
    hasGithub
    hasDiscord
    hasTelegram
    hasWorldcoin
    displayEmail
    displayTwitter
    displayGithub
    displayDiscord
    displayTelegram
    displayWorldcoin
    displayNamePref
    email
    twitterUserID
    twitterUserName
    githubUserID
    githubUserName
    discordUserID
    discordUserName
    telegramUserID
    telegramUserName
    worldcoinID
    enableEmailSubs
    subscriptions
    isWhitelisted
    isInvited
    isAdmin
    accessToken
    __typename
  }
}
"""
SPACELOYALTYPT = """query SpaceLoyaltyPoints($id: Int, $address: String!, $seasonId: Int) {
  space(id: $id) {
    id
    addressLoyaltyPoints(address: $address, sprintId: $seasonId) {
      id
      points
      rank
      __typename
    }
    __typename
  }
}
"""
GALXEPLUSEXPIRE = """query GetGalaxyPlusExpire($galxeId: String!) {
  plusSubscription(input: {galxeId: $galxeId}) {
    plusSubscription {
      id
      expireAt
      __typename
    }
    __typename
  }
}
"""
CAMPAIGNDETAILALL = """query CampaignDetailAll($id: ID!, $address: String!, $withAddress: Boolean!) {
  campaign(id: $id) {
    ...CampaignForSiblingSlide
    coHostSpaces {
      ...SpaceDetail
      isAdmin(address: $address) @include(if: $withAddress)
      isFollowing @include(if: $withAddress)
      followersCount
      categories
      __typename
    }
    bannerUrl
    ...CampaignDetailFrag
    userParticipants(address: $address, first: 1) @include(if: $withAddress) {
      list {
        status
        premintTo
        __typename
      }
      __typename
    }
    space {
      ...SpaceDetail
      isAdmin(address: $address) @include(if: $withAddress)
      isFollowing @include(if: $withAddress)
      followersCount
      categories
      __typename
    }
    isBookmarked(address: $address) @include(if: $withAddress)
    inWatchList
    claimedLoyaltyPoints(address: $address) @include(if: $withAddress)
    parentCampaign {
      id
      isSequencial
      thumbnail
      __typename
    }
    isSequencial
    numNFTMinted
    childrenCampaigns {
      ...ChildrenCampaignsForCampaignDetailAll
      __typename
    }
    __typename
  }
}

fragment CampaignDetailFrag on Campaign {
  id
  ...CampaignMedia
  ...CampaignForgePage
  ...CampaignForCampaignParticipantsBox
  name
  numberID
  type
  inWatchList
  cap
  info
  useCred
  smartbalancePreCheck(mintCount: 1)
  smartbalanceDeposited
  formula
  status
  seoImage
  creator
  tags
  thumbnail
  gasType
  isPrivate
  createdAt
  requirementInfo
  description
  enableWhitelist
  chain
  startTime
  endTime
  requireEmail
  requireUsername
  blacklistCountryCodes
  whitelistRegions
  rewardType
  distributionType
  rewardName
  claimEndTime
  loyaltyPoints
  tokenRewardContract {
    id
    address
    chain
    __typename
  }
  tokenReward {
    userTokenAmount
    tokenAddress
    depositedTokenAmount
    tokenRewardId
    tokenDecimal
    tokenLogo
    tokenSymbol
    __typename
  }
  nftHolderSnapshot {
    holderSnapshotBlock
    __typename
  }
  spaceStation {
    id
    address
    chain
    __typename
  }
  ...WhitelistInfoFrag
  ...WhitelistSubgraphFrag
  gamification {
    ...GamificationDetailFrag
    __typename
  }
  creds {
    id
    name
    type
    credType
    credSource
    referenceLink
    description
    lastUpdate
    lastSync
    syncStatus
    credContractNFTHolder {
      timestamp
      __typename
    }
    chain
    eligible(address: $address, campaignId: $id)
    subgraph {
      endpoint
      query
      expression
      __typename
    }
    dimensionConfig
    value {
      gitcoinPassport {
        score
        lastScoreTimestamp
        __typename
      }
      __typename
    }
    commonInfo {
      participateEndTime
      modificationInfo
      __typename
    }
    __typename
  }
  credentialGroups(address: $address) {
    ...CredentialGroupForAddress
    __typename
  }
  rewardInfo {
    discordRole {
      guildId
      guildName
      roleId
      roleName
      inviteLink
      __typename
    }
    premint {
      startTime
      endTime
      chain
      price
      totalSupply
      contractAddress
      banner
      __typename
    }
    loyaltyPoints {
      points
      __typename
    }
    loyaltyPointsMysteryBox {
      points
      weight
      __typename
    }
    __typename
  }
  participants {
    participantsCount
    bountyWinnersCount
    __typename
  }
  taskConfig(address: $address) {
    participateCondition {
      conditions {
        ...ExpressionEntity
        __typename
      }
      conditionalFormula
      eligible
      __typename
    }
    rewardConfigs {
      id
      conditions {
        ...ExpressionEntity
        __typename
      }
      conditionalFormula
      description
      rewards {
        ...ExpressionReward
        __typename
      }
      eligible
      rewardAttrVals {
        attrName
        attrTitle
        attrVal
        __typename
      }
      __typename
    }
    referralConfig {
      id
      conditions {
        ...ExpressionEntity
        __typename
      }
      conditionalFormula
      description
      rewards {
        ...ExpressionReward
        __typename
      }
      eligible
      rewardAttrVals {
        attrName
        attrTitle
        attrVal
        __typename
      }
      __typename
    }
    __typename
  }
  referralCode(address: $address)
  recurringType
  latestRecurringTime
  nftTemplates {
    id
    image
    treasureBack
    __typename
  }
  __typename
}

fragment CampaignMedia on Campaign {
  thumbnail
  rewardName
  type
  gamification {
    id
    type
    __typename
  }
  __typename
}

fragment CredentialGroupForAddress on CredentialGroup {
  id
  description
  credentials {
    ...CredForAddressWithoutMetadata
    __typename
  }
  conditionRelation
  conditions {
    expression
    eligible
    ...CredentialGroupConditionForVerifyButton
    __typename
  }
  rewards {
    expression
    eligible
    rewardCount
    rewardType
    __typename
  }
  rewardAttrVals {
    attrName
    attrTitle
    attrVal
    __typename
  }
  claimedLoyaltyPoints
  __typename
}

fragment CredForAddressWithoutMetadata on Cred {
  id
  name
  type
  credType
  credSource
  referenceLink
  description
  lastUpdate
  lastSync
  syncStatus
  credContractNFTHolder {
    timestamp
    __typename
  }
  chain
  eligible(address: $address)
  subgraph {
    endpoint
    query
    expression
    __typename
  }
  dimensionConfig
  value {
    gitcoinPassport {
      score
      lastScoreTimestamp
      __typename
    }
    __typename
  }
  __typename
}

fragment CredentialGroupConditionForVerifyButton on CredentialGroupCondition {
  expression
  eligibleAddress
  __typename
}

fragment WhitelistInfoFrag on Campaign {
  id
  whitelistInfo(address: $address) {
    address
    maxCount
    usedCount
    claimedLoyaltyPoints
    currentPeriodClaimedLoyaltyPoints
    currentPeriodMaxLoyaltyPoints
    __typename
  }
  __typename
}

fragment WhitelistSubgraphFrag on Campaign {
  id
  whitelistSubgraph {
    query
    endpoint
    expression
    variable
    __typename
  }
  __typename
}

fragment GamificationDetailFrag on Gamification {
  id
  type
  nfts {
    nft {
      id
      animationURL
      category
      powah
      image
      name
      treasureBack
      nftCore {
        ...NftCoreInfoFrag
        __typename
      }
      traits {
        name
        value
        __typename
      }
      __typename
    }
    __typename
  }
  airdrop {
    name
    contractAddress
    token {
      address
      icon
      symbol
      __typename
    }
    merkleTreeUrl
    addressInfo(address: $address) {
      index
      amount {
        amount
        ether
        __typename
      }
      proofs
      __typename
    }
    __typename
  }
  forgeConfig {
    minNFTCount
    maxNFTCount
    requiredNFTs {
      nft {
        category
        powah
        image
        name
        nftCore {
          capable
          contractAddress
          __typename
        }
        __typename
      }
      count
      __typename
    }
    __typename
  }
  __typename
}

fragment NftCoreInfoFrag on NFTCore {
  id
  capable
  chain
  contractAddress
  name
  symbol
  dao {
    id
    name
    logo
    alias
    __typename
  }
  __typename
}

fragment ExpressionEntity on ExprEntity {
  cred {
    id
    name
    type
    credType
    credSource
    dimensionConfig
    referenceLink
    description
    lastUpdate
    lastSync
    chain
    eligible(address: $address)
    metadata {
      visitLink {
        link
        __typename
      }
      twitter {
        isAuthentic
        __typename
      }
      worldcoin {
        dimensions {
          values {
            value
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    commonInfo {
      participateEndTime
      modificationInfo
      __typename
    }
    __typename
  }
  attrs {
    attrName
    operatorSymbol
    targetValue
    __typename
  }
  attrFormula
  eligible
  eligibleAddress
  __typename
}

fragment ExpressionReward on ExprReward {
  arithmetics {
    ...ExpressionEntity
    __typename
  }
  arithmeticFormula
  rewardType
  rewardCount
  rewardVal
  __typename
}

fragment CampaignForgePage on Campaign {
  id
  numberID
  chain
  spaceStation {
    address
    __typename
  }
  gamification {
    forgeConfig {
      maxNFTCount
      minNFTCount
      requiredNFTs {
        nft {
          category
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForCampaignParticipantsBox on Campaign {
  ...CampaignForParticipantsDialog
  id
  chain
  space {
    id
    isAdmin(address: $address)
    __typename
  }
  participants {
    participants(first: 10, after: "-1", download: false) {
      list {
        address {
          id
          avatar
          __typename
        }
        __typename
      }
      __typename
    }
    participantsCount
    bountyWinners(first: 10, after: "-1", download: false) {
      list {
        createdTime
        address {
          id
          avatar
          __typename
        }
        __typename
      }
      __typename
    }
    bountyWinnersCount
    __typename
  }
  __typename
}

fragment CampaignForParticipantsDialog on Campaign {
  id
  name
  type
  rewardType
  chain
  nftHolderSnapshot {
    holderSnapshotBlock
    __typename
  }
  space {
    isAdmin(address: $address)
    __typename
  }
  rewardInfo {
    discordRole {
      guildName
      roleName
      __typename
    }
    __typename
  }
  __typename
}

fragment SpaceDetail on Space {
  id
  name
  info
  thumbnail
  alias
  status
  links
  isVerified
  discordGuildID
  followersCount
  nftCores(input: {first: 1}) {
    list {
      id
      marketLink
      __typename
    }
    __typename
  }
  __typename
}

fragment ChildrenCampaignsForCampaignDetailAll on Campaign {
  space {
    ...SpaceDetail
    isAdmin(address: $address) @include(if: $withAddress)
    isFollowing @include(if: $withAddress)
    followersCount
    categories
    __typename
  }
  ...CampaignDetailFrag
  claimedLoyaltyPoints(address: $address) @include(if: $withAddress)
  userParticipants(address: $address, first: 1) @include(if: $withAddress) {
    list {
      status
      __typename
    }
    __typename
  }
  parentCampaign {
    id
    isSequencial
    __typename
  }
  __typename
}

fragment CampaignForSiblingSlide on Campaign {
  id
  space {
    id
    alias
    __typename
  }
  parentCampaign {
    id
    thumbnail
    isSequencial
    childrenCampaigns {
      id
      ...CampaignForGetImage
      ...CampaignForCheckFinish
      __typename
    }
    __typename
  }
  __typename
}

fragment CampaignForCheckFinish on Campaign {
  claimedLoyaltyPoints(address: $address)
  whitelistInfo(address: $address) {
    usedCount
    __typename
  }
  __typename
}

fragment CampaignForGetImage on Campaign {
  ...GetImageCommon
  nftTemplates {
    image
    __typename
  }
  __typename
}

fragment GetImageCommon on Campaign {
  ...CampaignForTokenObject
  id
  type
  thumbnail
  __typename
}

fragment CampaignForTokenObject on Campaign {
  tokenReward {
    tokenAddress
    tokenSymbol
    tokenDecimal
    tokenLogo
    __typename
  }
  tokenRewardContract {
    id
    chain
    __typename
  }
  __typename
}
"""
GETWHITELISTSITES = """query getWhitelistSites {
  whitelistSites {
    name
    url
    __typename
  }
}
"""
RECOMMENDCAMPAIGN = """query RecommendCampaignsByCampiagnAndUser($input: ListCampaignInput!) {
  campaigns(input: $input) {
    totalCount
    pageInfo {
      endCursor
      hasNextPage
      __typename
    }
    list {
      id
      cap
      numberID
      name
      status
      startTime
      endTime
      distributionType
      ...CampaignSnap
      childrenCampaigns {
        id
        inWatchList
        type
        rewardName
        rewardInfo {
          discordRole {
            guildId
            guildName
            roleId
            roleName
            inviteLink
            __typename
          }
          __typename
        }
        __typename
      }
      participants {
        participantsCount
        bountyWinnersCount
        __typename
      }
      tokenRewardContract {
        id
        address
        chain
        __typename
      }
      space {
        id
        name
        thumbnail
        alias
        isVerified
        __typename
      }
      tokenReward {
        userTokenAmount
        tokenAddress
        depositedTokenAmount
        tokenRewardId
        tokenDecimal
        tokenLogo
        tokenSymbol
        __typename
      }
      recurringType
      loyaltyPoints
      __typename
    }
    __typename
  }
}

fragment CampaignSnap on Campaign {
  id
  name
  inWatchList
  inNewYearWatchList
  ...CampaignMedia
  dao {
    ...DaoSnap
    __typename
  }
  __typename
}

fragment DaoSnap on DAO {
  id
  name
  logo
  alias
  isVerified
  __typename
}

fragment CampaignMedia on Campaign {
  thumbnail
  rewardName
  type
  gamification {
    id
    type
    __typename
  }
  __typename
}
"""
CAMPAIGNPARTICIPANTS = """query campaignParticipants($id: ID!, $pfirst: Int!, $pafter: String!, $wfirst: Int!, $wafter: String!, $pDownload: Boolean! = false, $bDownload: Boolean! = false, $isParent: Boolean = false) {
  campaign(id: $id) {
    id
    numberID
    numNFTMinted
    participants @skip(if: $isParent) {
      participants(first: $pfirst, after: $pafter, download: $pDownload) {
        list {
          createdTime
          address {
            id
            username
            avatar
            address
            email
            solanaAddress
            displayNamePref
            aptosAddress
            seiAddress
            flowAddress
            starknetAddress
            discordUserID
            bitcoinAddress
            injectiveAddress
            suiAddress
            stacksAddress
            __typename
          }
          __typename
        }
        pageInfo {
          endCursor
          hasNextPage
          __typename
        }
        __typename
      }
      participantsCount
      bountyWinners(first: $wfirst, after: $wafter, download: $bDownload) {
        list {
          createdTime
          address {
            id
            username
            avatar
            address
            email
            solanaAddress
            displayNamePref
            aptosAddress
            seiAddress
            flowAddress
            starknetAddress
            bitcoinAddress
            injectiveAddress
            suiAddress
            stacksAddress
            __typename
          }
          __typename
        }
        pageInfo {
          endCursor
          hasNextPage
          __typename
        }
        __typename
      }
      bountyWinnersCount
      __typename
    }
    __typename
  }
}
"""
RECOMMENDSPACESBYCAMPIAGNUSER = """query RecommendSpacesByCampiagnAndUser($input: ListSpaceInput!, $spaceCampaignsInput: ListCampaignInput!) {
  spaces(input: $input) {
    totalCount
    pageInfo {
      endCursor
      hasNextPage
      __typename
    }
    list {
      id
      name
      thumbnail
      alias
      isVerified
      backers
      categories
      isFollowing
      campaigns(input: $spaceCampaignsInput) {
        totalCount
        __typename
      }
      __typename
    }
    __typename
  }
}
"""
UPDATEACCESSTOKEN = """mutation UpdateAccessToken($input: UpdateAccessTokenInput!) {
  updateAccessToken(input: $input) {
    accessToken
    __typename
  }
}
"""
GALXEIDEXIST = """query GalxeIDExist($schema: String!) {
  galxeIdExist(schema: $schema)
}
"""
EMAIL_X = """mutation SendVerifyCode($input: SendVerificationEmailInput!) {
  sendVerificationCode(input: $input) {
    code
    message
    __typename
  }
}
"""
EMAIL_UPDATE_VERIF = """mutation UpdateEmail($input: UpdateEmailInput!) {
  updateEmail(input: $input) {
    code
    message
    __typename
  }
}
"""
ADDCRED = """mutation AddTypedCredentialItems($input: MutateTypedCredItemInput!) {
  typedCredentialItems(input: $input) {
    id
    __typename
  }
}
"""
SYNC_CRED = """mutation SyncCredentialValue($input: SyncCredentialValueInput!) {
  syncCredentialValue(input: $input) {
    value {
      address
      spaceUsers {
        follow
        points
        participations
        __typename
      }
      campaignReferral {
        count
        __typename
      }
      gitcoinPassport {
        score
        lastScoreTimestamp
        __typename
      }
      walletBalance {
        balance
        __typename
      }
      multiDimension {
        value
        __typename
      }
      allow
      survey {
        answers
        __typename
      }
      quiz {
        allow
        correct
        __typename
      }
      __typename
    }
    message
    __typename
  }
}
"""
