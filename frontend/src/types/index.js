/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} email
 * @property {string} name
 * @property {'investor' | 'entrepreneur' | 'creator' | 'artisan'} role
 * @property {string} [avatar]
 * @property {number} walletBalance
 * @property {string} createdAt
 */

/**
 * @typedef {Object} ProvenanceRecord
 * @property {string} id
 * @property {'created' | 'transferred' | 'funded' | 'verified'} action
 * @property {string} timestamp
 * @property {User} user
 * @property {string} details
 */

/**
 * @typedef {Object} Asset
 * @property {string} id
 * @property {string} title
 * @property {string} description
 * @property {User} creator
 * @property {'digital-art' | 'music' | 'physical-item' | 'experience' | 'intellectual-property'} category
 * @property {'phygital' | 'digital' | 'physical'} type
 * @property {number} price
 * @property {number} [fundingGoal]
 * @property {number} [currentFunding]
 * @property {string[]} images
 * @property {'active' | 'funded' | 'sold' | 'draft'} status
 * @property {string[]} tags
 * @property {ProvenanceRecord[]} provenance
 * @property {User[]} [collaborators]
 * @property {number} royaltyPercentage
 * @property {string} createdAt
 * @property {string} updatedAt
 */

/**
 * @typedef {Object} Transaction
 * @property {string} id
 * @property {'purchase' | 'funding' | 'royalty' | 'withdrawal'} type
 * @property {number} amount
 * @property {Asset} [asset]
 * @property {User} from
 * @property {User} to
 * @property {string} timestamp
 * @property {'pending' | 'completed' | 'failed'} status
 */

/**
 * @typedef {Object} FundingRound
 * @property {string} id
 * @property {Asset} asset
 * @property {number} goal
 * @property {number} raised
 * @property {{ user: User, amount: number, timestamp: string }[]} investors
 * @property {string} deadline
 * @property {'active' | 'successful' | 'failed'} status
 */